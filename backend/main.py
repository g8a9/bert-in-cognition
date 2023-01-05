import pickle
from itertools import combinations
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scipy.spatial.distance import cosine

EMBEDDING_DIR = "../bert_embeddings_coca/"

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimpleRequest(BaseModel):
    words: List[str]
    layer: int = 11
    aggregation: str = "average"


@app.get("/")
async def root():
    return {"message": "Hello World"}
    

@app.post("/prototypes")
async def prototypes(request: SimpleRequest):
    agg = request.aggregation
    layer = request.layer
    words = request.words

    if agg == "average":
        emb_file = f"prototype_embeddings_bert_{layer}.pkl"
    else:
        emb_file = f"non_contextual_embeddings_bert_{layer}.pkl"

    # load embeddings
    with open(f"{EMBEDDING_DIR}/{emb_file}", "rb") as fp:
        embs = pickle.load(fp)

    # out of vocabulary
    words = set(words)
    oov_words = [w for w in words if w not in embs]
    words = words.difference(oov_words)

    similarities = list()
    for w1, w2 in combinations(words, 2):

        similarities.append(
            {
                "w1": w1,
                "w2": w2,
                "sim": 1 - cosine(embs[w1], embs[w2])
            }
        )

    return {
        "request": request,
        "similarities": similarities,
        "oov_words": oov_words
    }
