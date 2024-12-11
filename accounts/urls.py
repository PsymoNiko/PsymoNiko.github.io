from django.urls import path


from . import views

urlpatterns = [
    path("create/", views.CreateUserViews.as_view(), name="create_user"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<str:phone_number>/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('transaction/', views.MoneyTransferAPIView.as_view(), name='money-transfer'),
    path('order/', views.OrderProcessingView.as_view(), name='order-flow'),



]
