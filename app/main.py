from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from stockfish import Stockfish
from queue import Empty
from queue import Queue
from typing import Optional

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sengiria.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

ENGINE_POOL_SIZE = 3
engine_pool: Optional[Queue] = None

class FENRequest(BaseModel):
    fen: str

def create_engine() -> Stockfish:
    return Stockfish(
        "./stockfish",
        depth=15,
        parameters={
            "Threads": 2,
            "Minimum Thinking Time": 30
        }
    )

@app.on_event("startup")
async def preload():
    global engine_pool
    engine_pool = Queue(maxsize=ENGINE_POOL_SIZE)

    for _ in range(ENGINE_POOL_SIZE):
        engine = create_engine()
        engine.set_position([])
        engine_pool.put(engine)

    print(f"Initialized and warmed up {ENGINE_POOL_SIZE} Stockfish engines.")

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/best-move")
def best_move(fen_request: FENRequest):
    global engine_pool

    if engine_pool is None:
        return {"error": "Engine pool not initialized."}

    try:
        engine = engine_pool.get(timeout=5)
    except Empty:
        return {"error": "All engines are currently busy. Try again shortly."}

    try:
        try:
            # try using the engine
            engine.set_fen_position(fen_request.fen)
            best = engine.get_best_move()
        except Exception as e:
            print("Stockfish crashed, recreating engine:", e)
            # Create a new engine
            engine = create_engine()
            engine.set_fen_position(fen_request.fen)
            best = engine.get_best_move()
    finally:
        engine_pool.put(engine)

    return {"best_move": best}
