"""
Views for the recipe APIs
"""

from core.models import Recipe, Tag
from recipe import serializers
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    """View to manage recipe APIs"""

    serializer_class = serializers.RecipeDetailSerializer
    # NOTE: Read a bit more about queryset
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        # NOTE: This method needed to be overridden, in order
        # to filter the recipes by the authenticated user
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request"""
        # NOTE: We override this method in order for it to address 2 endpoints
        # instead of just one. This way, the
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # NOTE: This method overrides Django's behavior for saving a Model
        # object.
        serializer.save(user=self.request.user)


class TagViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Overriding the DRF's default to scope it to the owner user"""

        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)
