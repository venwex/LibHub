from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, RetrieveUpdateDestroyAPIView, list_books, popular_books, search_books, book_detail, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# router = DefaultRouter()
# router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # path('', include(router.urls)),
    path('search/<str:q>/', search_books, name='search-books'),
    path('books/', list_books, name='list-books'),
    path('books/popular/', popular_books, name='popular-books'),
    path('registration/', RegisterView.as_view(), name='registration-user'),
    path('books/<int:id>/', book_detail, name='book-detail'),
    path('book/crud', RetrieveUpdateDestroyAPIView.as_view(), name='add-book-to-collection'),
    path('login/', TokenObtainPairView.as_view(), name='login-user'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
]
