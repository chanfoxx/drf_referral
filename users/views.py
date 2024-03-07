from rest_framework import generics
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from rest_framework.settings import api_settings

from users.models import User
from users.permissions import IsOwner, IsSuperUser
from users.serializers import (ReferralSerializer, ProfileSerializer,
                               LoginSerializer, ValidateSerializer, )
from users.services import get_verify_code, send_code_to_phone


class LoginApiView(views.APIView):
    """ Представление для входа/создания пользователя. """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        """ Вход/регистрация по номеру телефона. """
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            # Находим или создаем пользователя по введенному номеру телефона,
            # генерируем код верификации.
            user, _ = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={'verify_code': get_verify_code()}
            )
            # Отправляем верификационный код на номер телефона.
            # WARNING! Twilio работает только с подтвержденными номерами телефонов.
            try:
                send_code_to_phone(user.phone_number, user.verify_code)
            except Exception as e:
                return Response(
                    data={'error': str(e), 'message': 'Посмотреть код в админке.'}
                )

            user.save()

            return Response(
                {'detail': 'Код успешно отправлен на Ваш номер телефона.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Номер телефона должен иметь 10 символов.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ValidateApiView(views.APIView):
    """
    Представление для подтверждения
    аккаунта(номера телефона) пользователя.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ValidateSerializer)
    def post(self, request):
        """ Верификация доступа к аккаунту по верификационному коду. """
        serializer = ValidateSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verify_code = serializer.validated_data['verify_code']
            try:
                user = User.objects.filter(phone_number=phone_number).first()
            except User.DoesNotExist:
                return Response(
                    {'error': 'Вы ввели номер телефона не верно.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                if user.verify_code == int(verify_code):
                    user.verify_code = None
                    user.save()

                    # Создание или выдача токена для доступа к закрытым эндпоинтам.
                    token, _ = Token.objects.get_or_create(user=user)

                    return Response(
                        {'token': token.key},
                        status=status.HTTP_200_OK
                    )
        else:
            return Response(
                {'error': 'Вы ввели неверный код.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutApiView(views.APIView):
    """ Представление для выхода пользователя. """

    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        """ Выходит из учетной записи текущего пользователя. """
        request.user.auth_token.delete()
        return Response(
            {'detail': 'Вы успешно вышли из аккаунта.'},
            status=status.HTTP_200_OK
        )


class ProfileApiView(generics.RetrieveUpdateAPIView):
    """ Представление для профиля пользователя. """

    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner, IsSuperUser]


class ReferralApiView(generics.RetrieveUpdateAPIView):
    """ Представление для реферальных данных пользователя. """

    serializer_class = ReferralSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner, IsSuperUser]

    def perform_update(self, serializer):
        if self.request.data:
            raise MethodNotAllowed(method='put')

    def partial_update(self, request, *args, **kwargs):
        """ Ввод, проверка и установка кода приглашения. """
        user = self.get_object()
        enter_code = request.data.get('enter_code')

        if user.enter_code:
            return Response(
                {'error': 'Вы уже вводили код.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if enter_code:
                user.enter_code = enter_code
                # Устанавливаем пригласившего пользователя.
                user.referred_by = User.objects.filter(invite_code=enter_code).first()
                user.save()
                return Response(
                    {'detail': 'Инвайт код успешно активирован'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Код неверный.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
