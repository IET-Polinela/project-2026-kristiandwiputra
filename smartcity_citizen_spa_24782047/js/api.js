const BASE_URL = 'http://127.0.0.1:8000';

function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function saveAccessToken(token) {
    localStorage.setItem('access_token', token);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

async function refreshAccessToken() {
    const refreshToken = getRefreshToken();

    if (!refreshToken) {
        clearTokens();
        return false;
    }

    try {
        const response = await fetch(`${BASE_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (!response.ok) {
            clearTokens();
            return false;
        }

        const data = await response.json();
        saveAccessToken(data.access);
        return true;
    } catch (error) {
        clearTokens();
        return false;
    }
}

function buildRequestOptions(method, bodyData, token) {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const options = {
        method,
        headers
    };

    if (bodyData !== null) {
        options.body = JSON.stringify(bodyData);
    }

    return options;
}

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const url = `${BASE_URL}${endpoint}`;
    const token = getAccessToken();

    try {
        let response = await fetch(url, buildRequestOptions(method, bodyData, token));

        if (
            response.status === 401 &&
            endpoint !== '/api/token/' &&
            endpoint !== '/api/token/refresh/'
        ) {
            const refreshed = await refreshAccessToken();

            if (refreshed) {
                response = await fetch(url, buildRequestOptions(method, bodyData, getAccessToken()));
            }
        }

        return response;
    } catch (error) {
        console.error('Gagal terhubung ke server:', error);
        throw error;
    }
}