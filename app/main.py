from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from stockfish import Stockfish

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sengiria.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

stockfish = Stockfish(path="./stockfish", depth=15, parameters={
    "Threads": 2,
    "Minimum Thinking Time": 30
})

class FENRequest(BaseModel):
    fen: str

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/best-move")
async def best_move(request: FENRequest):
    fen = request.fen
    if not stockfish.is_fen_valid(fen):
        return {"error": "Invalid FEN"}

    stockfish.set_fen_position(fen)
    return {"best_move": stockfish.get_best_move()}
