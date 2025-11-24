from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do .env (quando rodar localmente)
load_dotenv()

app = FastAPI(
    title="IsCoolGPT",
    description="Assistente inteligente de estudos em Cloud Computing usando Gemini",
    version="1.0.0"
)

# Caminhos para servir arquivos estáticos (front)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Monta a pasta static em /static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
async def serve_frontend():
    """
    Serve a página inicial (front-end simples).
    """
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest):
    """
    Endpoint que conversa com a LLM do Gemini.
    """
    if not GEMINI_API_KEY:
        return ChatResponse(answer="Erro: GEMINI_API_KEY não configurada no servidor.")

    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = (
        "Você é um tutor especialista em Cloud Computing com foco em AWS, ECS, Docker, CI/CD "
        "e arquitetura cloud moderna. Explique com clareza, passo a passo e com exemplos simples.\n\n"
        f"Pergunta do aluno: {body.message}"
    )

    response = model.generate_content(prompt)

    return ChatResponse(answer=response.text)
