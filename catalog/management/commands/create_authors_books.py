import json
import os
import random
import uuid

from pathlib import Path
from mimesis import Text, Numeric, Datetime
from mimesis.locales import Locale
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import requests
from django.utils.timezone import now

from account.models import User
from catalog import models


new_dir_file = now().date().strftime("%Y/%m/%d")
uploaded_file_path = Path().parent / "media/book_images" / new_dir_file
uploaded_file_path.mkdir(exist_ok=True, parents=True)
uploaded_file_path = uploaded_file_path.absolute()


class Command(BaseCommand):
    """
    Создание книг.
    """

    def handle(self, *args, **options):

        self.stdout.write("Создание книг.")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with open(os.path.join(BASE_DIR, 'commands/books.json')) as json_file:
            data = json.load(json_file)

        users = [user for user in User.objects.all()]
        print(1111, len(data['items']))
        for item in data['items']:
            books = item['volumeInfo']
            text = Text(locale=Locale.RU)
            number = Numeric()

            url = books['imageLinks']['smallThumbnail']
            request = requests.get(url)
            filename = str(uuid.uuid4())
            file_name = "{name}.{ext}".format(name=filename, ext='jpg')
            file_path = "book_images/{new_dir}/{image_name}".format(new_dir=new_dir_file,
                                                                    image_name=file_name)
            path_absolute = str(Path(uploaded_file_path, file_name))

            with open(path_absolute, 'wb') as f:
                f.write(request.content)

            genre, created = models.Genre.objects.get_or_create(name=books['categories'][0])

            book = models.Book.objects.create(
                title=books.get('title')[:100],
                description=books.get('description', '')[:2000],
                isbn=books.get('industryIdentifiers')[0].get('identifier')[:20],
                publication_date=books.get('publishedDate')[:4],
                genre=genre,
            )

            text1 = Text(locale=Locale.RU)
            list_authors = []
            for author in books['authors']:
                first_name, last_name = author.split(' ')
                authors = models.Author.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    birth_date=str(Datetime().year(minimum=1820, maximum=1995)) + '-01-12',
                    biography=text1.text()[:200],
                )
                list_authors.append(authors)

            book.authors.add(*list_authors)
            models.BookImage.objects.create(image=file_path, book=book)


            user = random.choices(users)[0]
            models.Review.objects.create(
                text=text.text(),
                rate=number.integer_number(start=0, end=5),
                book=book,
                user=user
            )

            self.stdout.write(self.style.SUCCESS(f"Книга {book} создана"))

        self.stdout.write(self.style.SUCCESS("Процесс завершен успешно."))
