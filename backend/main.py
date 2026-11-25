
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PROJECT ECHO",
    version="0.4.0"
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

@app.get("/")
def home():
    return {
        "system": "PROJECT ECHO",
        "version": "0.4.0",
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ai_connected": False
    }

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "system": "ECHO",
        "message": request.message,
        "response": (
            "Backend đã nhận được tin nhắn. "
            "Mô hình AI chưa được kết nối."
        )
    }
