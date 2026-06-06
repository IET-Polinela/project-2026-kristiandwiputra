let currentTab = 'my_reports';
let currentPage = 1;
let editingReportId = null;

function initDashboardPage() {
    const tabMyReports = document.getElementById('tabMyReports');
    const tabFeed = document.getElementById('tabFeed');
    const reloadButton = document.getElementById('reloadDashboardBtn');
    const openModalButton = document.getElementById('openReportModalBtn');

    if (tabMyReports) {
        tabMyReports.onclick = function () {
            currentTab = 'my_reports';
            currentPage = 1;
            setActiveTab();
            loadDashboardData(currentTab, currentPage);
        };
    }

    if (tabFeed) {
        tabFeed.onclick = function () {
            currentTab = 'feed';
            currentPage = 1;
            setActiveTab();
            loadDashboardData(currentTab, currentPage);
        };
    }

    if (reloadButton) {
        reloadButton.onclick = function () {
            loadDashboardData(currentTab, currentPage);
        };
    }

    if (openModalButton) {
        openModalButton.onclick = openReportModal;
    }

    setupReportFormButtons();
    setActiveTab();
    loadDashboardData(currentTab, currentPage);
}

function setupReportFormButtons() {
    const saveDraftBtn = document.getElementById('saveDraftBtn');
    const submitReportBtn = document.getElementById('submitReportBtn');
    const closeBtn = document.getElementById('closeReportModalBtn');
    const cancelBtn = document.getElementById('cancelReportModalBtn');
    const modalLayer = document.getElementById('reportModal');

    if (saveDraftBtn) {
        saveDraftBtn.onclick = function () {
            submitReportForm('DRAFT');
        };
    }

    if (submitReportBtn) {
        submitReportBtn.onclick = function () {
            submitReportForm('REPORTED');
        };
    }

    if (closeBtn) {
        closeBtn.onclick = closeReportModal;
    }

    if (cancelBtn) {
        cancelBtn.onclick = closeReportModal;
    }

    if (modalLayer) {
        modalLayer.onclick = function (event) {
            if (event.target === modalLayer) {
                closeReportModal();
            }
        };
    }

    document.onkeydown = function (event) {
        if (event.key === 'Escape') {
            closeReportModal();
        }
    };
}

function openReportModal() {
    editingReportId = null;

    const form = document.getElementById('reportForm');
    const modalTitle = document.getElementById('reportModalTitle');
    const modalLayer = document.getElementById('reportModal');

    if (form) {
        form.reset();
    }

    setInputValue('reportId', '');
    setInputValue('reportTitle', '');
    setInputValue('reportCategory', '');
    setInputValue('reportLocation', '');
    setInputValue('reportDescription', '');

    if (modalTitle) {
        modalTitle.textContent = 'Laporan Baru';
    }

    if (modalLayer) {
        modalLayer.classList.add('show');
        document.body.classList.add('modal-lite-open');
    }
}

function closeReportModal() {
    const modalLayer = document.getElementById('reportModal');

    if (modalLayer) {
        modalLayer.classList.remove('show');
    }

    document.body.classList.remove('modal-lite-open');
}

async function editDraft(id) {
    editingReportId = id;

    try {
        const response = await requestAPI(`/api/reports/${id}/`, 'GET');

        if (!response.ok) {
            alert('Gagal mengambil data draft.');
            return;
        }

        const report = await response.json();
        const modalTitle = document.getElementById('reportModalTitle');

        setInputValue('reportId', report.id);
        setInputValue('reportTitle', report.title);
        setInputValue('reportCategory', report.category);
        setInputValue('reportLocation', report.location);
        setInputValue('reportDescription', report.description);

        if (modalTitle) {
            modalTitle.textContent = 'Edit Draft Laporan';
        }

        const modalLayer = document.getElementById('reportModal');

        if (modalLayer) {
            modalLayer.classList.add('show');
            document.body.classList.add('modal-lite-open');
        }
    } catch (error) {
        alert('Gagal terhubung ke server Django.');
    }
}

async function submitReportForm(status) {
    const title = getInputValue('reportTitle');
    const category = getInputValue('reportCategory');
    const location = getInputValue('reportLocation');
    const description = getInputValue('reportDescription');

    if (!title || !category || !location || !description) {
        alert('Semua field laporan harus diisi.');
        return;
    }

    const payload = {
        title,
        category,
        location,
        description,
        status
    };

    const endpoint = editingReportId ? `/api/reports/${editingReportId}/` : '/api/reports/';
    const method = editingReportId ? 'PUT' : 'POST';

    try {
        const response = await requestAPI(endpoint, method, payload);

        if (response.status === 201 || response.status === 200) {
            const form = document.getElementById('reportForm');

            if (form) {
                form.reset();
            }

            closeReportModal();
            editingReportId = null;
            currentTab = 'my_reports';
            currentPage = 1;
            setActiveTab();
            loadDashboardData(currentTab, currentPage);
            return;
        }

        alert('Gagal menyimpan laporan.');
    } catch (error) {
        alert('Gagal terhubung ke server Django.');
    }
}

function setActiveTab() {
    const tabButtons = document.querySelectorAll('.dashboard-tab');

    tabButtons.forEach(function (button) {
        if (button.dataset.tab === currentTab) {
            button.classList.remove('btn-soft');
            button.classList.add('btn-primary-custom');
        } else {
            button.classList.remove('btn-primary-custom');
            button.classList.add('btn-soft');
        }
    });
}

function normalizeApiResponse(data) {
    if (Array.isArray(data)) {
        return {
            count: data.length,
            next: null,
            previous: null,
            results: data
        };
    }

    return {
        count: data.count || 0,
        next: data.next || null,
        previous: data.previous || null,
        results: Array.isArray(data.results) ? data.results : []
    };
}

async function loadDashboardData(tab = 'my_reports', page = 1) {
    const reportContainer = document.getElementById('reportListContainer');
    const paginationContainer = document.getElementById('paginationContainer');

    if (!reportContainer || !paginationContainer) return;

    reportContainer.innerHTML = `
        <div class="soft-card p-4 text-center flex-shrink-0" style="width: 340px;">
            <div class="fw-bold text-main mb-1">Memuat data laporan...</div>
            <div class="small text-muted-custom">Mengambil data dari backend Django.</div>
        </div>
    `;

    paginationContainer.innerHTML = '';

    try {
        const response = await requestAPI(`/api/reports/?tab=${tab}&page=${page}`, 'GET');

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.hash = '#login';
            return;
        }

        if (!response.ok) {
            throw new Error('Gagal memuat data laporan');
        }

        const rawData = await response.json();
        const data = normalizeApiResponse(rawData);

        renderList(data.results, tab);
        renderPagination(data, tab, page);
        loadSummaryStats();
    } catch (error) {
        reportContainer.innerHTML = `
            <div class="soft-card p-4 text-center flex-shrink-0" style="width: 340px;">
                <div class="fw-bold text-main mb-1">Data gagal dimuat</div>
                <div class="small text-muted-custom">Pastikan server Django berjalan dan token login masih valid.</div>
            </div>
        `;
    }
}

async function loadSummaryStats() {
    try {
        const response = await requestAPI('/api/reports/?tab=my_reports&page_size=1000', 'GET');

        if (!response.ok) return;

        const rawData = await response.json();
        const data = normalizeApiResponse(rawData);
        const reports = data.results;

        const draftCount = reports.filter(report => report.status === 'DRAFT').length;
        const reportedCount = reports.filter(report => report.status === 'REPORTED').length;
        const progressCount = reports.filter(report => report.status === 'VERIFIED' || report.status === 'IN_PROGRESS').length;
        const resolvedCount = reports.filter(report => report.status === 'RESOLVED').length;
        const totalCount = draftCount + reportedCount + progressCount + resolvedCount;

        setText('summaryTotal', totalCount);
        setText('summaryDraft', draftCount);
        setText('summaryReported', reportedCount);
        setText('summaryProgress', progressCount);
        setText('summaryResolved', resolvedCount);

        setProgressLine('lineDraft', draftCount, totalCount);
        setProgressLine('lineReported', reportedCount, totalCount);
        setProgressLine('lineProgress', progressCount, totalCount);
        setProgressLine('lineResolved', resolvedCount, totalCount);
    } catch (error) {
        setText('summaryTotal', 0);
        setText('summaryDraft', 0);
        setText('summaryReported', 0);
        setText('summaryProgress', 0);
        setText('summaryResolved', 0);

        setProgressLine('lineDraft', 0, 0);
        setProgressLine('lineReported', 0, 0);
        setProgressLine('lineProgress', 0, 0);
        setProgressLine('lineResolved', 0, 0);
    }
}

function renderList(allReports, tab) {
    const reportContainer = document.getElementById('reportListContainer');

    if (!reportContainer) return;

    reportContainer.className = 'd-flex flex-nowrap overflow-auto gap-3 pb-3';

    if (allReports.length === 0) {
        reportContainer.innerHTML = `
            <div class="soft-card p-4 text-center flex-shrink-0" style="width: 340px;">
                <div class="mb-3 d-flex align-items-center justify-content-center rounded-4 mx-auto" style="width: 74px; height: 74px; background: var(--primary-soft); color: var(--primary);">
                    <i class="bi bi-inbox fs-2"></i>
                </div>

                <div class="fw-bold text-main mb-1">Belum ada laporan</div>

                <div class="small text-muted-custom">
                    ${tab === 'my_reports' ? 'Laporan pribadi kamu akan muncul di sini.' : 'Feed kota masih kosong.'}
                </div>
            </div>
        `;
        return;
    }

    reportContainer.innerHTML = allReports.map(function (report) {
        return renderReportCard(report, tab);
    }).join('');
}

function renderReportCard(report, tab) {
    const statusInfo = getStatusInfo(report.status);
    const reporterText = tab === 'feed' ? 'Warga Anonim' : (report.reporter || 'Saya');
    const actionButtons = getActionButtons(report, tab);
    const createdAt = formatDateTime(report.created_at);
    const updatedAt = formatDateTime(report.updated_at);

    return `
        <div class="soft-card p-3 flex-shrink-0" style="width: 345px; min-height: 360px;">
            <div class="d-flex flex-column h-100">
                <div class="d-flex align-items-center justify-content-between gap-2 mb-3">
                    <span class="badge rounded-pill" style="background: ${statusInfo.bg}; color: ${statusInfo.color}; border: 1px solid ${statusInfo.border};">
                        ${statusInfo.label}
                    </span>

                    <span class="small text-soft text-end">
                        <i class="bi bi-person-circle me-1"></i>
                        ${escapeHtml(reporterText)}
                    </span>
                </div>

                <h5 class="fw-bold text-main mb-2" style="line-height: 1.35;">
                    ${escapeHtml(report.title)}
                </h5>

                <div class="small text-muted-custom mb-2">
                    <div class="mb-1">
                        <i class="bi bi-folder2 me-1"></i>
                        ${escapeHtml(report.category || '-')}
                    </div>

                    <div>
                        <i class="bi bi-geo-alt me-1"></i>
                        ${escapeHtml(report.location || '-')}
                    </div>
                </div>

                <div class="small text-soft mb-2">
                    <div class="mb-1">
                        <i class="bi bi-calendar-plus me-1"></i>
                        Dibuat: ${escapeHtml(createdAt)}
                    </div>

                    <div>
                        <i class="bi bi-clock-history me-1"></i>
                        Diperbarui: ${escapeHtml(updatedAt)}
                    </div>
                </div>

                <p class="small text-muted-custom mb-3" style="line-height: 1.6; min-height: 72px;">
                    ${escapeHtml(report.description || '-')}
                </p>

                <div class="mt-auto">
                    <div class="progress" style="height: 8px; background: var(--card-bg);">
                        <div class="progress-bar" style="width: ${statusInfo.progress}%; background: ${statusInfo.color};"></div>
                    </div>

                    <div class="small text-soft mt-2 mb-3">
                        Progress laporan: ${statusInfo.progress}%
                    </div>

                    <div class="d-flex gap-2 flex-wrap">
                        ${actionButtons}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function getActionButtons(report, tab) {
    if (tab !== 'my_reports') {
        return '';
    }

    if (report.status === 'DRAFT' && report.is_owner) {
        return `
            <button type="button" class="btn btn-sm btn-soft" onclick="editDraft(${report.id})">
                <i class="bi bi-pencil-square me-1"></i>
                Edit
            </button>

            <button type="button" class="btn btn-sm btn-primary-custom" onclick="submitDraft(${report.id})">
                <i class="bi bi-send me-1"></i>
                Ajukan
            </button>
        `;
    }

    return `
        <button type="button" class="btn btn-sm btn-soft" disabled>
            <i class="bi bi-eye me-1"></i>
            Dipantau
        </button>
    `;
}

function renderPagination(data, tab, page) {
    const paginationContainer = document.getElementById('paginationContainer');

    if (!paginationContainer) return;

    const hasPrevious = Boolean(data.previous);
    const hasNext = Boolean(data.next);

    if (!hasPrevious && !hasNext) {
        paginationContainer.innerHTML = '';
        return;
    }

    paginationContainer.innerHTML = `
        <button type="button" class="btn btn-sm btn-soft" ${hasPrevious ? '' : 'disabled'} onclick="goToPage('${tab}', ${page - 1})">
            <i class="bi bi-chevron-left me-1"></i>
            Sebelumnya
        </button>

        <span class="small fw-bold text-main px-2">
            Halaman ${page}
        </span>

        <button type="button" class="btn btn-sm btn-soft" ${hasNext ? '' : 'disabled'} onclick="goToPage('${tab}', ${page + 1})">
            Berikutnya
            <i class="bi bi-chevron-right ms-1"></i>
        </button>
    `;
}

function goToPage(tab, page) {
    if (page < 1) return;

    currentTab = tab;
    currentPage = page;
    loadDashboardData(currentTab, currentPage);
}

async function submitDraft(id) {
    const confirmSubmit = confirm('Ajukan laporan ini sebagai REPORTED?');

    if (!confirmSubmit) return;

    try {
        const response = await requestAPI(`/api/reports/${id}/`, 'PATCH', {
            status: 'REPORTED'
        });

        if (response.ok) {
            loadDashboardData(currentTab, currentPage);
            return;
        }

        alert('Gagal mengajukan laporan.');
    } catch (error) {
        alert('Gagal terhubung ke server Django.');
    }
}

function getStatusInfo(status) {
    if (status === 'REPORTED') {
        return {
            label: 'DIAJUKAN',
            progress: 35,
            color: '#2563eb',
            bg: 'rgba(37, 99, 235, 0.10)',
            border: 'rgba(37, 99, 235, 0.24)'
        };
    }

    if (status === 'VERIFIED') {
        return {
            label: 'DIVERIFIKASI',
            progress: 60,
            color: '#0891b2',
            bg: 'rgba(8, 145, 178, 0.10)',
            border: 'rgba(8, 145, 178, 0.24)'
        };
    }

    if (status === 'IN_PROGRESS') {
        return {
            label: 'DIPROSES',
            progress: 80,
            color: '#f59e0b',
            bg: 'rgba(245, 158, 11, 0.12)',
            border: 'rgba(245, 158, 11, 0.25)'
        };
    }

    if (status === 'RESOLVED') {
        return {
            label: 'SELESAI',
            progress: 100,
            color: '#16a34a',
            bg: 'rgba(22, 163, 74, 0.12)',
            border: 'rgba(22, 163, 74, 0.25)'
        };
    }

    return {
        label: 'DRAFT',
        progress: 10,
        color: '#64748b',
        bg: 'rgba(100, 116, 139, 0.12)',
        border: 'rgba(100, 116, 139, 0.24)'
    };
}

function formatDateTime(value) {
    if (!value) return '-';

    const date = new Date(value);

    if (isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getInputValue(id) {
    const input = document.getElementById(id);
    return input ? input.value.trim() : '';
}

function setInputValue(id, value) {
    const input = document.getElementById(id);

    if (input) {
        input.value = value || '';
    }
}

function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}

function setProgressLine(id, value, total) {
    const element = document.getElementById(id);

    if (!element) return;

    if (!total || total <= 0) {
        element.style.width = '0%';
        return;
    }

    const percent = Math.max(4, Math.min(100, Math.round((value / total) * 100)));
    element.style.width = `${percent}%`;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}