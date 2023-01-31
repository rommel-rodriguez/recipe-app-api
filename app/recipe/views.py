"""
Views for the recipe APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for manage recipe APIs """
    serializer_class = serializers.RecipeSerializer
    # NOTE: Read a bit more about queryset
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve recipes for authenticated user """
        # NOTE: This method needed to be overridden, in order
        # to filter the recipes by the authenticated user 
        return self.queryset.filter(user=self.request.user).order_by('-id')