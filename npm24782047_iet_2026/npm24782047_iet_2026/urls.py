"""
URL configuration for npm24782047_iet_2026 project.
"""
from django.contrib import admin
from django.urls import path, include

# Import views bawaan dari SimpleJWT untuk manajemen token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rute Aplikasi Utama (Sistem Smart City)
    path('', include('main_app.urls')),
    
    # 2. Rute API Utama (Pastikan file main_app/api_urls.py sudah dibuat)
    path('api/', include('main_app.api_urls')), 
    
    # 3. Rute Aplikasi Pendukung
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('accounts/', include('usermanagement_24782047.urls')),
    path('dashboard-sys/', include('dashboard_24782047.urls')),
    
    # =========================================================================
    # TAHAP 2: ENDPOINT AUTENTIKASI JWT (STATELESS LOGIN)
    # =========================================================================
    # Endpoint login: menukar username & password dengan token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint refresh: memperbarui access token tanpa harus login ulang
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]