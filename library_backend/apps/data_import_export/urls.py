from django.urls import path
from .views import (export_books, import_books, export_readers, import_readers,
                    template_books, template_readers)

urlpatterns = [
    path('export/books/', export_books, name='export_books'),
    path('import/books/', import_books, name='import_books'),
    path('export/readers/', export_readers, name='export_readers'),
    path('import/readers/', import_readers, name='import_readers'),
    path('template/books/', template_books, name='template_books'),
    path('template/readers/', template_readers, name='template_readers'),
]
