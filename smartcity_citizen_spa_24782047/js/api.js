const BASE_URL = 'http://127.0.0.1:8000'; // URL Backend Django kamu

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = {
        'Content-Type': 'application/json',
    };

    // Ambil access_token dari localStorage
    const token = localStorage.getItem('access_token');
    
    // Jika token ada, sisipkan ke header Authorization
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers,
    };

    // Jika ada data yang dikirim (misal saat POST login), ubah ke string JSON
    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}