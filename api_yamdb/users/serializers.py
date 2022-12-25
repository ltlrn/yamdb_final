from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import User
from .utils import generate_token


class ConfCodeSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate_username(self, value):
        if not get_object_or_404(User, username=value):
            raise serializers.ValidationError()
        return value

    def validate_confirmation_code(self, value):
        if not len(value) == 6 or not value.isdigit():
            err_msg = 'Confirmation_code должен состоять из 6 цифр'
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if not user.confirmation_code == data.get('confirmation_code'):
            raise serializers.ValidationError('Wrong confirmation code')
        else:
            return generate_token(user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'role', 'email')
        model = User
