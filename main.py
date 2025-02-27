import os
import uvicorn
import openai
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

print("🚀 Iniciando API de Chat Colectivo...")

# Inicializar la aplicación FastAPI
app = FastAPI()

# ✅ Configurar CORS para permitir solicitudes desde la PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por los dominios permitidos si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)

# ✅ Permitir OPTIONS en /chat para evitar el error 405
@app.options("/chat")
async def chat_options():
    return JSONResponse({"message": "OK"}, status_code=200)

# ✅ Verificar si la clave de OpenAI está presente
OPENAI_API_KEY = os.getenv("chat-c")
if not OPENAI_API_KEY:
    print("❌ ERROR: La clave de OpenAI no está configurada en Railway.")
else:
    print("✅ Clave de OpenAI detectada.")
    openai.api_key = OPENAI_API_KEY

# ✅ URL del contrato colectivo en GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/andresurbanoz7/contrato-colectivo/main/contrato_colectivo.txt"

def obtener_contrato():
    """Obtiene el contenido del contrato colectivo desde GitHub con manejo de errores."""
    try:
        print("📥 Descargando contrato colectivo desde GitHub...")
        respuesta = requests.get(GITHUB_RAW_URL, timeout=5)
        if respuesta.status_code == 200:
            print("✅ Contrato colectivo descargado exitosamente.")
            return respuesta.text
        else:
            print("❌ ERROR: No se pudo obtener el contrato colectivo.")
            return "No se pudo obtener el contrato colectivo. Inténtalo más tarde."
    except requests.RequestException:
        print("❌ ERROR: Fallo de conexión con GitHub.")
        return "Error al conectarse a GitHub. Verifica tu conexión."

# ✅ Cargar el contrato colectivo al iniciar
CONTRATO_COLECTIVO = obtener_contrato()

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
        client = openai.OpenAI()  # 🔹 Inicializa correctamente el cliente

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente que solo responde preguntas relacionadas con el contrato colectivo."},
                {"role": "user", "content": f"Contrato colectivo:\n\n{CONTRATO_COLECTIVO}\n\nPregunta: {user_question}"}
            ],
            temperature=0.2
        )

        respuesta_chat = response.choices[0].message.content
        print(f"💬 Respuesta generada: {respuesta_chat}")

        return {"response": respuesta_chat}

    except Exception as e:
        print(f"❌ ERROR al procesar la pregunta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno en el servidor")

# ✅ Inicio del servidor en Railway
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))  # Usa el puerto asignado por Railway
    print(f"🚀 Iniciando servidor en el puerto {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, workers=1)
