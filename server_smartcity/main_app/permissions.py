from rest_framework import permissions

class IsCitizen(permissions.BasePermission):
    """
    Satpam 1: Hanya mengizinkan Citizen (Warga) untuk membuat laporan (POST).
    Admin dilarang.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_superuser)


class AdvancedReportAccessPolicy(permissions.BasePermission):
    """
    Satpam 2: Aturan Edit (PUT) & Delete (DELETE) level Objek.
    """
    def has_object_permission(self, request, view, obj):
        # 1. Izinkan akses untuk sekadar melihat data (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. Aturan Khusus ADMIN / SUPERUSER
        if request.user.is_superuser:
            if request.method in ['PUT', 'PATCH']:
                return True # Admin BOLEH Edit (nanti dibatasi cuma edit status di api_views)
            return False    # Admin DILARANG Delete

        # 3. Aturan Khusus CITIZEN / WARGA
        # BLOKIR PERTAMA: Cek apakah Citizen ini pemilik asli laporan?
        # (Kita gunakan ID untuk memastikan kecocokan mutlak)
        if obj.reporter.id != request.user.id:
            return False # LANGSUNG TOLAK (403) jika mencoba mengedit milik orang lain
        
        # BLOKIR KEDUA: Jika dia pemiliknya, apakah statusnya masih DRAFT?
        if obj.status != 'DRAFT':
            return False # LANGSUNG TOLAK (403) jika status sudah diverifikasi

        # Jika lolos semua ujian di atas (Pemilik Asli & Masih DRAFT), izinkan!
        return True