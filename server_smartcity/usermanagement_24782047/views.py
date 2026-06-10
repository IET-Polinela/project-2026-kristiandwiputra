from django.contrib import messages
from django.contrib.auth import login # Tambahkan ini jika ingin login otomatis setelah daftar
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    # Jika user sudah login, mereka akan langsung dilempar ke report_list tanpa melihat form login lagi
    redirect_authenticated_user = True 

    def form_valid(self, form):
        messages.success(self.request, f'Selamat datang kembali, {form.get_user().username}!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('report_list')


class CustomLogoutView(LogoutView):
    # Di Django 5.0+, logout sebaiknya dilakukan via POST untuk keamanan
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'GET':
            messages.info(request, 'Anda telah berhasil logout.')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    # Jika sudah login, tidak boleh buka halaman register
    if request.user.is_authenticated:
        return redirect('report_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opsional: Jika ingin user langsung login setelah daftar, aktifkan baris di bawah:
            # login(request, user)
            messages.success(request, 'Registrasi berhasil! Silakan gunakan akun Anda untuk login.')
            return redirect('login')
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa kembali data Anda.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})