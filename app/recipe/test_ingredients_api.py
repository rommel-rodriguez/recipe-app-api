"""
Tests for ingredients API.
"""

from decimal import Decimal

from core.models import Ingredient, Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import IngredientSerializer
from rest_framework import status
from rest_framework.test import APIClient

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def detail_url(ingredient_id):
    """Returns the URL for a Tag with the given id"""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


def create_user(email="user01@example.com", password="arandompasswod123"):
    """Creates a user"""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientApiTests(TestCase):
    """Test the Ingredient API for un-authenticated users."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test only authenticated users have access to the API"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test Ingredient API for authenticated users"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    # def test_created_ingredient_for_user(self):
    #     """Test that an ingredient is bound to the authenticated user."""
    #     payload = {"name": "Chicha"}
    #     res = self.client.post(INGREDIENTS_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     ingredients = Ingredient.objects.filter(user=self.user)
    #     self.assertTrue(ingredients.exists())
    #     self.assertEqual(ingredients.count(), 1)

    def test_user_can_list_ingredients(self):
        """Test the user can retrieve all ingredients he registered"""
        Ingredient.objects.create(user=self.user, name="Celery")
        Ingredient.objects.create(user=self.user, name="Raspberry")

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        # TODO: Find out the exact reason we have to go through the serializer to test
        # this.
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        ingredient = Ingredient.objects.create(user=self.user, name="Orange")
        # Ingredient.objects.create(user=self.user, name="Lemon")

        another_user = create_user(
            email="otheremail@example.com", password="anotherpass456"
        )
        Ingredient.objects.create(user=another_user, name="Apple")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], ingredient.id)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_update_ingredient(self):
        """Test can update ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name="Orange")
        updated_name = "Black Orange"
        payload = {"name": updated_name}
        res = self.client.patch(detail_url(ingredient.id), payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredient.refresh_from_db()

        for attr, value in payload.items():
            self.assertEqual(getattr(ingredient, attr), value)

    def test_delete_ingredient(self):
        """Test deleting an ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name="Mango")

        res = self.client.delete(detail_url(ingredient.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        ingredients = Ingredient.objects.filter(user=self.user)

        self.assertFalse(ingredients.exists())

    def test_ingredients_assigned_to_recipes(self):
        """Test limiting list of ingredients to those assigned to recipes."""
        in1 = Ingredient.objects.create(user=self.user, name="Apples")
        in2 = Ingredient.objects.create(user=self.user, name="Turkey")
        recipe = Recipe.objects.create(
            title="Apple Crumble",
            time_minutes=5,
            price=Decimal("4.50"),
            user=self.user,
        )
        recipe.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test elements in filtered ingredients are unique."""
        ing = Ingredient.objects.create(user=self.user, name="Eggs")
        Ingredient.objects.create(user=self.user, name="Lentils")
        recipe1 = Recipe.objects.create(
            title="Eggs Benedict",
            time_minutes=60,
            price=Decimal("7.00"),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title="Herb Eggs",
            time_minutes=20,
            price=Decimal("4.00"),
            user=self.user,
        )

        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
