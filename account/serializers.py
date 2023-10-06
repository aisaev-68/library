from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация пользователя
    """

    class Meta:
        model = User
        fields = ['fullName', 'phone', 'email', 'avatar']


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара.
    """

    class Meta:
        model = User
        fields = ['avatar', 'last_name', 'first_name', 'surname']

    def validate_avatar(self, avatar):
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Размер файла изображения не должен превышать 2 МБ.')
        return avatar

    def update(self, obj, validated_data):
        obj.avatar = validated_data.get('avatar', obj.avatar)
        obj.save()
        return obj


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """
    passwordCurrent = serializers.CharField()
    passwordReply = serializers.CharField()

    class Meta:
        model = User
        fields = ['passwordCurrent', 'password', 'passwordReply']

    def save(self, **kwargs):
        self.instance.password = make_password(self.validated_data['password'])
        self.instance.save()
        return self.instance
