from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import Report
from main_app.serializers import ReportSerializer
from main_app.views import report_detail_api


# ─────────────────────────────────────────────────────────────────────────────
# PENJELASAN: get_user_model()
# ─────────────────────────────────────────────────────────────────────────────
# Django mendukung custom user model melalui setting AUTH_USER_MODEL.
# Menggunakan get_user_model() memastikan test memakai model user proyek.
# ─────────────────────────────────────────────────────────────────────────────
User = get_user_model()


# =============================================================================
# ADDITIONAL TESTS FOR STATEMENT COVERAGE
# =============================================================================

class SerializerAndModelCoverageTests(APITestCase):
    """
    Kelas pengujian tambahan untuk menaikkan coverage model dan serializer.
    """

    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_str_test',
            password='Password123!',
            is_admin=False,
        )

    def test_report_model_str(self):
        """
        Menguji str(report) agar memanggil __str__ dan mengembalikan judul.
        """
        # Arrange
        report = Report.objects.create(
            title='Laporan Str Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga,
        )

        # Act dan Assert
        self.assertEqual(str(report), 'Laporan Str Uji')

    def test_report_serializer_no_request_context(self):
        """
        Menguji serializer tanpa request sehingga is_owner bernilai False
        dan identitas reporter disamarkan.
        """
        # Arrange
        report = Report.objects.create(
            title='Laporan Serializer Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga,
        )

        # Act
        serializer = ReportSerializer(report, context={})

        # Assert
        self.assertFalse(serializer.data['is_owner'])
        self.assertEqual(serializer.data['reporter'], 'Warga Anonim')


class MainAppMonolithicViewsCoverageTests(TestCase):
    """
    Menguji view monolitik di main_app/views.py berdasarkan route dan
    perilaku aplikasi yang benar-benar tersedia.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User.objects.create_user(
            username='admin_mono',
            password='Password123!',
            is_admin=True,
            is_staff=True,
        )
        self.citizen = User.objects.create_user(
            username='citizen_mono',
            password='Password123!',
            is_admin=False,
            is_staff=False,
        )
        self.report = Report.objects.create(
            title='Laporan Monolitik Uji',
            category='Infrastruktur',
            description='Ada kerusakan infrastruktur.',
            location='Bandung',
            status='REPORTED',
            reporter=self.citizen,
        )

    def test_report_detail_api_valid(self):
        """
        Detail API mengembalikan HTTP 200 untuk laporan publik yang tersedia.
        """
        # Arrange
        request = self.factory.get('/dummy-url/')
        request.user = AnonymousUser()

        # Act
        response = report_detail_api(request, self.report.id)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_report_detail_api_invalid(self):
        """
        Detail API menghasilkan Http404 untuk ID yang tidak tersedia.
        """
        # Arrange
        request = self.factory.get('/dummy-url/')
        request.user = AnonymousUser()

        # Act dan Assert
        with self.assertRaises(Http404):
            report_detail_api(request, 99999)

    def test_report_search_unauthenticated(self):
        """
        Live search dapat membaca laporan publik tanpa autentikasi.
        """
        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['reports']), 1)

    def test_report_search_citizen(self):
        """
        Citizen dapat memakai live search untuk laporan yang terlihat baginya.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['reports']), 1)

    def test_report_search_admin(self):
        """
        Admin dapat memakai live search untuk laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['reports']), 1)

    def test_home_view(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_list_view_unauthenticated(self):
        """
        Daftar laporan publik dapat dibuka tanpa autentikasi.
        """
        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/report_list.html')

    def test_report_list_view_citizen(self):
        """
        Citizen dapat membuka daftar laporan yang terlihat baginya.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 200)

    def test_report_list_view_admin(self):
        """
        Admin dapat membuka daftar laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/report_list.html')

    def test_report_create_view_unauthenticated(self):
        """
        View tambah laporan mengarahkan pengguna ke daftar laporan.
        """
        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report_list'))

    def test_report_create_view_citizen(self):
        """
        Citizen diarahkan ke portal citizen untuk membuat laporan.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report_list'))

    def test_report_create_view_admin(self):
        """
        Admin juga tidak membuat laporan citizen melalui view monolitik.
        """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report_list'))

    def test_report_create_post_does_not_create_report(self):
        """
        POST ke view monolitik tetap diarahkan dan tidak membuat laporan.
        """
        self.client.force_login(self.admin)
        payload = {
            'title': 'Laporan Form Baru',
            'category': 'Infrastruktur',
            'description': 'Deskripsi baru.',
            'location': 'Jakarta',
            'status': 'DRAFT',
        }

        response = self.client.post(reverse('add_report'), payload)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Report.objects.filter(title='Laporan Form Baru').exists())

    def test_report_detail_view_unauthenticated(self):
        """
        Detail laporan publik dapat dilihat tanpa autentikasi.
        """
        response = self.client.get(
            reverse('report_detail', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_detail_view_citizen(self):
        """
        Citizen dapat melihat detail laporan publik.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('report_detail', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_detail_view_admin(self):
        """
        Admin dapat melihat detail laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('report_detail', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_update_view_unauthenticated(self):
        """
        Pengguna anonim diarahkan ke login saat membuka edit laporan.
        """
        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_update_view_citizen(self):
        """
        Citizen tidak memperoleh objek melalui view edit admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_report_update_view_admin_get(self):
        """
        Admin dapat membuka form edit laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_update_view_admin_post_valid(self):
        """
        Admin dapat menyimpan perubahan melalui form edit.
        """
        self.client.force_login(self.admin)
        payload = {
            'title': 'Laporan Terupdate',
            'category': 'Infrastruktur',
            'description': 'Deskripsi terupdate.',
            'location': 'Jakarta',
            'status': 'REPORTED',
        }

        response = self.client.post(
            reverse('edit_report', kwargs={'pk': self.report.id}),
            payload,
        )

        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.title, 'Laporan Terupdate')

    def test_report_delete_view_unauthenticated(self):
        """
        Pengguna anonim diarahkan ke login saat membuka hapus laporan.
        """
        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_delete_view_citizen(self):
        """
        Citizen tidak memperoleh objek melalui view hapus admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_report_delete_view_admin_get(self):
        """
        Admin dapat membuka halaman konfirmasi penghapusan.
        """
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_delete_view_admin_post(self):
        """
        Admin dapat menghapus laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Report.objects.filter(id=self.report.id).exists())

    def test_report_update_status_view_unauthenticated(self):
        """
        Pengguna anonim tidak dapat memperbarui status laporan.
        """
        response = self.client.post(
            reverse('update_status', kwargs={'pk': self.report.id}),
            {'status': 'VERIFIED'},
        )

        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'REPORTED')

    def test_report_update_status_view_citizen(self):
        """
        Citizen tidak dapat memperbarui status laporan.
        """
        self.client.force_login(self.citizen)

        response = self.client.post(
            reverse('update_status', kwargs={'pk': self.report.id}),
            {'status': 'VERIFIED'},
        )

        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'REPORTED')
