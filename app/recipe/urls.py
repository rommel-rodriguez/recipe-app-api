"""
URL mapping for the recipe app
"""

from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"recipes", views.RecipeViewSet)
router.register(r"tags", views.TagViewset)

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
