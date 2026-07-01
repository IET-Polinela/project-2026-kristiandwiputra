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
        report = Report.objects.create(
            title='Laporan Str Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga,
        )

        self.assertEqual(str(report), 'Laporan Str Uji')

    def test_report_serializer_no_request_context(self):
        """
        Menguji serializer tanpa request sehingga is_owner bernilai False
        dan identitas reporter disamarkan.
        """
        report = Report.objects.create(
            title='Laporan Serializer Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga,
        )

        serializer = ReportSerializer(report, context={})

        self.assertFalse(serializer.data['is_owner'])
        self.assertEqual(serializer.data['reporter'], 'Warga Anonim')


class MainAppMonolithicViewsCoverageTests(TestCase):
    """
    Menguji view monolitik di main_app/views.py sesuai arahan dosen:
    - halaman list/detail/create web admin hanya untuk admin,
    - citizen/anonymous diarahkan,
    - admin tidak boleh edit dan hapus laporan warga,
    - admin hanya boleh memproses status laporan.
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
        request = self.factory.get('/dummy-url/')
        request.user = AnonymousUser()

        response = report_detail_api(request, self.report.id)

        self.assertEqual(response.status_code, 200)

    def test_report_detail_api_invalid(self):
        """
        Detail API menghasilkan Http404 untuk ID yang tidak tersedia.
        """
        request = self.factory.get('/dummy-url/')
        request.user = AnonymousUser()

        with self.assertRaises(Http404):
            report_detail_api(request, 99999)

    def test_report_search_unauthenticated(self):
        """
        Anonymous tidak boleh memakai live search admin.
        """
        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 403)

    def test_report_search_citizen(self):
        """
        Citizen tidak boleh memakai live search admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 403)

    def test_report_search_admin(self):
        """
        Admin boleh memakai live search laporan non-DRAFT.
        """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('report_search_api'), {'q': 'Monolitik'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['reports']), 1)

    def test_home_view(self):
        """
        Halaman home dapat diakses.
        """
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_list_view_unauthenticated(self):
        """
        Anonymous diarahkan ke login saat membuka daftar laporan admin.
        """
        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 302)

    def test_report_list_view_citizen(self):
        """
        Citizen diarahkan karena daftar laporan monolitik hanya untuk admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('report_list'))

        self.assertEqual(response.status_code, 302)

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
        Anonymous diarahkan ke login saat membuka tambah laporan.
        """
        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 302)

    def test_report_create_view_citizen(self):
        """
        Citizen diarahkan karena tambah laporan monolitik hanya untuk admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 302)

    def test_report_create_view_admin_get(self):
        """
        Admin dapat membuka form tambah laporan pada web admin.
        """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('add_report'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/add_report.html')

    def test_report_create_view_admin_post_valid(self):
        """
        Admin dapat membuat laporan melalui form admin.
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
        self.assertTrue(Report.objects.filter(title='Laporan Form Baru').exists())

    def test_report_detail_view_unauthenticated(self):
        """
        Anonymous diarahkan ke login saat membuka detail laporan admin.
        """
        response = self.client.get(
            reverse('report_detail', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_detail_view_citizen(self):
        """
        Citizen diarahkan karena detail laporan monolitik hanya untuk admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('report_detail', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

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
        Anonymous diarahkan ke login saat membuka edit laporan.
        """
        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_update_view_citizen(self):
        """
        Citizen diarahkan karena tidak boleh mengedit melalui web admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_update_view_admin_get_denied(self):
        """
        Admin tidak boleh membuka form edit isi laporan warga.

        Expected:
        HTTP 403 Forbidden.
        """
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('edit_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 403)

    def test_report_update_view_admin_post_denied(self):
        """
        Admin tidak boleh menyimpan perubahan isi laporan warga.

        Expected:
        HTTP 403 Forbidden dan data tidak berubah.
        """
        self.client.force_login(self.admin)
        original_title = self.report.title

        payload = {
            'title': 'Laporan Terupdate Oleh Admin',
            'category': 'Infrastruktur',
            'description': 'Deskripsi terupdate.',
            'location': 'Jakarta',
            'status': 'REPORTED',
        }

        response = self.client.post(
            reverse('edit_report', kwargs={'pk': self.report.id}),
            payload,
        )

        self.assertEqual(response.status_code, 403)

        self.report.refresh_from_db()
        self.assertEqual(self.report.title, original_title)
        self.assertNotEqual(self.report.title, 'Laporan Terupdate Oleh Admin')

    def test_report_delete_view_unauthenticated(self):
        """
        Anonymous diarahkan ke login saat membuka hapus laporan.
        """
        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_delete_view_citizen(self):
        """
        Citizen diarahkan karena tidak boleh menghapus melalui web admin.
        """
        self.client.force_login(self.citizen)

        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_report_delete_view_admin_get_denied(self):
        """
        Admin tidak boleh membuka halaman konfirmasi hapus laporan warga.

        Expected:
        HTTP 403 Forbidden.
        """
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('delete_report', kwargs={'pk': self.report.id})
        )

        self.assertEqual(response.status_code, 403)

    def test_report_delete_view_admin_post_denied(self):
        """
        Admin tidak boleh menghapus laporan warga.

        Expected:
        HTTP 403 Forbidden dan data tetap ada.
        """
        self.client.force_login(self.admin)
        report_id = self.report.id

        response = self.client.post(
            reverse('delete_report', kwargs={'pk': report_id})
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Report.objects.filter(id=report_id).exists())

    def test_report_update_status_view_unauthenticated(self):
        """
        Anonymous tidak dapat memperbarui status laporan.
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