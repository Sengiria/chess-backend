# Stockfish Chess API

A FastAPI-based backend that uses [Stockfish](https://stockfishchess.org/) to calculate the best move from any valid FEN position. Optimized with CORS, GZip, and `orjson` for speed and safety.

---

## Features

- **Best Move Endpoint** — returns Stockfish's best move from a given FEN.
- **CORS Middleware** — only allows requests from the deployed frontend.
- **GZip Compression** — reduces payload size for large responses.
- **Ping Endpoint** — quick health check for the server.
- **Fast JSON** — uses `orjson` for faster serialization.

---

## Requirements

- Python 3.9+
- `stockfish` binary (place inside the root directory)

---

## Project Structure
<pre>
├── main.py # FastAPI app with endpoints
├── stockfish # Stockfish engine binary (chmod +x if needed)
└── requirements.txt # Python dependencies
</pre>

---

##  Install dependencies:
```bash
   pip install -r requirements.txt
```

## Run the server:
```bash
uvicorn main:app --reload
```

## Test it
Visit:
http://localhost:8000/docs — Swagger UI
http://localhost:8000/ping — Health check

## Deployed Frontend

This API is used by the frontend at:
[https://sengiria.github.io/chess/](https://sengiria.github.io/chess/)

## Endpoints

POST /best-move

Returns the best move for a given position.

**Body:**
```bash
{
  "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
}
```

**Response:**
```bash
{
  "best_move": "c7c5"
}
```

GET /ping

Health check.

**Returns:**
```bash
{
    "status": "ok" 
}
```

---

## License
MIT – feel free to use and modify for your own projects!