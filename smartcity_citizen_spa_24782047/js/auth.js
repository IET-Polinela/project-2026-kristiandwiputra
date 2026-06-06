function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');

    if (!loginForm) return;

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        const submitButton = loginForm.querySelector('button[type="submit"]');

        if (!username || !password) {
            alert('Username dan password harus diisi.');
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Memproses...';
        }

        try {
            const response = await requestAPI('/api/token/', 'POST', {
                username,
                password
            });

            if (response.ok) {
                const data = await response.json();

                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                window.location.hash = '#dashboard';
                return;
            }

            alert('Login gagal. Periksa kembali username dan password.');
        } catch (error) {
            alert('Tidak dapat terhubung ke server Django.');
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Masuk';
            }
        }
    });
}