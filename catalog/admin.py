from django.contrib import admin
from catalog import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_date', 'biography', 'photo')
    search_fields = ('first_name', 'last_name')

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    full_name.short_description = 'Имя и Фамилия'


class BookImageInline(admin.StackedInline):
    model = models.BookImage
    max_num = 1


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'publication_date', 'display_author', 'genre')
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors',)
    list_filter = ('genre',)
    list_editable = ('publication_date',)  # Разрешаем редактирование в списке
    inlines = [BookImageInline]

    def display_author(self, obj):
        return ', '.join([author.__str__() for author in obj.authors.all()])

    display_author.short_description = 'Авторы'
