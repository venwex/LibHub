from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Book, CustomUser
from .serializers import BookSerializer, CustomUserSerializer, RegisterSerializer, BookCollectionSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateDestroyAPIView

User = get_user_model()

@api_view(['GET'])
def list_books(request):
    books = Book.objects.all()

    ordering = request.query_params.get('ordering')
    if ordering:
        books = books.order_by(ordering)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def popular_books(request):
    top_books = Book.objects.order_by('-rating')[:10]
    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_books(request, q):
    if q:
        books = Book.objects.filter(title__icontains=q) | Book.objects.filter(author__icontains=q)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    return Response({"detail": "Query is empty"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@api_view(['GET'])
def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        raise NotFound(detail="Book not found", code=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book)
    return Response(serializer.data)

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class BookViewSet(viewsets.ModelViewSet):
#     # permission_classes = [IsAuthenticated]
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     # Позволяет искать по полям title, author, genres
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'author', 'genres']
#     ordering_fields = ['rating', 'dateUploaded', 'datePublished']

#     @action(detail=False, methods=['get'], url_path='popular')
#     def popular_books(self, request):
#         """Возвращает книги, отсортированные по рейтингу (топовые)"""
#         top_books = Book.objects.order_by('-rating')[:10]
#         serializer = self.get_serializer(top_books, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path='search')
#     def search_books(self, request):
#         """Поиск книг через параметр ?q="""
#         query = request.query_params.get('q', '')
#         if query:
#             books = Book.objects.filter(
#                 title__icontains=query
#             ) | Book.objects.filter(
#                 author__icontains=query
#             )
#             serializer = self.get_serializer(books, many=True)
#             return Response(serializer.data)
#         return Response({"detail": "Query is empty"}, status=status.HTTP_400_BAD_REQUEST)

# class AddBookToCollectionView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data

#         book_id = data.get('book_id')
#         title = data.get('title')
#         cover_image = data.get('cover_image')

#         # Если book_id указан, пытаемся найти книгу в БД
#         if book_id:
#             book = get_object_or_404(Book, id=book_id)
#         else:
#             # Если book_id нет, создаём книгу с title и cover_image
#             if not title or not cover_image:
#                 return Response({'error': 'title and cover_image are required if book_id is not provided'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             book = Book.objects.create(title=title, cover_image=cover_image)

#         # Добавляем книгу в коллекцию пользователя
#         request.user.books.add(book)
#         return Response({'message': 'Book added into the collection'}, status=status.HTTP_200_OK)
