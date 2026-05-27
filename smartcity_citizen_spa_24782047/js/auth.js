function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    
    // Pastikan form ada di halaman saat ini
    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(event) {
        // Wajib: Mencegah halaman web reload otomatis
        event.preventDefault(); 

        // Ambil nilai dari inputan form
        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        const payload = {
            username: usernameInput,
            password: passwordInput
        };

        try {
            // Gunakan requestAPI dari api.js untuk tembak endpoint login Django
            const response = await requestAPI('/api/token/', 'POST', payload);

            if (response.status === 200) {
                const data = await response.json();
                
                // Simpan token JWT ke memori browser (localStorage)
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                
                alert('Login Berhasil!');
                
                // Pindah halaman ke Dashboard secara instan
                window.location.hash = '#dashboard';
            } else {
                alert('Login Gagal! Username atau password salah.');
            }
        } catch (error) {
            alert('Gagal terhubung ke Server Django.');
        }
    });
}