from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet

router = DefaultRouter()
router.register('', BookViewSet, basename='book')

category_router = DefaultRouter()
category_router.register('', CategoryViewSet, basename='category')

urlpatterns = [
    path('categories/', include(category_router.urls)),
    path('', include(router.urls)),
]
