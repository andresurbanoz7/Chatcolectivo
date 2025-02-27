import os
import uvicorn
import openai
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

print("🚀 Iniciando API de Chat Colectivo...")

# ✅ Obtener la API Key desde la variable de entorno correcta
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Debe estar en Railway con este nombre

if not OPENAI_API_KEY:
    print("❌ ERROR: La clave de OpenAI no está configurada en Railway.")
else:
    print("✅ Clave de OpenAI detectada.")

# ✅ Crear cliente de OpenAI con la clave correcta
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Configurar FastAPI y CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.options("/chat")
async def chat_options():
    return JSONResponse({"message": "OK"}, status_code=200)

@app.get("/")
def home():
    return {"message": "API de Chat Colectivo en línea. Usa /chat para interactuar."}

@app.post("/chat")
async def chat_laboral(question: dict):
    """Responde solo preguntas sobre el contrato colectivo."""
    user_question = question.get("message")

    if not user_question:
        raise HTTPException(status_code=400, detail="Debe incluir una pregunta.")

    print(f"📩 Recibida pregunta del usuario: {user_question}")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente que solo responde preguntas relacionadas con el contrato colectivo."},
                {"role": "user", "content": f"Contrato colectivo:\n\nPregunta: {user_question}"}
            ],
            temperature=0.2
        )

        respuesta_chat = response.choices[0].message.content
        print(f"💬 Respuesta generada: {respuesta_chat}")

        return {"response": respuesta_chat}

    except Exception as e:
        print(f"❌ ERROR al procesar la pregunta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno en el servidor")

# ✅ Iniciar servidor en Railway
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))
    print(f"🚀 Iniciando servidor en el puerto {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, workers=1)
