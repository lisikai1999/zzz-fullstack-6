import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    publisher = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='categories__id')
    status = django_filters.CharFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'isbn', 'category', 'status']
