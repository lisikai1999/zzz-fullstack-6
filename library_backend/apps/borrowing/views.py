from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from .models import BorrowingRecord, BorrowingConfig
from .serializers import (BorrowingRecordSerializer, BorrowingConfigSerializer,
                          BorrowBookSerializer, ReturnBookSerializer)
from apps.books.models import Book
from apps.users.permissions import IsAdmin, IsAdminOrLibrarian


class BorrowingConfigViewSet(viewsets.ModelViewSet):
    queryset = BorrowingConfig.objects.all()
    serializer_class = BorrowingConfigSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAdminOrLibrarian()]
        return [IsAdmin()]


class BorrowingRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowingRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = BorrowingRecord.objects.select_related('user', 'book').all()
        if hasattr(user, 'profile') and user.profile.role in ('admin', 'librarian'):
            pass
        else:
            queryset = queryset.filter(user=user)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            if status_filter == 'overdue':
                queryset = queryset.filter(status='borrowed', due_date__lt=timezone.now())
            else:
                queryset = queryset.filter(status=status_filter)
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        book_id = self.request.query_params.get('book_id')
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset


@api_view(['POST'])
@permission_classes([IsAdminOrLibrarian])
def borrow_book(request):
    serializer = BorrowBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    book_id = serializer.validated_data['book_id']
    user_id = serializer.validated_data['user_id']
    notes = serializer.validated_data.get('notes', '')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'detail': '图书不存在'}, status=status.HTTP_404_NOT_FOUND)

    try:
        borrower = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

    if book.available_copies <= 0:
        return Response({'detail': '该图书暂无可借副本'}, status=status.HTTP_400_BAD_REQUEST)

    active_borrows = BorrowingRecord.objects.filter(
        user=borrower, status='borrowed').count()
    max_count = borrower.profile.max_borrow_count
    if active_borrows >= max_count:
        return Response({'detail': f'已达最大借阅数量({max_count})'}, status=status.HTTP_400_BAD_REQUEST)

    membership = borrower.profile.membership_type
    try:
        config = BorrowingConfig.objects.get(membership_type=membership)
        borrow_days = config.max_borrow_days
    except BorrowingConfig.DoesNotExist:
        borrow_days = 30

    due_date = timezone.now() + timedelta(days=borrow_days)
    record = BorrowingRecord.objects.create(
        user=borrower, book=book, due_date=due_date, notes=notes
    )
    book.available_copies -= 1
    if book.available_copies == 0:
        book.status = 'borrowed'
    book.save()

    return Response(BorrowingRecordSerializer(record).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAdminOrLibrarian])
def return_book(request, pk):
    try:
        record = BorrowingRecord.objects.get(id=pk)
    except BorrowingRecord.DoesNotExist:
        return Response({'detail': '借阅记录不存在'}, status=status.HTTP_404_NOT_FOUND)

    if record.status == 'returned':
        return Response({'detail': '该图书已归还'}, status=status.HTTP_400_BAD_REQUEST)

    now = timezone.now()
    record.return_date = now
    record.status = 'returned'

    if now > record.due_date:
        overdue_days = (now - record.due_date).days
        membership = record.user.profile.membership_type
        try:
            config = BorrowingConfig.objects.get(membership_type=membership)
            fine = overdue_days * float(config.fine_per_day)
        except BorrowingConfig.DoesNotExist:
            fine = overdue_days * 0.5
        record.fine_amount = fine

    notes = request.data.get('notes', '')
    if notes:
        record.notes = notes
    record.save()

    book = record.book
    book.available_copies += 1
    if book.available_copies > 0:
        book.status = 'available'
    book.save()

    return Response(BorrowingRecordSerializer(record).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def renew_book(request, pk):
    try:
        record = BorrowingRecord.objects.get(id=pk)
    except BorrowingRecord.DoesNotExist:
        return Response({'detail': '借阅记录不存在'}, status=status.HTTP_404_NOT_FOUND)

    if record.status != 'borrowed':
        return Response({'detail': '只有借出状态的图书可以续借'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if user.profile.role == 'reader' and record.user != user:
        return Response({'detail': '无权操作'}, status=status.HTTP_403_FORBIDDEN)

    membership = record.user.profile.membership_type
    try:
        config = BorrowingConfig.objects.get(membership_type=membership)
        max_renew = config.max_renew_times
        renew_days = config.max_borrow_days
    except BorrowingConfig.DoesNotExist:
        max_renew = 2
        renew_days = 30

    if record.renew_count >= max_renew:
        return Response({'detail': f'已达最大续借次数({max_renew})'}, status=status.HTTP_400_BAD_REQUEST)

    record.due_date = record.due_date + timedelta(days=renew_days)
    record.renew_count += 1
    record.save()

    return Response(BorrowingRecordSerializer(record).data)


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def overdue_list(request):
    now = timezone.now()
    records = BorrowingRecord.objects.filter(
        status='borrowed', due_date__lt=now
    ).select_related('user', 'book')
    serializer = BorrowingRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_records(request):
    records = BorrowingRecord.objects.filter(
        user=request.user
    ).select_related('book')
    serializer = BorrowingRecordSerializer(records, many=True)
    return Response(serializer.data)
