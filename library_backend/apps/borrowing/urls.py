from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BorrowingConfigViewSet, BorrowingRecordViewSet,
                    borrow_book, return_book, renew_book, overdue_list, my_records)

router = DefaultRouter()
router.register('config', BorrowingConfigViewSet, basename='borrowing-config')
router.register('records', BorrowingRecordViewSet, basename='borrowing-record')

urlpatterns = [
    path('borrow/', borrow_book, name='borrow_book'),
    path('return/<int:pk>/', return_book, name='return_book'),
    path('renew/<int:pk>/', renew_book, name='renew_book'),
    path('overdue/', overdue_list, name='overdue_list'),
    path('my-records/', my_records, name='my_records'),
    path('', include(router.urls)),
]
