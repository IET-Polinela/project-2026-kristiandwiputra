const routes = {
    '#login': `
        <div class="row justify-content-center align-items-center mt-5">
            <div class="col-md-5 col-lg-4">
                <div class="card border-0 rounded-4 overflow-hidden shadow-lg" style="background-color: #0b1120; border: 1px solid #1e293b !important;">
                    <div class="p-4 text-center" style="border-bottom: 1px solid #1e293b;">
                        <i class="bi bi-shield-lock-fill display-4 mb-2" style="color: #0ea5e9;"></i>
                        <h4 class="fw-bold mb-0 text-white">SYSTEM_LOGIN</h4>
                        <p class="small mb-0" style="color: #eab308; font-family: monospace;">> KOTA_LAMPUNG : SECURE_CORE</p>
                    </div>
                    <div class="card-body p-4 p-sm-5">
                        <form id="loginForm">
                            <div class="mb-3">
                                <label class="form-label" style="color: #94a3b8; font-family: monospace; font-size: 0.9rem;"><i class="bi bi-person-fill me-2"></i>_Username</label>
                                <input type="text" id="loginUsername" class="form-control" style="background-color: #0f172a; border: 1px solid #334155; color: #0ea5e9;" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label" style="color: #94a3b8; font-family: monospace; font-size: 0.9rem;"><i class="bi bi-key-fill me-2"></i>_Password</label>
                                <input type="password" id="loginPassword" class="form-control" style="background-color: #0f172a; border: 1px solid #334155; color: #0ea5e9;" required>
                            </div>
                            <button type="submit" class="btn w-100 fw-bold rounded-2 mt-3" style="background-color: transparent; border: 1px solid #0ea5e9; color: #0ea5e9; transition: 0.3s;" onmouseover="this.style.backgroundColor='#0ea5e9'; this.style.color='#0b1120';" onmouseout="this.style.backgroundColor='transparent'; this.style.color='#0ea5e9';">
                                <i class="bi bi-box-arrow-in-right me-2"></i>AUTHENTICATE
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-lg rounded-4 overflow-hidden" style="background-color: #0b1120; border: 1px solid #1e293b !important;">
                    <div class="card-body p-4 p-md-5 d-flex align-items-center justify-content-between">
                        <div>
                            <p class="mb-2" style="color: #eab308; font-family: monospace; font-size: 0.85rem;">> SYSTEM.INIT_SUCCESS: SECURE_CORE_CONNECTED</p>
                            <h2 class="fw-bold mb-1 text-white" style="letter-spacing: 1px;">BANDAR-LAMPUNG <span style="color: #0ea5e9; font-weight: normal;">SmartGrid</span></h2>
                            <p class="mb-0 mt-2" style="color: #94a3b8; font-family: monospace; font-size: 0.85rem;">[NODE]: CITIZEN_PORTAL | [STATUS]: <span class="text-success">ONLINE</span></p>
                        </div>
                        <i class="bi bi-cpu opacity-50 d-none d-md-block" style="font-size: 5rem; color: #0ea5e9;"></i>
                    </div>
                </div>
            </div>
        </div>

        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-4 shadow-lg rounded-4 sticky-top" style="background-color: #0b1120; border: 1px solid #1e293b !important; top: 20px;">
                    <h6 class="fw-bold mb-4 text-uppercase" style="letter-spacing: 1px; font-size: 0.85rem; color: #94a3b8; font-family: monospace;">> _Command_Center</h6>
                    <button class="btn btn-lg w-100 fw-bold mb-3 rounded-2 shadow-sm d-flex align-items-center justify-content-center" style="background-color: #0ea5e9; color: #0b1120; border: none;">
                        <i class="bi bi-plus-square-fill me-2"></i>Laporan Baru
                    </button>
                    <button class="btn w-100 fw-bold rounded-2 d-flex align-items-center justify-content-center" style="background-color: transparent; border: 1px solid #eab308; color: #eab308; transition: 0.3s; padding: 10px 0;" onmouseover="this.style.backgroundColor='#eab308'; this.style.color='#0b1120';" onmouseout="this.style.backgroundColor='transparent'; this.style.color='#eab308';">
                        <i class="bi bi-database me-2"></i>Riwayat Data
                    </button>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card border-0 p-5 shadow-lg text-center rounded-4 h-100 d-flex flex-column justify-content-center align-items-center" style="background-color: #0b1120; border: 1px solid rgba(14, 165, 233, 0.5) !important; box-shadow: inset 0 0 20px rgba(14, 165, 233, 0.05), 0 0 15px rgba(14, 165, 233, 0.1) !important;">
                    <div class="p-4 rounded-circle mb-4 d-flex align-items-center justify-content-center" style="background-color: rgba(14, 165, 233, 0.1); width: 100px; height: 100px;">
                        <i class="bi bi-hdd-network" style="font-size: 3rem; color: #0ea5e9;"></i>
                    </div>
                    <h4 class="fw-bold text-white mb-2" style="font-family: monospace;">_Data_Stream_Empty</h4>
                    <p class="small w-75 mb-0 mt-2" style="color: #94a3b8; line-height: 1.6;">Koneksi API untuk menarik data laporan secara real-time dari backend Django akan diimplementasikan pada Lab 12.</p>
                </div>
            </section>

            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card border-0 shadow-lg rounded-4 sticky-top overflow-hidden" style="background-color: #0b1120; border: 1px solid rgba(16, 185, 129, 0.5) !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.1) !important; top: 20px;">
                    <div class="p-3 d-flex align-items-center" style="border-bottom: 1px solid #1e293b;">
                        <i class="bi bi-shield-check me-2" style="color: #10b981; font-size: 1.2rem;"></i>
                        <h6 class="fw-bold mb-0 text-white" style="font-family: monospace;">_Sec_Gateway</h6>
                    </div>
                    <div class="card-body p-4">
                        
                        <div class="d-flex align-items-start mb-4">
                            <i class="bi bi-activity mt-1 me-3" style="color: #10b981; font-size: 1.2rem;"></i>
                            <div>
                                <h6 class="mb-1 fw-bold text-white" style="font-family: monospace; font-size: 0.9rem;">Secure_Status</h6>
                                <p class="mb-0" style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">0 Anomali Jaringan terdeteksi dalam 24 Jam terakhir.</p>
                            </div>
                        </div>

                        <div class="d-flex align-items-start">
                            <i class="bi bi-cpu-fill mt-1 me-3" style="color: #0ea5e9; font-size: 1.2rem;"></i>
                            <div>
                                <h6 class="mb-1 fw-bold text-white" style="font-family: monospace; font-size: 0.9rem;">Active_Nodes</h6>
                                <p class="mb-0" style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">2,408 ESP32 & Sensor Terhubung ke SmartGrid.</p>
                            </div>
                        </div>

                    </div>
                </div>
            </aside>
        </div>
    `
};

function handleRouting() {
    const hash = window.location.hash || '#login'; 
    document.getElementById('app-content').innerHTML = routes[hash] || routes['#login'];
    
    // Ubah warna latar belakang utama halaman secara dinamis
    document.body.style.backgroundColor = '#0f172a';
    
    // Modifikasi Navbar bawaan index.html agar menjadi Dark Mode
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.classList.remove('bg-primary');
        navbar.style.backgroundColor = '#0b1120';
        navbar.style.borderBottom = '1px solid #1e293b';
        const brand = navbar.querySelector('.navbar-brand');
        if (brand) brand.style.color = '#f8fafc';
    }

    // Jalankan fungsi login jika sedang di halaman login
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);