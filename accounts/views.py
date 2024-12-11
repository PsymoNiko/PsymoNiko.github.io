from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from core.opentelemetry_config import configure_tracing
from .filters import TransactionFilter
from .forms import CustomUserRegistrationForm
from .models import User, Account, Transaction
from .serialiezrs import UserSerializer, TransactionSerializer, OrderTransactionSerializer


class CreateUserViews(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('index')  # Redirect to the home page after successful registration
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.phone_number}!')
            return redirect('index')  # Redirect to the home page after successful registration
        else:
            messages.error(request, 'Invalid registration details. Please check the form.')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to your login page


class UserProfileView(APIView):
    def get(self, request, phone_number):
        try:
            user = User.objects.get(phone_number=phone_number)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class MoneyTransferAPIView(generics.ListCreateAPIView):
    # configure_tracing()
    # queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    filterset_fields = ['receiver', 'status', 'created_at']  # Filtering fields
    # search_fields = ['receiver__name', 'status']  #
    # Get the tracer
    tracer = trace.get_tracer(__name__)

    def get_queryset(self):
        # print(self.request.data)
        with self.tracer.start_as_current_span("get_queryset", kind=SpanKind.SERVER):

            user = self.request.user
            # print(user)
            return Transaction.objects.filter(sender__user=user)
        # return Transaction.objects.all()


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return User.objects.all()


class MoneyTransferAPIView2(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            sender_id = serializer.validated_data['sender'].id
            receiver_id = serializer.validated_data['receiver'].id
            amount = serializer.validated_data['amount']

            try:
                with transaction.atomic():
                    # Fetch accounts
                    sender_account = Account.objects.select_for_update().get(id=sender_id)
                    receiver_account = Account.objects.select_for_update().get(id=receiver_id)

                    # Check balance
                    if sender_account.balance < amount:
                        return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

                    # Deduct from sender
                    sender_account.balance -= amount
                    sender_account.save()

                    receiver_account.balance += amount
                    receiver_account.save()
                    transaction_record = serializer.save(status='SUCCESS')

                return Response(TransactionSerializer(transaction_record).data, status=status.HTTP_201_CREATED)
            except Account.DoesNotExist:
                return Response({"error": "Invalid sender or receiver account"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderProcessingView(generics.ListCreateAPIView):
    # configure_tracing()
    # queryset = Transaction.objects.all()
    serializer_class = OrderTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    filterset_fields = ['receiver', 'status', 'created_at']  # Filtering fields
    # search_fields = ['receiver__name', 'status']  #
    # Get the tracer
    tracer = trace.get_tracer(__name__)

    def get_queryset(self):
        # print(self.request.data)
        with self.tracer.start_as_current_span("get_queryset", kind=SpanKind.SERVER):

            user = self.request.user
            # print(user)
            return Transaction.objects.filter(sender__user=user)
        # return Transaction.objects.all()
