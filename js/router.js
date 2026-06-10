const routes = {
    '#login': `
        <div class="row justify-content-center align-items-center" style="min-height: calc(100vh - 160px);">
            <div class="col-md-6 col-lg-4">
                <div class="page-card p-4 p-sm-5">
                    <div class="text-center mb-4">
                        <div class="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-4" style="width: 66px; height: 66px; background: var(--primary-soft); color: var(--primary);">
                            <i class="bi bi-person-lock fs-2"></i>
                        </div>

                        <h4 class="fw-bold mb-1 text-main">Masuk Portal Warga</h4>
                        <p class="small mb-0 text-muted-custom">
                            Silakan masuk untuk mengakses dashboard laporan.
                        </p>
                    </div>

                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-main">Username</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="bi bi-person"></i>
                                </span>
                                <input type="text" id="loginUsername" class="form-control" placeholder="Masukkan username" required>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="form-label fw-semibold text-main">Password</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="bi bi-lock"></i>
                                </span>
                                <input type="password" id="loginPassword" class="form-control" placeholder="Masukkan password" required>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary-custom w-100">
                            <i class="bi bi-box-arrow-in-right me-2"></i>
                            Masuk
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `,

    '#dashboard': `
        <section class="page-card p-4 p-lg-5 mb-4">
            <div class="row align-items-center g-4">
                <div class="col-lg-8">
                    <div class="section-label">
                        <i class="bi bi-broadcast-pin"></i>
                        Portal Layanan Warga
                    </div>

                    <h1 class="page-title">Smart City Tracker</h1>

                    <p class="page-desc">
                        Pantau, kirim, dan kelola laporan warga secara langsung dari portal SPA yang terhubung ke backend Django.
                    </p>
                </div>

                <div class="col-lg-4">
                    <div class="row g-3">
                        <div class="col-6">
                            <div class="soft-card p-3 h-100">
                                <div class="small fw-bold text-soft mb-1">Status Sistem</div>
                                <div class="fw-bold text-main">
                                    <i class="bi bi-check-circle-fill me-1" style="color: var(--success);"></i>
                                    Aktif
                                </div>
                            </div>
                        </div>

                        <div class="col-6">
                            <div class="soft-card p-3 h-100">
                                <div class="small fw-bold text-soft mb-1">Mode Akses</div>
                                <div class="fw-bold text-main">Warga</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <div class="row g-4">
            <aside class="col-12 col-lg-3">
    <div class="page-card p-4">
        <h6 class="fw-bold mb-3 text-main">
            <i class="bi bi-bar-chart me-2 text-primary"></i>
            Rekap Laporan
        </h6>

        <div class="soft-card p-3 mb-3" style="background: var(--primary-soft);">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="small fw-bold text-soft mb-1">Total Laporan</div>
                    <div class="h3 fw-bold mb-0 text-main" id="summaryTotal">0</div>
                </div>
                <div class="rounded-3 d-flex align-items-center justify-content-center" style="width: 42px; height: 42px; background: var(--card-bg); color: var(--primary);">
                    <i class="bi bi-file-earmark-text"></i>
                </div>
            </div>
            <div style="height: 6px; background: var(--card-bg); border-radius: 999px;">
                <div style="height: 6px; width: 100%; background: var(--primary); border-radius: 999px;"></div>
            </div>
        </div>

        <div class="soft-card p-3 mb-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="small fw-bold text-soft mb-1">Draft</div>
                    <div class="h4 fw-bold mb-0 text-main" id="summaryDraft">0</div>
                </div>
                <div class="rounded-3 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; background: rgba(100, 116, 139, 0.12); color: #64748b;">
                    <i class="bi bi-pencil-square"></i>
                </div>
            </div>
            <div style="height: 6px; background: var(--card-bg); border-radius: 999px;">
                <div id="lineDraft" style="height: 6px; width: 0%; background: #64748b; border-radius: 999px;"></div>
            </div>
        </div>

        <div class="soft-card p-3 mb-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="small fw-bold text-soft mb-1">Diajukan</div>
                    <div class="h4 fw-bold mb-0" style="color: var(--primary);" id="summaryReported">0</div>
                </div>
                <div class="rounded-3 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; background: var(--primary-soft); color: var(--primary);">
                    <i class="bi bi-send"></i>
                </div>
            </div>
            <div style="height: 6px; background: var(--card-bg); border-radius: 999px;">
                <div id="lineReported" style="height: 6px; width: 0%; background: var(--primary); border-radius: 999px;"></div>
            </div>
        </div>

        <div class="soft-card p-3 mb-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="small fw-bold text-soft mb-1">Diproses</div>
                    <div class="h4 fw-bold mb-0" style="color: #f59e0b;" id="summaryProgress">0</div>
                </div>
                <div class="rounded-3 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; background: rgba(245, 158, 11, 0.14); color: #f59e0b;">
                    <i class="bi bi-hourglass-split"></i>
                </div>
            </div>
            <div style="height: 6px; background: var(--card-bg); border-radius: 999px;">
                <div id="lineProgress" style="height: 6px; width: 0%; background: #f59e0b; border-radius: 999px;"></div>
            </div>
        </div>

        <div class="soft-card p-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="small fw-bold text-soft mb-1">Selesai</div>
                    <div class="h4 fw-bold mb-0" style="color: var(--success);" id="summaryResolved">0</div>
                </div>
                <div class="rounded-3 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; background: rgba(22, 163, 74, 0.12); color: var(--success);">
                    <i class="bi bi-check-circle"></i>
                </div>
            </div>
            <div style="height: 6px; background: var(--card-bg); border-radius: 999px;">
                <div id="lineResolved" style="height: 6px; width: 0%; background: var(--success); border-radius: 999px;"></div>
            </div>
        </div>
    </div>
</aside>
            <section class="col-12 col-lg-9">
                <div class="page-card p-4">
                    <div class="soft-card p-3 p-md-4 mb-4">
                        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
                            <div>
                                <div class="small fw-bold mb-1" style="color: var(--primary);">
                                    <i class="bi bi-plus-circle me-1"></i>
                                    Aksi Cepat
                                </div>
                                <h5 class="fw-bold mb-1 text-main">Buat Laporan Baru</h5>
                                <p class="small mb-0 text-muted-custom">
                                    Buat laporan warga, simpan sebagai draft, atau langsung ajukan ke sistem.
                                </p>
                            </div>

                            <div class="d-flex gap-2 flex-wrap">
                                <button type="button" id="openReportModalBtn" class="btn btn-primary-custom">
                                    <i class="bi bi-plus-circle me-2"></i>
                                    Laporan Baru
                                </button>

                                <button type="button" id="reloadDashboardBtn" class="btn btn-soft">
                                    <i class="bi bi-arrow-clockwise me-2"></i>
                                    Muat Ulang
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                        <div>
                            <h5 class="fw-bold mb-1 text-main">Linimasa Laporan</h5>
                            <p class="small mb-0 text-muted-custom">
                                Geser ke kanan atau kiri untuk melihat kartu laporan lainnya.
                            </p>
                        </div>

                        <div class="d-flex gap-2 flex-wrap">
                            <button type="button" class="btn btn-primary-custom dashboard-tab" id="tabMyReports" data-tab="my_reports">
                                <i class="bi bi-person-lines-fill me-1"></i>
                                Laporan Saya
                            </button>

                            <button type="button" class="btn btn-soft dashboard-tab" id="tabFeed" data-tab="feed">
                                <i class="bi bi-globe2 me-1"></i>
                                Feed Kota
                            </button>
                        </div>
                    </div>

                    <div id="reportListContainer" class="d-flex flex-nowrap overflow-auto gap-3 pb-3">
                        <div class="soft-card p-4 text-center flex-shrink-0" style="width: 340px;">
                            <div class="fw-bold text-main mb-1">Memuat data laporan...</div>
                            <div class="small text-muted-custom">Data akan ditarik dari backend Django.</div>
                        </div>
                    </div>

                    <div id="paginationContainer" class="d-flex justify-content-center align-items-center gap-2 flex-wrap mt-4"></div>
                </div>
            </section>
        </div>
    `
};

function isLoggedIn() {
    return Boolean(localStorage.getItem('access_token'));
}

function logoutCitizen() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    renderNavMenus();
    window.location.hash = '#login';
}

function renderNavMenus() {
    const navMenus = document.getElementById('nav-menus');

    if (!navMenus) return;

    if (isLoggedIn()) {
        navMenus.innerHTML = `
            <button type="button" class="btn btn-sm" onclick="logoutCitizen()" style="background: rgba(220, 38, 38, 0.10); border: 1px solid rgba(220, 38, 38, 0.25); color: var(--danger); border-radius: 12px; font-weight: 750;">
                <i class="bi bi-box-arrow-right me-1"></i>
                Keluar
            </button>
        `;
        return;
    }

    navMenus.innerHTML = `
        <a href="#login" class="btn btn-sm btn-primary-custom">
            <i class="bi bi-box-arrow-in-right me-1"></i>
            Masuk
        </a>
    `;
}

function handleRouting() {
    let hash = window.location.hash;

    if (!hash) {
        hash = isLoggedIn() ? '#dashboard' : '#login';
        window.location.hash = hash;
        return;
    }

    const content = document.getElementById('app-content');

    if (!content) return;

    if (hash === '#dashboard' && !isLoggedIn()) {
        window.location.hash = '#login';
        return;
    }

    content.innerHTML = routes[hash] || routes['#login'];
    renderNavMenus();

    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }

    if (hash === '#dashboard' && typeof initDashboardPage === 'function') {
        initDashboardPage();
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);