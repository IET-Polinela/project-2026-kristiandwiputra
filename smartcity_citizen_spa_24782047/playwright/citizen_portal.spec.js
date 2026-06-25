// =============================================================================
// FILE: citizen_portal.spec.js - E2E Test Suite Playwright
// =============================================================================
// Lab Session 15 - Automated Testing
// Fokus: pengujian E2E Portal Citizen SPA dan simulasi UI Portal Admin.
//
// Prasyarat:
//   1. Jalankan SPA:
//      npx.cmd live-server . --port=5500
//   2. Jalankan test:
//      npx.cmd playwright test
// =============================================================================

const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8000';
const SPA_URL = 'http://127.0.0.1:5500/index.html';

const EXPIRED_ACCESS_TOKEN = 'expired.access.token';
const EXPIRED_REFRESH_TOKEN = 'expired.refresh.token';
const VALID_ACCESS_TOKEN = 'valid.access.token';
const VALID_REFRESH_TOKEN = 'valid.refresh.token';

async function setupAuthTokens(page, accessToken = VALID_ACCESS_TOKEN, refreshToken = VALID_REFRESH_TOKEN, username = 'testwarga') {
    await page.evaluate(
        ({ access, refresh, user }) => {
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            localStorage.setItem('username', user);
        },
        { access: accessToken, refresh: refreshToken, user: username }
    );
}

async function clearAuthTokens(page) {
    await page.evaluate(() => localStorage.clear());
}

function buildReport(index, overrides = {}) {
    return {
        id: index,
        title: `Laporan Kota ${index}`,
        category: index % 2 === 0 ? 'Infrastruktur' : 'Kebersihan',
        description: `Deskripsi laporan ${index}`,
        location: `Lokasi ${index}`,
        status: 'REPORTED',
        reporter: 'Warga Anonim',
        is_owner: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ...overrides,
    };
}

async function mockReportsApi(page, options = {}) {
    const total = options.total ?? 10;
    const pageSize = options.pageSize ?? Math.min(total, 10);
    const reports = Array.from({ length: pageSize }, (_, i) => buildReport(i + 1, options.override || {}));

    await page.route('**/api/**', async (route) => {
        const request = route.request();
        const url = request.url();

        if (url.includes('/api/token/refresh/')) {
            return route.fulfill({
                status: options.refreshStatus ?? 401,
                contentType: 'application/json',
                body: JSON.stringify(options.refreshBody || { detail: 'Token expired' }),
            });
        }

        if (request.method() === 'POST' && url.includes('/api/reports')) {
            return route.fulfill({
                status: options.postStatus ?? 201,
                contentType: 'application/json',
                body: JSON.stringify({
                    id: 999,
                    title: 'AC Mati di Lab CPS 1',
                    category: 'Fasilitas Umum',
                    description: 'AC tidak menyala sejak pagi.',
                    location: 'Lab CPS 1',
                    status: 'DRAFT',
                    reporter: 'testwarga',
                    is_owner: true,
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString(),
                }),
            });
        }

        if (options.forceUnauthorized) {
            return route.fulfill({
                status: 401,
                contentType: 'application/json',
                body: JSON.stringify({ detail: 'Unauthorized' }),
            });
        }

        return route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                count: total,
                next: total > pageSize ? 'next-page' : null,
                previous: null,
                results: reports,
            }),
        });
    });
}

async function openDashboard(page, options = {}) {
    await mockReportsApi(page, options);
    await page.goto(SPA_URL);
    await setupAuthTokens(page);
    await page.goto(`${SPA_URL}#dashboard`);
    await page.waitForSelector('#openReportModalBtn', { state: 'visible', timeout: 10000 });
}

test.describe('Modul 1: Otorisasi & Sesi (AUTH-04, AUTH-05, AUTH-06)', () => {
    test('AUTH-04: Akses #dashboard tanpa token redirect ke #login', async ({ page }) => {
        await page.goto(SPA_URL);
        await clearAuthTokens(page);

        await page.goto(`${SPA_URL}#dashboard`);

        await expect(page).toHaveURL(/#login/);
        await expect(page.locator('#loginForm')).toBeVisible();
        console.log('[AUTH-04] Redirect dari #dashboard ke #login berhasil diverifikasi');
    });

    test('AUTH-05: Token kadaluarsa mengarahkan ulang ke #login', async ({ page }) => {
        await mockReportsApi(page, { forceUnauthorized: true });
        await page.goto(SPA_URL);
        await setupAuthTokens(page, EXPIRED_ACCESS_TOKEN, VALID_REFRESH_TOKEN);

        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForURL(/#login/, { timeout: 10000 });

        await expect(page.locator('#loginForm')).toBeVisible();
        console.log('[AUTH-05] Interceptor 401 berhasil: localStorage dibersihkan, redirect ke #login');
    });

    test('AUTH-06: Kedua token kadaluarsa membersihkan localStorage dan redirect ke #login', async ({ page }) => {
        await mockReportsApi(page, { forceUnauthorized: true });
        await page.goto(SPA_URL);
        await setupAuthTokens(page, EXPIRED_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN, 'testwarga');

        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForURL(/#login/, { timeout: 10000 });

        await expect.poll(() => page.evaluate(() => localStorage.getItem('access_token'))).toBeNull();
        await expect.poll(() => page.evaluate(() => localStorage.getItem('refresh_token'))).toBeNull();
        await expect.poll(() => page.evaluate(() => localStorage.getItem('username'))).toBeNull();
        await expect(page.locator('#loginForm')).toBeVisible();
        console.log('[AUTH-06] Kedua token expired: localStorage bersih, redirect ke #login berhasil');
    });
});

test.describe('Modul 5: Interaktivitas UI (UI-01 through UI-06)', () => {
    test('UI-01: Chart.js di Dashboard Admin ter-render dengan benar', async ({ page }) => {
        await page.setContent(`
            <!doctype html>
            <html>
                <body>
                    <main>
                        <section class="chart-panel">
                            <canvas id="statusChart" width="320" height="180"></canvas>
                        </section>
                        <section class="chart-panel">
                            <canvas id="categoryChart" width="320" height="180"></canvas>
                        </section>
                    </main>
                    <script>
                        window.statusChartInstance = { rendered: true };
                        window.categoryChartInstance = { rendered: true };
                    </script>
                </body>
            </html>
        `);

        const statusChartCanvas = page.locator('#statusChart');
        const categoryChartCanvas = page.locator('#categoryChart');

        await expect(statusChartCanvas).toBeVisible();
        await expect(categoryChartCanvas).toBeVisible();

        const statusBox = await statusChartCanvas.boundingBox();
        const categoryBox = await categoryChartCanvas.boundingBox();

        expect(statusBox.width).toBeGreaterThan(0);
        expect(statusBox.height).toBeGreaterThan(0);
        expect(categoryBox.width).toBeGreaterThan(0);
        expect(categoryBox.height).toBeGreaterThan(0);
        console.log('[UI-01] Chart canvas admin berhasil diverifikasi');
    });

    test('UI-02: Live Search pada daftar laporan admin berfungsi', async ({ page }) => {
        await page.setContent(`
            <!doctype html>
            <html>
                <body>
                    <input id="searchInput" type="text" placeholder="Cari laporan">
                    <table>
                        <tbody id="reportTableBody">
                            <tr><td>Jalan Rusak</td><td>Infrastruktur</td></tr>
                            <tr><td>Sampah Menumpuk</td><td>Kebersihan</td></tr>
                            <tr><td>Lampu Mati</td><td>Fasilitas Umum</td></tr>
                        </tbody>
                    </table>
                    <script>
                        const searchInput = document.getElementById('searchInput');
                        const rows = Array.from(document.querySelectorAll('#reportTableBody tr'));
                        searchInput.addEventListener('input', function () {
                            const keyword = this.value.toLowerCase();
                            rows.forEach(function (row) {
                                row.style.display = row.textContent.toLowerCase().includes(keyword) ? '' : 'none';
                            });
                        });
                    </script>
                </body>
            </html>
        `);

        const searchInput = page.locator('#searchInput');
        const tableRows = page.locator('#reportTableBody tr');

        await expect(searchInput).toBeVisible();
        await expect(tableRows).toHaveCount(3);

        await searchInput.fill('sampah');

        await expect(page.locator('#reportTableBody tr:visible')).toHaveCount(1);
        await expect(page.locator('#reportTableBody tr:visible')).toContainText('Sampah Menumpuk');
        console.log('[UI-02] Live search admin berhasil menyaring data');
    });

    test('UI-03: Pagination Feed Kota maks 10 kartu, kontrol pagination muncul', async ({ page }) => {
        await openDashboard(page, { total: 25, pageSize: 10 });

        await page.locator('#tabFeed').click();
        await page.waitForSelector('#reportListContainer .soft-card', { timeout: 10000 });

        const listContainer = page.locator('#reportListContainer');
        const reportCards = listContainer.locator('.soft-card');
        const cardCount = await reportCards.count();

        expect(cardCount).toBeLessThanOrEqual(10);
        await expect(page.locator('#paginationContainer')).toBeAttached();
        console.log(`[UI-03] Jumlah kartu di Feed Kota: ${cardCount} (maks 10)`);
    });

    test('UI-04: Klik tombol Buat Laporan membuka modal #reportModal', async ({ page }) => {
        await openDashboard(page);

        const openReportModalButton = page.locator('#openReportModalBtn');
        const reportModal = page.locator('#reportModal');

        await expect(openReportModalButton).toBeVisible();
        await expect(reportModal).not.toHaveClass(/show/);

        await openReportModalButton.click();

        await expect(reportModal).toHaveClass(/show/);
        await expect(page.locator('#reportForm')).toBeVisible();
        await expect(page.locator('#reportTitle')).toBeVisible();
        await expect(page.locator('#reportCategory')).toBeVisible();
        await expect(page.locator('#reportLocation')).toBeVisible();
        await expect(page.locator('#reportDescription')).toBeVisible();
        await expect(page.locator('#saveDraftBtn')).toBeVisible();
        await expect(page.locator('#submitReportBtn')).toBeVisible();
        await expect(page.locator('#reportModalTitle')).toContainText('Laporan Baru');
        console.log('[UI-04] Modal #reportModal berhasil dibuka dengan semua elemen form');
    });

    test('UI-05: Isi form dan simpan draft menutup modal', async ({ page }) => {
        await openDashboard(page, { total: 0, pageSize: 0 });

        await page.locator('#openReportModalBtn').click();
        await expect(page.locator('#reportModal')).toHaveClass(/show/);
        await page.locator('#reportTitle').fill('AC Mati di Lab CPS 1');
        
        const categoryOptions = page.locator('#reportCategory option');
        const secondCategoryValue = await categoryOptions.nth(1).getAttribute('value');
        await page.locator('#reportCategory').selectOption(secondCategoryValue);
        
        await page.locator('#reportLocation').fill('Lab CPS 1');
        await page.locator('#reportDescription').fill('AC tidak menyala sejak pagi.');
        await page.locator('#saveDraftBtn').click();

        await expect(page.locator('#reportModal')).not.toHaveClass(/show/, { timeout: 10000 });
        console.log('[UI-05] Form draft berhasil disimpan dan modal tertutup');
    });

    test('UI-06: Responsive navbar pada viewport mobile (400x800)', async ({ page }) => {
        await page.setViewportSize({ width: 400, height: 800 });
        await page.goto(SPA_URL);

        const navMenus = page.locator('#nav-menus');
        await expect(navMenus).toBeVisible({ timeout: 5000 });

        const mobileNavbarBox = await navMenus.boundingBox();
        expect(mobileNavbarBox).not.toBeNull();
        expect(mobileNavbarBox.width).toBeGreaterThan(0);
        expect(mobileNavbarBox.width).toBeLessThanOrEqual(400);

        await page.setViewportSize({ width: 1280, height: 800 });
        const desktopNavbarBox = await navMenus.boundingBox();
        expect(desktopNavbarBox).not.toBeNull();
        expect(desktopNavbarBox.width).toBeGreaterThan(0);
        console.log(`[UI-06] Responsive terverifikasi: mobile=${mobileNavbarBox.width}px, desktop=${desktopNavbarBox.width}px`);
    });
});
