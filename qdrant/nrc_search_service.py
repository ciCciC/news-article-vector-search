from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neural_searcher import NeuralSearcher
from qdrant.config import COLLECTION_NAME

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)


@app.get("/nrc/search")
async def search_article(q: str, limit: int):
    return {
        "result": neural_searcher.search(text=q, limit=limit)
    }


@app.get("/nrc/recommend")
async def recommend_articles(like: int = None, limit: int = 5):
    return {
        "result": neural_searcher.recommend(like=like, limit=limit)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
