from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('phone', 'name', 'password')

    def create(self, validate_data):
        """Create a new user"""
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate create"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=phone,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
