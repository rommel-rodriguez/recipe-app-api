"""
Serializers for recipe APIs
"""

from core.models import Recipe, Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags: dict, recipe: Recipe):
        """
        Handle getting or creating tags as needed.

        :param tags: The tags to either be created or returned.
        :param recipe: A Recipe object to get or create the tags for.
        :return
        """
        # NOTE: Extracting the authenticated user from the context.
        auth_user = self.context["request"].user

        for tag in tags:
            # NOTE: I assume, that the tag_obj is a more complete object that differs
            # from tag, in that it, also, includes the id of the created tag
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
        # return recipe

    def create(self, validated_data):
        """Overriding default 'create' method to support writing og tags array."""
        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)

        # NOTE: Assuming I do no have to call Recipe.save(recipe) or something
        # Does this function only have to return the object to be created?
        return recipe

    def update(self, instance: Recipe, validated_data):
        """Update recipe."""
        # NOTE: tags must be None by default, because, None is returned if the "tags"
        # field was not included for the update. Meaning, that the client does not wish
        # to update the tags. On the other hand, if tags is [], that means that the
        # client WANTS to update the tags by clearing them.
        tags = validated_data.pop("tags", None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
