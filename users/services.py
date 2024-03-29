import os
from random import randint
from twilio.rest import Client


def get_verify_code() -> int:
    """ Возвращает 4-ех значный код верификации. """
    verify_code = randint(1000, 9999)
    return verify_code


def send_code_to_phone(phone, code) -> None:
    """ Отправляет код верификации на номер телефона. """
    account_sid = os.getenv('TW_ACC_SID')
    auth_token = os.getenv('TW_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TW_PHONE')

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Ваш код подтверждения: {code}',
        from_=twilio_phone_number,
        to=f'+7{phone}'
    )
    print(message.sid)


def get_city_choices() -> list[tuple]:
    """ Возвращает список городов для поля city (choices). """
    CITIES = [
        ("Санкт-Петербург и область", (
            ("Санкт-Петербург", "Санкт-Петербург"),
            ("Александровская", "Александровская"),
            ("Бокситогорск", "Бокситогорск"),
            ("Большая Ижора", "Большая Ижора"),
            ("Будогощь", "Будогощь"),
            ("Вознесенье", "Вознесенье"),
            ("Волосово", "Волосово"),
            ("Волхов", "Волхов"),
            ("Всеволожск", "Всеволожск"),
            ("Выборг", "Выборг"),
            ("Вырица", "Вырица"),
            ("Высоцк", "Высоцк"),
            ("Гатчина", "Гатчина"),
            ("Дружная Горка", "Дружная Горка"),
            ("Дубровка", "Дубровка"),
            ("Ефимовский", "Ефимовский"),
            ("Зеленогорск", "Зеленогорск"),
            ("Ивангород", "Ивангород"),
            ("Каменногорск", "Каменногорск"),
            ("Кикерино", "Кикерино"),
            ("Кингисепп", "Кингисепп"),
            ("Кириши", "Кириши"),
            ("Кировск", "Кировск"),
            ("Кобринское", "Кобринское"),
            ("Колпино", "Колпино"),
            ("Коммунар", "Коммунар"),
            ("Кронштадт", "Кронштадт"),
            ("Лисий Нос", "Лисий Нос"),
            ("Лодейное Поле", "Лодейное Поле"),
            ("Ломоносов", "Ломоносов"),
            ("Луга", "Луга"),
            ("Павловск", "Павловск"),
            ("Парголово", "Парголово"),
            ("Петродворец", "Петродворец"),
            ("Пикалёво", "Пикалёво"),
            ("Подпорожье", "Подпорожье"),
            ("Приозерск", "Приозерск"),
            ("Пушкин", "Пушкин"),
            ("Сестрорецк", "Сестрорецк"),
            ("Сланцы", "Сланцы"),
            ("Сосновый Бор", "Сосновый Бор"),
            ("Тихвин", "Тихвин"),
            ("Тосно", "Тосно"),
            ("Шлиссельбург", "Шлиссельбург")
        ))
    ]
    return CITIES
