import logging
from datetime import datetime
from django.conf import settings
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from catalog import models
from catalog import serializers

logger = logging.getLogger(__name__)


def add_catalog_params(func):
    return swagger_auto_schema(
        operation_description='Получение книг по фильтру',
        manual_parameters=[
            openapi.Parameter(
                'filterSearch',
                openapi.IN_QUERY,
                description='Текст поиска',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description='Сколько страниц',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description='Поля соритовки',
                type=openapi.TYPE_STRING,
                enum=['date', 'name', 'rating', 'reviews']  # Здесь указываем доступные значения
            ),
            openapi.Parameter(
                'sortType',
                openapi.IN_QUERY,
                description='Тип сортировки (dec/inc)',
                type=openapi.TYPE_STRING,
                enum=['dec', 'inc']
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description='Количество книг на странице',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'ID genre',
                openapi.IN_QUERY,
                description='Id жанра',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )(func)


class GenreAPIView(APIView):
    """
    Представление для получения жанров книг или жанра.
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: serializers.GenreSerializer(many=True)},
        operation_description="Получение жанра",
    )
    def get(self, request: Request, pk: int = None) -> Response:
        if pk:
            genre = models.Genre.objects.get(pk=pk)
            serializer = serializers.GenreSerializer(genre, many=False)
            logger.info("Получение жанра")
        else:
            genres = models.Genre.objects.all()
            serializer = serializers.GenreSerializer(genres, many=True)
            logger.info("Получение списка жанров")
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BookAPIView(APIView):
    """
    Представление для фильтрации книг по автору или названию книги, а также сортировки книг.
    """
    permission_classes = (AllowAny,)

    def filter_queryset(self, queryset):
        # Извлечение параметров запроса

        search_text = self.request.query_params.get('filterSearch')
        genre = self.request.query_params.get('genre')
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')
        name_filter = self.request.query_params.get('filter[name]')
        title_filter = self.request.query_params.get('filter[title]')
        genre_filter = self.request.query_params.get('filter[genre]')

        # Применение фильтров к queryset
        if search_text:
            queryset = queryset.filter(
                Q(title__icontains=search_text) | Q(description__icontains=search_text)
            )

        if genre:
            queryset = queryset.filter(genre_id=genre)

        if name_filter:
            authors = models.Author.objects.filter(
                Q(first_name__icontains=name_filter) | Q(last_name__icontains=name_filter))
            queryset = queryset.filter(authors__in=authors)

        if title_filter:
            queryset = queryset.filter(title__icontains=title_filter)

        if genre_filter:
            genre = models.Genre.objects.get(name__icontains=genre_filter)
            queryset = queryset.filter(genre=genre)

        if sort:
            sort_field = '-' + sort if sort_type == 'dec' else sort
            if sort == "rating":
                sort_field = '-' + 'reviews__rate' if sort_type == 'dec' else 'reviews__rate'
                queryset = queryset.annotate(avg_reviews=Avg('reviews__rate'))
            elif sort == 'reviews':
                queryset = queryset.annotate(avg_reviews=Avg('reviews'))

            elif sort == 'author':
                sort_field = '-' + 'authors__last_name' if sort_type == 'dec' else 'authors__last_name'

            queryset = queryset.order_by(sort_field)

        return queryset

    def pagination_queryset(self, queryset):
        len_products = len(queryset)
        paginator = PageNumberPagination()
        limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        paginator.page_size = limit
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        current_page = int(self.request.GET.get('page', 1))
        if len_products % limit == 0:
            last_page = len_products // limit
        else:
            last_page = len_products // limit + 1

        return {
            'pagination': paginated_queryset,
            'currentPage': current_page,
            'lastPage': last_page,
        }

    @add_catalog_params
    def get(self, request: Request, pk: int = None) -> Response:

        if pk is not None:
            queryset = self.filter_queryset(models.Book.objects.get(genre_id=pk))
        else:
            queryset = self.filter_queryset(models.Book.objects.order_by('-publication_date').all())

        data = self.pagination_queryset(queryset)
        paginated_queryset = data['pagination']
        serialized_data = serializers.BookSerializer(paginated_queryset, many=True).data

        response_data = {
            'items': serialized_data,
            'currentPage': data['currentPage'],
            'lastPage': data['lastPage'],
        }
        # print(serialized_data)
        logger.info("Получены список книг.")
        return Response(response_data, status=status.HTTP_200_OK)


class BookIdAPIView(APIView):
    """
    Представление для получения книги по ее ID.
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: serializers.BookSerializer(many=False)},
        operation_description="Получение книги по Id",
    )
    def get(self, request: Request, pk: int) -> Response:
        queryset = models.Book.objects.get(pk=pk)

        response_data = serializers.BookSerializer(queryset, many=False).data
        logger.info(f"Получены книга по id {pk}.")
        return Response({'bookInfo': response_data}, status=status.HTTP_200_OK)


class BookDetailAPIView(APIView):
    """
    Представление для получения детальной страницы о книге.
    """

    @swagger_auto_schema(
        responses={200: serializers.BookReviewsSerializer(many=False)},
        operation_description="Получение детальной информации о книге",
    )
    def get(self, request, pk) -> Response:
        queryset = models.Book.objects.prefetch_related('reviews').get(pk=pk)
        queryset.title = queryset.title[:50]
        serializer = serializers.BookReviewsSerializer(queryset, many=False)
        logger.info('Получена детальная информация о книге № %s', queryset.id)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookPopularAPIView(APIView):
    """
    Представление для получения популярных книг.
    """

    @swagger_auto_schema(
        responses={200: serializers.BookSerializer(many=True)},
        operation_description="Получение популярных книг",
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        books = models.Book.objects.annotate(
            average_rating=Avg('reviews__rate', filter=Q(reviews__isnull=False)),
            reviews_count=Count('reviews')
        ).order_by('-average_rating', '-reviews_count')[:8]

        for book in books:
            book.title = book.title[:25] + '...'

        serializer = serializers.BookSerializer(books, many=True)
        logger.info("Получение популярных книг.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    """Представление для поиска книг через строку поиска на странице."""

    def pagination_queryset(self, queryset):
        len_products = len(queryset)
        paginator = PageNumberPagination()
        limit = 6

        paginator.page_size = limit
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        current_page = int(self.request.GET.get('page', 1))
        if len_products % limit == 0:
            last_page = len_products // limit
        else:
            last_page = len_products // limit + 1

        return {
            'pagination': paginated_queryset,
            'currentPage': current_page,
            'lastPage': last_page,
        }

    @swagger_auto_schema(
        operation_description='Получение книг по поиску',
        responses={200: serializers.BookSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'filterSearch',
                openapi.IN_QUERY,
                description='Текст поиска',
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def get(self, request) -> Response:

        search_text = self.request.query_params.get('filterSearch')
        book = models.Book.objects.filter(
            title__icontains=search_text,
            description__icontains=search_text).all()
        data = self.pagination_queryset(book)
        paginated_queryset = data['pagination']
        serialized_data = serializers.BookSerializer(paginated_queryset, many=True).data

        response_data = {
            'items': serialized_data,
            'currentPage': data['currentPage'],
            'lastPage': data['lastPage'],
        }
        logger.info(f"Иноформация по поиску книг {response_data}.")

        return Response(response_data, status=status.HTTP_200_OK)


class BookReviewAPIView(APIView):
    """
    Представление для создания отзывов о книге.
    """
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING),
                'rate': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['text', 'rate'],
        ),
        responses={201: serializers.ReviewSerializer(many=False)},
        operation_description="меню добавления отзывов",
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        data = request.data

        review = models.Review.objects.create(
            user=request.user,
            text=data['text'],
            date=datetime.now(),
            rate=data['rate'],
            book_id=pk
        )
        serializer = self.serializer_class(review, many=False)
        logger.info('Сохранение отзыва о книге пользователем %s', request.user)
        return Response([serializer.data], status=status.HTTP_201_CREATED)
