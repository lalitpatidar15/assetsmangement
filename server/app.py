from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Any, Dict, List
import asyncio

app = FastAPI(title="Asset Agent Ingest API")

# In-memory log store for demo; production should persist to DB or file
logs: List[Dict[str, Any]] = []

@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.post("/ingest")
async def ingest(request: Request) -> Response:
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)

    record = {
        "received_at": datetime.utcnow().isoformat(),
        "remote": request.client.host if request.client else None,
        "payload": payload,
    }
    logs.append(record)

    # Print to server console for immediate visibility
    print("[INGEST]", record["received_at"], record["remote"], payload)

    # Keep only last 1000 records to avoid unbounded growth in demo
    if len(logs) > 1000:
        del logs[: len(logs) - 1000]

    return JSONResponse({"status": "ok"})

@app.get("/logs")
async def get_logs(limit: int = 50) -> Dict[str, Any]:
    if limit <= 0:
        limit = 1
    limit = min(limit, 1000)
    return {"count": len(logs), "items": logs[-limit:]}
