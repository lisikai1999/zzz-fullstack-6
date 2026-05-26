from django.urls import path
from .views import dashboard, borrowing_trend, category_stats, overdue_stats, top_books, active_readers

urlpatterns = [
    path('dashboard/', dashboard, name='report_dashboard'),
    path('borrowing-trend/', borrowing_trend, name='borrowing_trend'),
    path('category-stats/', category_stats, name='category_stats'),
    path('overdue-stats/', overdue_stats, name='overdue_stats'),
    path('top-books/', top_books, name='top_books'),
    path('active-readers/', active_readers, name='active_readers'),
]
