from rest_framework import serializers

from users.models import User
from users.validators import PhoneNumberValidator


class LoginSerializer(serializers.ModelSerializer):
    """ Сериалайзер для входа. """

    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator(field='phone_number')]
    )

    class Meta:
        """ Метаданные сериалайзера. """
        model = User
        fields = ('phone_number',)


class ValidateSerializer(serializers.ModelSerializer):
    """ Сериалайзер для валидации телефона. """

    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator(field='phone_number')]
    )

    class Meta:
        """ Метаданные сериалайзера. """
        model = User
        fields = ('phone_number', 'verify_code',)


class ProfileSerializer(serializers.ModelSerializer):
    """ Сериалайзер для просмотра профиля пользователя. """

    class Meta:
        """ Метаданные сериалайзера. """
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'city',
                  'avatar',)


class ReferralSerializer(serializers.ModelSerializer):
    """ Сериалайзер для редактирования профиля пользователя. """

    my_users = serializers.SerializerMethodField(read_only=True)

    def get_my_users(self, instance):
        """
        Возвращает список пользователей,
        которые ввели код приглашения текущего пользователя.
        """
        users = instance.invited_users.all().values_list('phone_number', flat=True)
        return users

    class Meta:
        """ Метаданные сериалайзера. """
        model = User
        fields = ('enter_code', 'referred_by', 'invite_code', 'my_users')
