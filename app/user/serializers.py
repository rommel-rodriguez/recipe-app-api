"""
Serializers for the user API View
"""

from django.contrib.auth import get_user_model
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