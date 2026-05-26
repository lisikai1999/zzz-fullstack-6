from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Book, Category
from .serializers import BookListSerializer, BookDetailSerializer, CategorySerializer
from .filters import BookFilter
from apps.users.permissions import IsAdmin, IsAdminOrLibrarian


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('categories').all()
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'isbn', 'publisher']
    ordering_fields = ['title', 'author', 'created_at', 'available_copies']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAdminOrLibrarian()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAdminOrLibrarian()]
