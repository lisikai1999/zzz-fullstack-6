from rest_framework import serializers
from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'book_count', 'created_at']

    def get_book_count(self, obj):
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'publisher', 'publish_date',
                  'categories', 'total_copies', 'available_copies', 'location',
                  'status', 'created_at']


class BookDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(),
        write_only=True, source='categories', required=False
    )

    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'publisher', 'publish_date',
                  'categories', 'category_ids', 'description', 'cover_image',
                  'total_copies', 'available_copies', 'location', 'status',
                  'created_at', 'updated_at']

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        book = Book.objects.create(**validated_data)
        book.categories.set(categories)
        return book

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.categories.set(categories)
        return instance
