from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render

from .models import Report
from .forms import ReportForm


def home(request):
    return render(request, 'main_app/home.html')


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Silakan login terlebih dahulu.')
            return redirect('login')

        if not request.user.is_admin:
            messages.error(request, 'Akses Ditolak. Hanya admin yang dapat mengakses fitur ini.')
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    ordering = ['-created_at']


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'


class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil ditambahkan.')
        return super().form_valid(form)


class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil diperbarui.')
        return super().form_valid(form)


class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dihapus.')
        return super().form_valid(form)


class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        allowed_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED',
        }

        if report.status in allowed_transitions and allowed_transitions[report.status] == new_status:
            report.status = new_status
            report.save()
            messages.success(
                request,
                f'Status laporan berhasil diubah menjadi {report.get_status_display()}.'
            )
        else:
            messages.error(request, 'Perubahan status tidak valid.')

        return redirect('report_list')


def report_search_api(request):
    keyword = request.GET.get('q', '').strip()

    reports = Report.objects.all().order_by('-created_at')

    if keyword:
        reports = reports.filter(
            Q(title__icontains=keyword) |
            Q(category__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(status__icontains=keyword)
        )

    data = []
    for report in reports[:50]:
        data.append({
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'location': report.location,
            'status': report.status,
            'status_display': report.get_status_display(),
        })

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
        'created_at': report.created_at.strftime('%d %B %Y, %H:%M'),
    })