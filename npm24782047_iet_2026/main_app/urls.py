from django.urls import path
from .views import (
    home,
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    report_search_api,
    report_detail_api,
)

urlpatterns = [
    path('', home, name='home'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('reports/add/', ReportCreateView.as_view(), name='add_report'),
    path('reports/<int:pk>/edit/', ReportUpdateView.as_view(), name='edit_report'),
    path('reports/<int:pk>/delete/', ReportDeleteView.as_view(), name='delete_report'),
    path('reports/<int:pk>/update-status/', ReportUpdateStatusView.as_view(), name='update_status'),
    path('reports/api/search/', report_search_api, name='report_search_api'),
    path('reports/api/<int:pk>/detail/', report_detail_api, name='report_detail_api'),
]