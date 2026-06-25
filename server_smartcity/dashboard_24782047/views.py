from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from main_app.models import Report


def is_admin_dashboard_user(user):
    return user.is_authenticated and (
        user.is_superuser or user.is_staff or getattr(user, 'is_admin', False)
    )


class DashboardView(TemplateView):
    template_name = 'dashboard_24782047/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_admin_dashboard_user(request.user):
            messages.error(request, 'Akses ditolak.')
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_reports'] = Report.objects.count()
        context['reported_count'] = Report.objects.filter(status='REPORTED').count()
        context['resolved_count'] = Report.objects.filter(status='RESOLVED').count()

        context['latest_reported'] = Report.objects.filter(
            status='REPORTED'
        ).order_by('-id')[:5]

        context['latest_resolved'] = Report.objects.filter(
            status='RESOLVED'
        ).order_by('-id')[:5]

        return context


def dashboard_stats_api(request):
    if not is_admin_dashboard_user(request.user):
        messages.error(request, 'Akses ditolak.')
        return JsonResponse({'detail': 'Akses ditolak.'}, status=403)

    status_data = (
        Report.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )

    category_data = (
        Report.objects.values('category')
        .annotate(total=Count('id'))
        .order_by('category')
    )

    status_labels = [item['status'] for item in status_data]
    status_totals = [item['total'] for item in status_data]

    category_labels = [item['category'] for item in category_data]
    category_totals = [item['total'] for item in category_data]

    return JsonResponse({
        'status_labels': status_labels,
        'status_totals': status_totals,
        'category_labels': category_labels,
        'category_totals': category_totals,
    })