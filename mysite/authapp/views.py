"""
Файл views.py содержит реализацию API-представлений (views) для обработки
HTTP-запросов, связанных с взаимодействием с пользовательскими профилями,
аутентификацией и другими функциями.

Список классов:
- AvatarView: Представление для загрузки аватара пользователя.
- ChangePasswordView: Представление для изменения пароля пользователя.
- ProfileView: Представление для работы с профилем пользователя.
- SignInView: Представление для аутентификации пользователя и выдачи токена доступа.
- SignOutView: Представление для выхода пользователя из аккаунта.
- SignUpView: Представление для регистрации нового пользователя.
"""


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
import os

from .models import UserProfile
from .serializers import UserProfileSerializer


class AvatarView(APIView):
    """
    Класс AvatarView представляет API для загрузки и обновления аватара пользователя.

    POST-запрос:
    - Принимает файл аватара, загруженный пользователем.
    - Обновляет аватар пользователя.
    - Возвращает сериализованные данные профиля пользователя.

    """

    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        avatar = request.FILES.get('avatar')
        if avatar:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.avatar = request.FILES['avatar']
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Файл аватара не найден'}, status=400)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(APIView):
    """
    Класс ChangePasswordView представляет API для изменения пароля пользователя.

    POST-запрос:
    - Принимает текущий и новый пароли.
    - Проверяет правильность текущего пароля.
    - Изменяет пароль пользователя на новый.
    - Удаляет существующий токен доступа.
    - Возвращает сообщение об успешном изменении пароля.

    """

    parser_classes = [JSONParser]

    def post(self, request, format=None):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if not current_password or not new_password:
            return Response({'error': 'Неверные данные'}, status=400)

        user = request.user

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            Token.objects.filter(user=user).delete()
            return Response({'success': 'Пароль успешно изменен'}, status=200)
        else:
            return Response({'error': 'Неверный текущий пароль'}, status=400)


@method_decorator(login_required, name='dispatch')
class ProfileView(APIView):
    """
    Класс ProfileView представляет API для просмотра и обновления профиля пользователя.

    GET-запрос:
    - Возвращает сериализованные данные профиля пользователя.

    POST-запрос:
    - Обновляет данные профиля пользователя, включая аватар.
    - Удаляет предыдущий аватар, если новый аватар был загружен.
    - Возвращает сериализованные данные обновленного профиля пользователя.

    """

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request, format=None):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_profile = UserProfile.objects.get(user=request.user)
        data = request.data.copy()
        avatar = data.get('avatar')

        if isinstance(avatar, str):
            del data['avatar']
        else:
            if user_profile.avatar:
                avatar_path = user_profile.avatar.path
                if os.path.exists(avatar_path):
                    os.remove(avatar_path)

        serializer = UserProfileSerializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class SignInView(APIView):
    """
    Класс SignInView представляет API для аутентификации пользователя и выдачи токена доступа.

    POST-запрос:
    - Принимает имя пользователя и пароль.
    - Проверяет правильность имени пользователя и пароля.
    - Выполняет вход пользователя в систему.
    - Генерирует и возвращает токен доступа.

    """

    parser_classes = [FormParser]

    def post(self, request, format=None):
        json_data = list(request.data.keys())[0]
        data = json.loads(json_data)

        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Ошибка авторизации!'}, status=401)


class SignOutView(APIView):
    """
    Класс SignOutView представляет API для выхода пользователя из аккаунта.

    POST-запрос:
    - Удаляет существующий токен доступа пользователя.
    - Выполняет выход пользователя из системы.
    - Возвращает сообщение об успешном выходе из аккаунта.

    """

    def post(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            logout(request)
            return Response({'detail': 'Вы успешно вышли из аккаунта'})
        else:
            return Response({'detail': 'Пользователь не аутентифицирован'}, status=401)


class SignUpView(APIView):
    """
    Класс SignUpView представляет API для регистрации нового пользователя.

    POST-запрос:
    - Принимает имя, имя пользователя и пароль нового пользователя.
    - Создает нового пользователя в системе.
    - Создает профиль пользователя.
    - Генерирует и возвращает токен доступа нового пользователя.

    """

    parser_classes = [FormParser]

    def post(self, request, format=None):
        json_data = list(request.data.keys())[0]
        data = json.loads(json_data)

        name = data.get('name')
        username = data.get('username')
        password = data.get('password')

        if not name or not username or not password:
            return Response({'error': 'Все поля должны быть заполнены'}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = name
            user.save()

            profile = UserProfile(user=user, fullName=name)
            profile.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'success': 'Аккаунт успешно зарегистрирован', 'token': token.key}, status=201)
        except Exception as e:
            return Response({'error': 'Ошибка при регистрации аккаунта'}, status=500)
