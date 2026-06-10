from django.urls import path
from . import views # Menggunakan cara ini agar lebih aman dan ringkas

urlpatterns = [
    # --- HOME & DASHBOARD ---
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'), # Pastikan rute ini ada

    # --- REPORT MANAGEMENT (WEB VIEW) ---
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/add/', views.ReportCreateView.as_view(), name='add_report'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='edit_report'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='delete_report'),

    # --- LOGIKA TOMBOL VERIFIKASI (SINKRONISASI) ---
    # Baris ini yang akan menghilangkan error NoReverseMatch kamu
    path('reports/<int:pk>/verify/', views.verify_report, name='verify_report'),
    path('reports/<int:pk>/update-status/', views.ReportUpdateStatusView.as_view(), name='update_status'),

    # --- API ENDPOINTS (UNTUK LIVE SEARCH) ---
    path('reports/api/search/', views.report_search_api, name='report_search_api'),
    path('reports/api/<int:pk>/detail/', views.report_detail_api, name='report_detail_api'),
]