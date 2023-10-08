import os

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import User


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=200,
        help_text=" Введите жанр книги",
        verbose_name="Жанр книги"
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def href(self):
        """
        Получение ссылки жанров.
        :return: ссылка
        """
        return reverse('catalog') + f'?genre={self.pk}'

    def str(self):
        return self.name


class Author(models.Model):
    """Модель авторов книг."""
    first_name = models.CharField(
        max_length=100,
        help_text="Введите имя автора книги",
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Введите фамилию автора книги",
        verbose_name="Фамилия"
    )
    birth_date = models.DateField(
        help_text="Введите дата рождения автора книги",
        verbose_name="Дата рождения")
    biography = models.TextField(
        max_length=2000,
        help_text="Введите краткую биографию автора книги",
        verbose_name='Краткая биография')
    photo = models.ImageField(
        upload_to='images',
        help_text="Введите фото автора",
        verbose_name="Фoтo автора",
        null=True, blank=True
    )

    def __str__(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ('last_name',)


def get_upload_path_by_products(instance, filename):
    """
        Получение пути для сохранения изображения книги
        :param instance: экземпляр книги
        :param filename: имя файла изображения
        :return: путь для сохранения
        """
    return os.path.join('book_images/', now().date().strftime("%Y/%m/%d"), filename)


class Book(models.Model):
    """Модель книг."""
    title = models.CharField(
        max_length=100,
        help_text="Введите название книги",
        verbose_name="Название книги")
    description = models.TextField(
        max_length=2000,
        help_text="Введите краткое описание книги",
        verbose_name='Краткое описание книги'
    )
    isbn = models.CharField(
        max_length=20,
        help_text="Введите ISBN номер книги",
        verbose_name="ISBN номер книги."
    )
    publication_date = models.IntegerField(
        help_text="Введите год издания книги",
        verbose_name="Год издания книги."
    )

    authors = models.ManyToManyField(
        'Author', related_name="books",
        help_text="Введите автора книги",
        verbose_name="Автор книги"
    )
    genre = models.ForeignKey('Genre',
                              on_delete=models.CASCADE,
                              related_name="books",
                              help_text="Выберите жанр книги",
                              verbose_name="Жанр книги", null=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title',)

    def __str__(self):
        return "{title}".format(title=self.title)

    def authors_names(self) -> list:
        return ["{} {}".format(a.first_name, a.last_name) for a in self.authors.all()]

    def rating_info(self):
        return self.reviews.aggregate(avg_rating=models.Avg('rate')).get('avg_rating')

    def reviews_list(self):
        return list(self.reviews.all())

    def href(self):
        """
        Получение ссылки для книги
        :return: ссылка на детальную информацию о книге
        """
        return reverse('book-detail', args=[str(self.pk)])

    def photo(self):
        """
        Получение главного изображения книги
        :return: изображение
        """
        return self.images.all()[0]

    def display_author(self):
        """
        Функция формирует список авторов.
        """
        return ', '.join([author.last_name for author in
                          self.authors.all()])

    display_author.short_description = 'Авторы'


class BookImage(models.Model):
    """
    Модель изображения книги.
    """
    image = models.FileField(upload_to=get_upload_path_by_products, verbose_name='Изображение книги')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images',
                             verbose_name='Книга')

    class Meta:
        ordering = ["pk"]
        verbose_name = "Изображение книги"
        verbose_name_plural = "Изображения книги"

    def src(self):
        """
        Получаем ссылку на изображение.
        :return: изображение
        """
        return self.image.url

    def __str__(self):
        return f'/{self.image}'


class Review(models.Model):
    """
    Модель отзывов.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name='Пользователь')
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name='Книга')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text
