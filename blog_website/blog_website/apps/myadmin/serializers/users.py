from django.utils import timezone
from rest_framework import serializers
from user.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    """管理员序列化器类"""
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 校验密码
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')
            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.last_login = timezone.now()
        user.save()
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(label='密码', write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'webname', 'email', 'password', 'bio', 'address', 'profession', 'avatar_url', 'soliloquy','is_staff')


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        super().update(instance, validated_data)
        if password == '123':
            return instance
        else:
            instance.set_password(password)
            instance.save()
        return instance

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user
