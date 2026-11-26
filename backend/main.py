
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.adapter import generate_reply
from memory.manager import save_memory, get_memories

app = FastAPI(
    title="PROJECT ECHO",
    version="0.5.0"
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


@app.get("/")
def home():
    return {
        "system": "PROJECT ECHO",
        "version": "0.5.0",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ai_configured": bool(__import__("os").getenv("OPENAI_API_KEY"))
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
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Không thể nhận phản hồi từ AI."
        )


@app.post("/memory")
def create_memory(request: MemoryRequest):
    try:
        memory = save_memory(
            request.content,
            request.category
        )

        return {
            "status": "saved",
            "memory": memory
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/memory")
def list_memories():
    return {
        "memories": get_memories()
    }
    
