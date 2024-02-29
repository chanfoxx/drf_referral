from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class LoginForm(UserCreationForm):
    """ Форма создания пользователя. """

    class Meta:
        model = User
        fields = '__all__'


class ProfileForm(UserChangeForm):
    """ Форма редактирования пользователя. """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'city',
                  'referred_by', 'enter_code', 'invite_code', 'avatar',)
