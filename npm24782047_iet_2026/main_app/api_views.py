from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer
# Import 2 satpam baru kita
from .permissions import IsCitizen, AdvancedReportAccessPolicy

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        Logika Aturan 'List & Detail' (Baris 5-8 di fotomu)
        """
        user = self.request.user
        
        # 1. Admin ==> exclude DRAFT (Ditambah order_by agar yang terbaru di atas)
        if user.is_superuser:
            return Report.objects.exclude(status='DRAFT').order_by('-id')
        
        # 2. Citizen ==> Admin (exclude DRAFT) + Report milik sendiri (DRAFT)
        # Menggunakan logika OR (|) (Ditambah order_by agar yang terbaru di atas)
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT')).order_by('-id')

    def get_permissions(self):
        """
        Logika Aturan 'Create, Edit, Delete' (Baris 10-16 di fotomu)
        """
        # Aturan CREATE: Hanya Citizen
        if self.action == 'create':
            return [IsCitizen()]
            
        # Aturan EDIT & DELETE: Gunakan Satpam 2 (AdvancedReportAccessPolicy)
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), AdvancedReportAccessPolicy()]
        
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Otomatis isi pelapor dengan user JWT, 
        dan PAKSA status awal menjadi DRAFT sesuai aturan RBAC.
        """
        serializer.save(reporter=self.request.user, status='DRAFT')

    def perform_update(self, serializer):
        """
        Aturan Khusus: Admin ==> cuma ngubah status aja (Baris 14 di fotomu).
        Mencegah Admin mengutak-atik judul atau deskripsi.
        """
        if self.request.user.is_superuser:
            # Kita paksa ambil data 'status' saja dari request.
            # Field lain akan diabaikan.
            new_status = self.request.data.get('status', serializer.instance.status)
            serializer.save(status=new_status)
        else:
            # Jika citizen yang edit, simpan normal (semua field)
            serializer.save()