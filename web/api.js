const init = {
    "headers": {
        'Content-Type': 'application/json'
    },
}

const query_article = async (q, limit) => {
    let base_url = 'http://127.0.0.1:8000/nrc/search?q=' + q + '&limit=' + limit
    const response = await fetch(base_url, init);
    return response.json();
}