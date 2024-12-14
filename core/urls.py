from django.contrib import admin
from django.urls import path, include
from .views import handle_root_redirect
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0





urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('metrics/', include('django_prometheus.urls')),
    path('silk/', include('silk.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("chat/", include("chat.urls")),
    path('user/', include("accounts.urls")),
    path('admin/', admin.site.urls),
    path('', handle_root_redirect, name='handle_root_redirect'),  # Redirect root to index

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
