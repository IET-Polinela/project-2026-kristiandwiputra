from django.test import TestCase
from django.urls import reverse

from .models import Report


class MainAppTests(TestCase):
    def test_home_page_is_accessible(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_list_page_is_accessible(self):
        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/report_list.html')

    def test_report_status_updates_in_allowed_order(self):
        report = Report.objects.create(
            title='Lampu Jalan Mati',
            category='Infrastruktur',
            description='Lampu jalan tidak menyala di malam hari.',
            location='Jl. Merdeka',
        )

        response = self.client.post(
            reverse('update_status', args=[report.pk]),
            {'status': 'VERIFIED'},
        )

        report.refresh_from_db()

        self.assertRedirects(response, reverse('report_list'))
        self.assertEqual(report.status, 'VERIFIED')

    def test_report_status_rejects_skipped_transition(self):
        report = Report.objects.create(
            title='Jalan Rusak',
            category='Infrastruktur',
            description='Aspal berlubang cukup dalam.',
            location='Jl. Asia Afrika',
        )

        self.client.post(
            reverse('update_status', args=[report.pk]),
            {'status': 'RESOLVED'},
        )

        report.refresh_from_db()

        self.assertEqual(report.status, 'REPORTED')
