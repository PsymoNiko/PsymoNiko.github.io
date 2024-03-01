from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.CreateUserViews.as_view(), name="create_user"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),

]
