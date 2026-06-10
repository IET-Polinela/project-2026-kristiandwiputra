from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

from .models import Report
from .forms import ReportForm, CustomUserCreationForm
from .serializers import ReportSerializer


def is_admin_account(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'is_admin', False))


def visible_reports_for(user):
    queryset = Report.objects.select_related('reporter')

    if is_admin_account(user):
        return queryset.exclude(status='DRAFT')

    if user.is_authenticated:
        return queryset.filter(Q(reporter=user) | ~Q(status='DRAFT'))

    return queryset.exclude(status='DRAFT')


def home(request):
    return render(request, 'main_app/home.html')


def dashboard(request):
    reports = visible_reports_for(request.user)

    total_reports = reports.count()
    reported_count = reports.filter(status='REPORTED').count()
    verified_count = reports.filter(status='VERIFIED').count()
    in_progress_count = reports.filter(status='IN_PROGRESS').count()
    resolved_count = reports.filter(status='RESOLVED').count()

    status_labels = ['Reported', 'Verified', 'In Progress', 'Resolved']
    status_data = [reported_count, verified_count, in_progress_count, resolved_count]

    cat_query = reports.values('category').annotate(total=Count('id')).order_by('-total')[:5]
    category_labels = [item['category'] for item in cat_query]
    category_data = [item['total'] for item in cat_query]

    latest_reported = reports.filter(status='REPORTED').order_by('-created_at')[:5]
    latest_resolved = reports.filter(status='RESOLVED').order_by('-created_at')[:5]

    context = {
        'total_reports': total_reports,
        'reported_count': reported_count,
        'resolved_count': resolved_count,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
        'verified_count': verified_count,
        'in_progress_count': in_progress_count,
        'status_labels': status_labels,
        'status_data': status_data,
        'category_labels': category_labels,
        'category_data': category_data,
    }

    return render(request, 'dashboard_24782047/dashboard.html', context)


def verify_report(request, pk):
    if not is_admin_account(request.user):
        messages.error(request, 'Akses ditolak.')
        return redirect('report_list')

    report = get_object_or_404(Report.objects.exclude(status='DRAFT'), pk=pk)

    if report.status == 'REPORTED':
        report.status = 'VERIFIED'
        messages.success(request, f'Laporan #{pk} diverifikasi.')
    elif report.status == 'VERIFIED':
        report.status = 'IN_PROGRESS'
        messages.warning(request, f'Laporan #{pk} masuk tahap pengerjaan.')
    elif report.status == 'IN_PROGRESS':
        report.status = 'RESOLVED'
        messages.info(request, f'Laporan #{pk} dinyatakan selesai.')
    else:
        messages.info(request, f'Laporan #{pk} tidak memiliki perubahan status lanjutan.')

    report.save()
    return redirect('report_list')


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    paginate_by = 25

    def get_queryset(self):
        return visible_reports_for(self.request.user).order_by('-created_at')


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

    def get_queryset(self):
        return visible_reports_for(self.request.user)


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        messages.error(request, 'Penambahan laporan dilakukan melalui web citizen.')
        return redirect('report_list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = 'DRAFT'
        return super().form_valid(form)


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        if is_admin_account(self.request.user):
            return Report.objects.exclude(status='DRAFT')
        return Report.objects.none()


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        if is_admin_account(self.request.user):
            return Report.objects.exclude(status='DRAFT')
        return Report.objects.none()


class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not is_admin_account(request.user):
            messages.error(request, 'Akses ditolak.')
            return redirect('report_list')

        report = get_object_or_404(Report.objects.exclude(status='DRAFT'), pk=pk)
        new_status = request.POST.get('status')

        if new_status and new_status != 'DRAFT':
            report.status = new_status
            report.save()

        return redirect('report_list')


def report_search_api(request):
    keyword = request.GET.get('q', '').strip()

    reports = visible_reports_for(request.user).filter(
        Q(title__icontains=keyword) |
        Q(location__icontains=keyword) |
        Q(category__icontains=keyword)
    ).order_by('-created_at')[:50]

    data = [{
        'id': report.id,
        'title': report.title,
        'location': report.location,
        'category': report.category,
        'description': report.description,
        'status': report.status,
        'status_display': report.get_status_display(),
        'created_at': report.created_at.strftime('%d %b %Y, %H:%M'),
    } for report in reports]

    return JsonResponse({'reports': data})


def report_detail_api(request, pk):
    report = get_object_or_404(visible_reports_for(request.user), pk=pk)

    return JsonResponse({
        'id': report.id,
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
        'status_display': report.get_status_display(),
        'created_at': report.created_at.strftime('%d %B %Y'),
        'updated_at': report.updated_at.strftime('%d %B %Y, %H:%M'),
    })


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab', 'my_reports')

        queryset = Report.objects.select_related('reporter').order_by('-updated_at')

        if is_admin_account(user):
            return queryset.exclude(status='DRAFT')

        if tab == 'my_reports':
            return queryset.filter(reporter=user)

        if tab == 'feed':
            return queryset.exclude(reporter=user).exclude(status='DRAFT')

        return queryset.filter(reporter=user)

    def perform_create(self, serializer):
        user = self.request.user

        if is_admin_account(user):
            raise PermissionDenied('Admin tidak boleh membuat laporan citizen.')

        status = self.request.data.get('status') or 'DRAFT'

        if status not in ['DRAFT', 'REPORTED']:
            status = 'DRAFT'

        serializer.save(reporter=user, status=status)

    def perform_update(self, serializer):
        report = self.get_object()
        user = self.request.user

        if is_admin_account(user):
            new_status = self.request.data.get('status', report.status)

            if new_status == 'DRAFT':
                raise PermissionDenied('Admin tidak boleh mengubah laporan menjadi DRAFT.')

            serializer.save()
            return

        if report.reporter_id != user.id:
            raise PermissionDenied('Kamu tidak boleh mengubah laporan milik user lain.')

        if report.status != 'DRAFT':
            raise PermissionDenied('Citizen hanya boleh mengubah laporan yang masih DRAFT.')

        new_status = self.request.data.get('status', report.status)

        if new_status not in ['DRAFT', 'REPORTED']:
            raise PermissionDenied('Citizen hanya boleh menyimpan DRAFT atau mengajukan REPORTED.')

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if is_admin_account(user):
            instance.delete()
            return

        if instance.reporter_id != user.id:
            raise PermissionDenied('Kamu tidak boleh menghapus laporan milik user lain.')

        if instance.status != 'DRAFT':
            raise PermissionDenied('Citizen hanya boleh menghapus laporan yang masih DRAFT.')

        instance.delete()