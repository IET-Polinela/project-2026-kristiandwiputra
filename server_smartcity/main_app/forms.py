from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Report
# Import CustomUser dari app usermanagement kamu
from usermanagement_24782047.models import CustomUser 

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # PERBAIKAN: Tambahkan 'status' agar bisa diubah saat edit
        fields = ['title', 'category', 'description', 'location', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Masukkan judul laporan'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan kategori laporan'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Masukkan deskripsi laporan'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan lokasi laporan'
            }),
            # Tambahkan widget select untuk status
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields