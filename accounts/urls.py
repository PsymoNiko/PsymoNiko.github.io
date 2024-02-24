from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.CreateUserViews.as_view(), name="create_user"),
]