from core.models import Ingredient
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
