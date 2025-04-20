from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Book, CustomUser
from .serializers import BookSerializer, CustomUserSerializer, RegisterSerializer, BookCollectionSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class BookViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Позволяет искать по полям title, author, genres
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'genres']
    ordering_fields = ['rating', 'dateUploaded', 'datePublished']

    @action(detail=False, methods=['get'], url_path='popular')
    def popular_books(self, request):
        """Возвращает книги, отсортированные по рейтингу (топовые)"""
        top_books = Book.objects.order_by('-rating')[:10]
        serializer = self.get_serializer(top_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search_books(self, request):
        """Поиск книг через параметр ?q="""
        query = request.query_params.get('q', '')
        if query:
            books = Book.objects.filter(
                title__icontains=query
            ) | Book.objects.filter(
                author__icontains=query
            )
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        return Response({"detail": "Query is empty"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class AddBookToCollectionView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Получаем данные книги из запроса
        data = request.data

        book_id = data.get('book_id')
        title = data.get('title')
        cover_image = data.get('cover_image')

        # Если book_id указан, пытаемся найти книгу в БД
        if book_id:
            book = get_object_or_404(Book, id=book_id)
        else:
            # Если book_id нет, создаём книгу с title и cover_image
            if not title or not cover_image:
                return Response({'error': 'title and cover_image are required if book_id is not provided'},
                                status=status.HTTP_400_BAD_REQUEST)
            book = Book.objects.create(title=title, cover_image=cover_image)

        # Добавляем книгу в коллекцию пользователя
        request.user.books.add(book)
        return Response({'message': 'Книга добавлена в коллекцию'}, status=status.HTTP_200_OK)