from rest_framework import serializers
from .models import Book, Genre, CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    coverImage = serializers.CharField(source='cover_image', allow_null=True)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'language',
            'file_type',
            'file_url',
            'date_published',
            'date_uploaded',
            'rating',
            'coverImage',
            'description',
            'pages',
            'isbn',
            'genres'
        ]

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

class CustomUserSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'books']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password') 

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user_id': instance.id,
            'username': instance.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image']
