from django.urls import path
from .views import CustomLoginView, CustomLogoutView, register_view

# Import view khusus API yang baru saja kita buat di Tahap 5
from .api_views import RegisterView

urlpatterns = [
    # ==========================================
    # RUTE WEB / HTML (Dari Tugas Minggu Lalu)
    # ==========================================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

    # ==========================================
    # RUTE API / STATELESS (Tugas Minggu 10)
    # ==========================================
    # Endpoint untuk mendaftarkan warga (Citizen) baru via API
    path('api/register/', RegisterView.as_view(), name='api_register'),
]