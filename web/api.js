const init = {
    "headers": {
        'Content-Type': 'application/json'
    },
}

const queryArticles = async (q, limit) => {
    let base_url = 'http://127.0.0.1:8000/nrc/search?q=' + q + '&limit=' + limit
    const response = await fetch(base_url, init);
    return response.json();
}

const recommendArticles = async (like, limit) => {
    let base_url = 'http://127.0.0.1:8000/nrc/recommend?like=' + like + '&limit=' + limit
    const response = await fetch(base_url, init);
    return response.json();
}