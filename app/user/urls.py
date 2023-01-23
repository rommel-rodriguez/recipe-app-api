"""
URL mappings for the user API
"""

from django.urls import path

from user import views


# NOTE: Needed so the reverse function in the tests
# can find its target
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]