from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

from users.managers import UserManager
from users.services import get_city_choices


NULLABLE = {'blank': True, 'null': 'True'}


class User(AbstractUser):
    """ Модель пользователя. """

    username = None

    phone_number = models.CharField(
        unique=True,
        max_length=10,
        help_text='Введите номер телефона без использования пробелов.',
        verbose_name='Номер телефона'
    )
    # Поля для реферальной системы.
    invite_code = models.CharField(
        max_length=7,
        **NULLABLE,
        verbose_name='Код приглашения'
    )
    enter_code = models.CharField(
        **NULLABLE,
        verbose_name='Ввод чужого кода приглашения'
    )
    referred_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name='invited_users',
        verbose_name='Пригласивший пользователь'
    )
    # Поле кода верификации.
    verify_code = models.PositiveSmallIntegerField(
        **NULLABLE,
        verbose_name='Код верификации')
    # Стандартные поля профиля.
    city = models.CharField(
        choices=get_city_choices(),
        max_length=150,
        **NULLABLE,
        verbose_name='Город'
    )
    avatar = models.ImageField(
        upload_to='images/users/',
        **NULLABLE,
        verbose_name='Фото профиля'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели пользователя. """
        if self.first_name:
            return f"{self.first_name}"
        else:
            return f"{self.phone_number}"

    def save(self, *args, **kwargs):
        """ Генерирует код приглашения и сохраняет его в поле. """
        if not self.is_superuser:
            self.password = ''
        if not self.pk:
            self.invite_code = get_random_string(7)

        super().save(*args, **kwargs)

    class Meta:
        """ Метаданные для модели пользователя. """
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
