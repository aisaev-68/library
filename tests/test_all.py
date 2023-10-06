from rest_framework.test import APITestCase
from rest_framework import status
from catalog import models
from account.models import User
from django.urls import reverse


class AllAPITestCase(APITestCase):
    """
    Тесты для API.
    """

    def setUp(self):
        """
        Настройка перед тестами.
        """
        self.genre = models.Genre.objects.create(
            name='Genre test'
        )
        self.user = User.objects.create_user(
            username='test',
            first_name='Test1',
            last_name='Test2',
            surname='Test3',
            email='test@test.ru',
            phone='78993445544',
            password='12345',

        )

        self.book = models.Book.objects.create(
            title='Book',
            description='Best book',
            isbn='9785998978470',
            publication_date=2000,
            genre=self.genre,
        )

        self.authors = models.Author.objects.create(
            first_name='Петр',
            last_name='Петров',
            birth_date='1999-01-12',
            biography='Bla bla bla',
        )
        self.book.authors.add(self.authors)
        models.BookImage.objects.create(
            image='media/book_images/1.jpg',
            book=self.book
        )

        models.Review.objects.create(
            text='Test test test test',
            rate=4,
            book=self.book,
            user=self.user
        )

    def tearDown(self):
        User.objects.all().delete()
        models.Genre.objects.all().delete()
        models.Author.objects.all().delete()
        models.Book.objects.all().delete()
        models.BookImage.objects.all().delete()
        models.Review.objects.all().delete()

    def test_my_login_view_valid_credentials(self):
        """
        Тест проверки логина и пароля.
        """
        url = reverse('login')
        data = {
            'username': 'test',
            'password': '12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/account/')

    def test_my_login_view_invalid_credentials(self):
        """
        Тест входа с ошибочными данными.
        """
        url = reverse('login')
        data = {
            'username': 'test',
            'password': '123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login/')  # Assuming unsuccessful login redirects to '/login'

    def test_get_all_genres(self):
        """
        Тест получения всех жанров.
        """
        url = reverse('catalog:genre-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_genre_detail(self):
        """
        Тест получения деталей жанра.
        """
        url = reverse('catalog:genre_by_id', kwargs={'pk': self.genre.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Genre test')

    def test_get_all_books(self):
        """
        Тест получения всех книг.
        """
        url = reverse('catalog:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)

    def test_get_book_detail(self):
        """
        Тест получения деталей книги.
        """
        url = reverse('catalog:book_by_id', kwargs={'pk': self.book.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book')

    def test_create_review(self):
        """
        Тест создания отзыва.
        """
        url = reverse('catalog:book-review', kwargs={'pk': self.book.pk})
        data = {
            'user': self.user.fullName,
            'text': 'This is a test review',
            'rate': 4,
            'book': self.book.id
        }
        self.client.login(username='test', password='12345')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]['text'], 'This is a test review')
        self.assertEqual(response.data[0]['rate'], 4)
        self.assertEqual(response.data[0]['user'], self.user.fullName)

    def test_create_review_unauthenticated(self):
        """
        Тест создания отзыва без аутентификации (ожидается 403 Forbidden).
        """
        url = reverse('catalog:book-review', kwargs={'pk': self.book.pk})
        data = {
            'user': self.user.fullName,
            'text': 'This is a test review',
            'rate': 4,
            'book': self.book.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
