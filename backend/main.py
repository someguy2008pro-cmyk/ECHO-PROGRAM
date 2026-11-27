from fastapi.responses import JSONResponse
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.adapter import generate_reply
from memory.manager import (
    propose_memory,
    get_memories,
    search_memories,
    get_pending_memories,
    approve_memory,
    update_memory,
    delete_memory
)

app = FastAPI(
    title="PROJECT ECHO",
    version="0.5.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://someguy2008pro-cmyk.github.io"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class MemoryRequest(BaseModel):
    content: str
    category: str = "general"


class MemorySearchRequest(BaseModel):
    query: str


class MemoryUpdateRequest(BaseModel):
    content: Optional[str] = None
    category: Optional[str] = None


@app.get("/")
def home():
    return {
        "system": "PROJECT ECHO",
        "version": "0.5.2",
        "status": "online"
    }


@app.get("/health")
def health():
    import os
    return {
        "status": "healthy",
        "ai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Tin nhắn không được để trống."
        )

    try:
        reply = generate_reply(message)
        return {
            "system": "ECHO",
            "message": message,
            "response": reply
        }
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Không thể nhận phản hồi từ AI."
        )


@app.post("/memory")
def create_memory(request: MemoryRequest):
    try:
        return propose_memory(
            request.content,
            request.category
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/memory")
def list_memories():
    return {"memories": get_memories()}


@app.post("/memory/search")
def search_memory_api(request: MemorySearchRequest):
    results = search_memories(request.query)

    return {
        "query": request.query,
        "count": len(results),
        "results": results
    }


@app.get("/memory/pending")
def list_pending_memories():
    return {"pending_memories": get_pending_memories()}


@app.post("/memory/{memory_id}/approve")
def approve_memory_api(memory_id: str):
    result = approve_memory(memory_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy ký ức."
        )

    return result


@app.put("/memory/{memory_id}")
def update_memory_api(
    memory_id: str,
    request: MemoryUpdateRequest
):
    if request.content is None and request.category is None:
        raise HTTPException(
            status_code=400,
            detail="Không có nội dung cập nhật."
        )

    try:
        result = update_memory(
            memory_id,
            request.content,
            request.category
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy ký ức."
        )

    return result


@app.delete("/memory/{memory_id}")
def delete_memory_api(memory_id: str):
    result = delete_memory(memory_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy ký ức."
        )

    return result


@app.get("/memory/backup")
def backup_memory():
    return JSONResponse(
        content={
            "system": "PROJECT ECHO",
            "backup_version": "1.0",
            "memories": get_memories()
        },
        headers={
            "Content-Disposition":
                'attachment; filename="echo-memory-backup.json"'
        }
    )
