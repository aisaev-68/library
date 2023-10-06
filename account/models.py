from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def get_upload_path_by_user(instance, filename):
    """
    Функция возврата пути файла.
    :param filename:
    :return: возвращает путь для записи файла
    """
    return f'avatars/{instance.id}/{filename}'


def validate_image_file_extension(image):
    """
    Валидатор, проверяющий размер изображения
    """
    max_size = 2 * 1024 * 1024  # 2 Мб
    if image.size > max_size:
        raise ValidationError(
            f'Изображение превышает максимальный размер в {max_size / (1024 * 1024)} Mb')


class User(AbstractUser):
    """
    Модель абстрактного пользователя.
    """
    fullName = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="Email")
    surname = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        unique=True
    )
    avatar = models.ImageField(
        upload_to=get_upload_path_by_user,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                    validate_image_file_extension], verbose_name="Аватар",
        default='avatars/default_avatars.png'
    )

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs) -> None:
        if self.fullName:
            self.last_name, self.first_name, self.surname = str(
                self.fullName).split(' ', 2)
        else:
            self.fullName = f'{self.last_name} {self.first_name} {self.surname}'
        super().save(*args, **kwargs)

    def get_url(self) -> str:
        """
        Возвращаем url пользователя.
        """
        return reverse('profile')

    def clean(self) -> None:
        super().clean()
        try:
            existing_user = User.objects.get(phone=self.phone)
            if existing_user and existing_user.id != self.id:
                raise ValidationError("Номер телефона уже существует.")
        except User.DoesNotExist:
            pass

        try:
            existing_user = User.objects.get(email=self.email)
            if existing_user and existing_user.id != self.id:
                raise ValidationError("Эл. адрес уже существует.")
        except User.DoesNotExist:
            pass

    def clean_avatar(self) -> None:
        if self.avatar:
            if self.avatar.size > 2 * 1024 * 1024:
                raise ValidationError('Размер файла изображения не должен превышать 2 МБ.')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
