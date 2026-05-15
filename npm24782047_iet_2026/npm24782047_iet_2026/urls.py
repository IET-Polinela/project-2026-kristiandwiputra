"""
URL configuration for npm24782047_iet_2026 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rute Aplikasi Utama (Sistem Smart City)
    path('', include('main_app.urls')),
    
    # 2. Rute API Utama (Jika kamu memisahkannya)
    path('api/', include('main_app.api_urls')) if 'main_app.api_urls' else None, 
    
    # 3. Rute Aplikasi Pendukung
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('accounts/', include('usermanagement_24782047.urls')),
    path('dashboard-sys/', include('dashboard_24782047.urls')), # Ubah prefix agar tidak bentrok dengan views.dashboard
]