from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BorrowingRecord, BorrowingConfig
from apps.books.serializers import BookListSerializer


class BorrowingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingConfig
        fields = '__all__'


class BorrowingRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_name = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = BorrowingRecord
        fields = ['id', 'user', 'username', 'user_name', 'book', 'book_title', 'book_isbn',
                  'borrow_date', 'due_date', 'return_date', 'renew_count',
                  'status', 'fine_amount', 'notes', 'is_overdue', 'created_at']
        read_only_fields = ['id', 'borrow_date', 'created_at']

    def get_user_name(self, obj):
        return f"{obj.user.last_name}{obj.user.first_name}" or obj.user.username

    def get_is_overdue(self, obj):
        from django.utils import timezone
        if obj.status == 'borrowed' and obj.due_date < timezone.now():
            return True
        return False


class BorrowBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class ReturnBookSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class RenewBookSerializer(serializers.Serializer):
    pass
