from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/books/', include('apps.books.urls')),
    path('api/v1/borrowing/', include('apps.borrowing.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/data/', include('apps.data_import_export.urls')),
]
