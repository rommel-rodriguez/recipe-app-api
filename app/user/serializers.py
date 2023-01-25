"""
Serializers for the user API View
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length':5}}

    def create(self, validated_data):
        """ Create and return a user with encrypted password """
        # NOTE: We need a custom create method, because by default ModelSerializer
        # would save the password as clear-text. Instead, inside this custom method
        # we are using the hashing method defined before to create a new Model
        # object.
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update and return user """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # NOTE: The password must be processed separately
        # Or else, the update method will store/update it
        # as clear text. To prevent this, we must use the 
        # set_password method from the Model object
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token """
    email = serializers.EmailField() 
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs