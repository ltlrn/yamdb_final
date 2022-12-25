from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer
from .utils import confirmation_mail, email_check, generate_conf_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin, ]
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'username',
    ]

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me',
        url_name='me',
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        request_data = request.data.copy()
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            # Проверка невозможности не-админу поменять себе роль
            new_role = request_data.get('role')
            if (
                new_role is not None and new_role != user.role
                and user.role != 'admin' and not user.is_superuser
            ):
                request_data['role'] = user.role
            serializer = self.get_serializer(
                user, data=request_data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def mail_code(request):

    email = request.data.get('email')
    username = request.data.get('username')

    error_response = {}

    if not username:
        error_response.update(
            {'username': ['Поле username не должно быть пустым']})

    if not email:
        error_response.update(
            {'email': ['Поле email не должно быть пустым']})

    if username == 'me':
        error_response.update(
            {'username': [f"'{username}' is the restricted username"]})

    if User.objects.filter(username=username).exists():
        error_response.update(
            {'username': [f'Имя {username} уже используется']})

    if User.objects.filter(email=email).exists():
        error_response.update(
            {'email': [f'Адрес {email} уже используется']})

    if not email_check(email):
        err_msg = 'You should provide a valid email address'
        error_response.update({'email': [err_msg]})

    if error_response:
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.create(username=username, email=email)
        user.confirmation_code = generate_conf_code()
        confirmation_mail(email, user.confirmation_code)
        user.save()
        return Response(
            {'email': email, 'username': username}, status=status.HTTP_200_OK)
