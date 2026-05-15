from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report
from .forms import ReportForm, CustomUserCreationForm

# --- HOME ---
def home(request):
    return render(request, 'main_app/home.html')

# --- DASHBOARD (LOGIKA FINAL & TERPADU) ---
def dashboard(request):
    """Fungsi dashboard tunggal: Menghitung metrik dan menyiapkan data grafik."""
    # 1. Metrik Angka (Kotak Atas)
    total_reports = Report.objects.count()
    reported_count = Report.objects.filter(status='REPORTED').count()
    verified_count = Report.objects.filter(status='VERIFIED').count()
    in_progress_count = Report.objects.filter(status='IN_PROGRESS').count()
    resolved_count = Report.objects.filter(status='RESOLVED').count()

    # 2. Data Grafik Status (Doughnut Chart)
    status_labels = ['Reported', 'Verified', 'In Progress', 'Resolved']
    status_data = [reported_count, verified_count, in_progress_count, resolved_count]

    # 3. Data Grafik Kategori (Bar Chart) - Ambil 5 Teratas
    cat_query = Report.objects.values('category').annotate(total=Count('id')).order_by('-total')[:5]
    category_labels = [item['category'] for item in cat_query]
    category_data = [item['total'] for item in cat_query]

    # 4. Data Tabel (Aktivitas Terbaru)
    latest_reported = Report.objects.filter(status='REPORTED').order_by('-created_at')[:5]
    latest_resolved = Report.objects.filter(status='RESOLVED').order_by('-created_at')[:5]

    context = {
        'total_reports': total_reports,
        'reported_count': reported_count,
        'resolved_count': resolved_count,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
        'verified_count': verified_count,
        'in_progress_count': in_progress_count,
        # Variabel WAJIB agar Chart.js di dashboard.html muncul:
        'status_labels': status_labels,
        'status_data': status_data,
        'category_labels': category_labels,
        'category_data': category_data,
    }
    return render(request, 'dashboard_24782047/dashboard.html', context)

# --- LOGIKA VERIFIKASI BERTINGKAT (Pipeline) ---
def verify_report(request, pk):
    """Menaikkan status: Reported -> Verified -> In Progress -> Resolved."""
    is_admin_user = getattr(request.user, 'is_admin', False)
    if not (request.user.is_superuser or is_admin_user):
        messages.error(request, 'Otoritas ROOT diperlukan.')
        return redirect('report_list')

    report = get_object_or_404(Report, pk=pk)
    
    if report.status == 'REPORTED':
        report.status = 'VERIFIED'
        messages.success(request, f'Laporan #{pk} diverifikasi.')
    elif report.status == 'VERIFIED':
        report.status = 'IN_PROGRESS'
        messages.warning(request, f'Laporan #{pk} masuk tahap pengerjaan.')
    elif report.status == 'IN_PROGRESS':
        report.status = 'RESOLVED'
        messages.info(request, f'Laporan #{pk} dinyatakan selesai.')
    
    report.save()
    return redirect('report_list')

# --- CRUD VIEWS ---
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    ordering = ['-created_at']

class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        if new_status:
            report.status = new_status
            report.save()
        return redirect('report_list')

# --- API VIEWS (UNTUK LIVE SEARCH & MODAL) ---
def report_search_api(request):
    keyword = request.GET.get('q', '').strip()
    reports = Report.objects.filter(
        Q(title__icontains=keyword) | 
        Q(location__icontains=keyword) |
        Q(category__icontains=keyword)
    ).order_by('-created_at')[:50]
    
    data = [{
        'id': r.id, 
        'title': r.title, 
        'location': r.location, 
        'category': r.category,
        'status': r.status, 
        'status_display': r.get_status_display()
    } for r in reports]
    return JsonResponse({'reports': data})

def report_detail_api(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return JsonResponse({
        'id': report.id, 
        'title': report.title, 
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status, 
        'status_display': report.get_status_display(),
        'created_at': report.created_at.strftime('%d %B %Y')
    })