from rest_framework import serializers

from catalog import models
from account.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров.
    """
    href = serializers.SerializerMethodField()

    class Meta:
        model = models.Genre
        fields = ['id', 'name', 'href']

    def get_href(self, obj):
        return obj.href()


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализация автора книги.
    """

    biography_short = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Author
        fields = ['id', 'full_name', 'birth_date', 'biography', 'biography_short', 'full_name']

    def get_full_name(self, obj):
        """
        Метод для возвращения полного имени (last_name + first_name).
        """
        return f"{obj.last_name} {obj.first_name}"

    def get_biography_short(self, obj):
        """
        Метод для возвращения краткой биографии (50 символов).
        """
        return obj.biography[:50]


class BookImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор изображений изображения книги.
    """

    class Meta:
        model = models.BookImage
        fields = ('image',)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов.
    """
    user = UserSerializer(many=False)

    class Meta:
        model = models.Review
        fields = ('user', 'text', 'date', 'rate')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["date"] = obj.date.strftime('%Y-%m-%d %H:%M')
        data['user'] = obj.user.fullName
        return data


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор книг.
    """

    title_short = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    description_short = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    # description = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = models.Book
        fields = (
            'id', 'title', 'title_short', 'description', 'description_short', 'isbn', 'publication_date', 'href',
            'images', 'reviews', 'rating', 'authors'
        )

    def get_title_short(self, obj):
        return obj.title[:40]

    def get_description_short(self, obj):
        return obj.description[:15]

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        return obj.rating_info()

    def get_images(self, obj):
        return ['/media/' + str(image.image) for image in obj.images.all()]

    def get_href(self, obj):
        return obj.href()


class BookReviewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор книг, отзывов к книге и рейтинга.
    """
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    description_short = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    title_short = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        fields = (
            'id', 'title', 'title_short', 'description', 'description_short', 'isbn', 'publication_date', 'href',
            'image', 'reviews', 'rating', 'authors')

    def get_title_short(self, obj):
        return obj.title[:50]

    def get_rating(self, obj):
        return obj.rating_info()

    def get_image(self, obj):
        return '/media' + str(obj.images.all()[0])

    def get_href(self, obj):
        return obj.href()

    def get_description_short(self, obj):
        if len(obj.description) > 50:
            return f'{obj.description[:50]}...'
        return obj.description

    def get_authors(self, obj):
        return obj.authors_names()
