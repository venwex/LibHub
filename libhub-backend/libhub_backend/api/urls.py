from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RegisterView, AddBookToCollectionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('add/', AddBookToCollectionView.as_view(), name='add-book-to-collection'),
]
