import random
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
from decouple import config

from account.models import User
from catalog import models



class Command(BaseCommand):
    help = 'Создает группы разрешений для пользователей и добавляет пользователей.'

    def handle(self, *args, **options):
        self.stdout.write("Create groups")
        admin_group, created = Group.objects.get_or_create(name="Admin")
        clients_group, created = Group.objects.get_or_create(name="Clients")

        content_type_genre = ContentType.objects.get_for_model(models.Genre)
        genre_permission = Permission.objects.filter(content_type=content_type_genre)
        for perm in genre_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        content_type_book = ContentType.objects.get_for_model(models.Book)
        book_permission = Permission.objects.filter(content_type=content_type_book)
        for perm in book_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        content_type_book_image = ContentType.objects.get_for_model(models.BookImage)
        book_image_permission = Permission.objects.filter(content_type=content_type_book_image)
        for perm in book_image_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        content_type_review = ContentType.objects.get_for_model(models.Review)
        review_permission = Permission.objects.filter(content_type=content_type_review)
        for perm in review_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        content_type_author = ContentType.objects.get_for_model(models.Author)
        author_permission = Permission.objects.filter(content_type=content_type_author)
        for perm in author_permission:
            admin_group.permissions.add(perm)
            clients_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS("Группы созданы."))

        self.stdout.write(self.style.SUCCESS("Создание суперпользователя."))
        User.objects.create_superuser(
            username=config('SUPER_USERNAME'),
            email=config('SUPER_USER_EMAIL'),
            password=config('SUPER_USER_PASSWORD'),
            phone=config('SUPER_USER_PHONE'),
            last_name=config('SUPER_USER_FIRST_NAME'),
            first_name=config('SUPER_USER_LAST_NAME'),
            surname=config('SUPER_USER_SURNAME'),
        )

        self.stdout.write(self.style.SUCCESS("Суперпользователь создан."))

        self.stdout.write(self.style.SUCCESS("Создание администратора."))
        admin_user = User.objects.create_user(
            username=config('USER_ADMIN'),
            email=config('EMAIL'),
            password=config('PASSWORD'),
            phone=config('PHONE'),
            last_name=config('FIRST_NAME'),
            first_name=config('LAST_NAME'),
            surname=config('SURNAME'),
            is_staff=True,
        )
        admin_group = Group.objects.get(name="Admin")
        admin_user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f"{admin_user} добавлен в группу Admin"))

        for _ in range(20):
            person = Person(locale=Locale.RU)
            gender = random.choices([Gender.MALE, Gender.FEMALE])[0]
            client_user = User.objects.create_user(
                username=person.username(),
                first_name=person.first_name(gender=gender),
                last_name=person.last_name(gender=gender),
                surname=person.surname(gender=gender),
                email=person.email(),
                phone=person.telephone('7##########'),
                password='12345',
            )

            client_group = Group.objects.get(name="Clients")
            client_user.groups.add(client_group)

            self.stdout.write(self.style.SUCCESS(f"{client_user} добавлен в группу Clients"))

        self.stdout.write(self.style.SUCCESS("Процесс добавления пользователей завершен успешно."))
