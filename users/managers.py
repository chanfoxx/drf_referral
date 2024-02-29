from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ Менеджер пользовательской модели. """
    use_in_migrations = True

    def create_user(self, phone_number, **extra_fields):
        """ Создает и сохраняет пользователя с переданным phone_number. """
        if not phone_number:
            raise ValueError('Вы должны указать номер телефона.')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.save()

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """ Создает и сохраняет пользователя с переданными e-mail, password. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь статус '
                             'is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь статус '
                             'is_superuser=True.')

        if not phone_number:
            raise ValueError('Вы должны указать номер телефона.')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()

        return user
