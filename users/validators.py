from rest_framework.serializers import ValidationError


class PhoneNumberValidator:
    """ Валидатор для поля - номер телефона. """

    def __init__(self, field):
        """
        Создание экземпляра класса PhoneNumberValidator.

        :param fields: Название поля для валидации.
        """
        self.field = field

    def __call__(self, value):
        """ Позволяет вызывать экземпляр класса как функцию. """
        if len(value) != 10 and not value.isnumeric():
            raise ValidationError(
                'Номер телефона должен иметь 10 символов '
                'и состоять только из цифр.'
            )
