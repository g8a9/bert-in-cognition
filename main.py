import pickle
from itertools import combinations
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from scipy.spatial.distance import cosine

app = FastAPI()


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
    with open(f"../bert_embeddings_coca/{emb_file}", "rb") as fp:
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
