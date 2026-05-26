from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from datetime import timedelta
from apps.books.models import Book, Category
from apps.borrowing.models import BorrowingRecord
from apps.users.permissions import IsAdminOrLibrarian


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def dashboard(request):
    now = timezone.now()
    total_books = Book.objects.count()
    total_readers = User.objects.filter(profile__role='reader').count()
    active_borrows = BorrowingRecord.objects.filter(status='borrowed').count()
    overdue_count = BorrowingRecord.objects.filter(
        status='borrowed', due_date__lt=now).count()
    total_categories = Category.objects.count()
    returned_today = BorrowingRecord.objects.filter(
        return_date__date=now.date()).count()

    return Response({
        'total_books': total_books,
        'total_readers': total_readers,
        'active_borrows': active_borrows,
        'overdue_count': overdue_count,
        'total_categories': total_categories,
        'returned_today': returned_today,
    })


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def borrowing_trend(request):
    months = int(request.query_params.get('months', 12))
    start_date = timezone.now() - timedelta(days=months * 30)
    records = BorrowingRecord.objects.filter(
        borrow_date__gte=start_date
    ).annotate(
        month=TruncMonth('borrow_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    return Response(list(records))


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def category_stats(request):
    categories = Category.objects.annotate(
        book_count=Count('books')
    ).values('name', 'book_count').order_by('-book_count')
    return Response(list(categories))


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def overdue_stats(request):
    now = timezone.now()
    overdue_records = BorrowingRecord.objects.filter(
        status='borrowed', due_date__lt=now
    ).select_related('user', 'book')

    total_overdue = overdue_records.count()
    total_fine = sum(
        (now - r.due_date).days * 0.5 for r in overdue_records
    )

    by_days = {
        '1-7天': overdue_records.filter(
            due_date__gte=now - timedelta(days=7)).count(),
        '8-30天': overdue_records.filter(
            due_date__lt=now - timedelta(days=7),
            due_date__gte=now - timedelta(days=30)).count(),
        '30天以上': overdue_records.filter(
            due_date__lt=now - timedelta(days=30)).count(),
    }

    return Response({
        'total_overdue': total_overdue,
        'total_fine': round(total_fine, 2),
        'by_days': by_days,
    })


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def top_books(request):
    limit = int(request.query_params.get('limit', 10))
    books = Book.objects.annotate(
        borrow_count=Count('borrowing_records')
    ).order_by('-borrow_count')[:limit]

    return Response([
        {'id': b.id, 'title': b.title, 'author': b.author, 'borrow_count': b.borrow_count}
        for b in books
    ])


@api_view(['GET'])
@permission_classes([IsAdminOrLibrarian])
def active_readers(request):
    limit = int(request.query_params.get('limit', 10))
    readers = User.objects.filter(profile__role='reader').annotate(
        borrow_count=Count('borrowing_records')
    ).order_by('-borrow_count')[:limit]

    return Response([
        {'id': r.id, 'username': r.username,
         'name': f"{r.last_name}{r.first_name}" or r.username,
         'borrow_count': r.borrow_count}
        for r in readers
    ])
