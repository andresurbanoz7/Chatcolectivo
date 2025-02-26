from fastapi import FastAPI, HTTPException
import openai
import requests

app = FastAPI()

# Configura tu clave de API de OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


# URL del contrato colectivo en GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/andresurbanoz7/contrato-colectivo/main/contrato_colectivo.txt"

def obtener_contrato():
    """Obtiene el contenido del contrato colectivo desde GitHub con manejo de errores."""
    try:
        respuesta = requests.get(GITHUB_RAW_URL, timeout=5)

        if respuesta.status_code == 200:
            return respuesta.text
        else:
            return "No se pudo obtener el contrato colectivo. Inténtalo más tarde."
    except requests.RequestException:
        return "Error al conectarse a GitHub. Verifica tu conexión."


# Cargar el contrato colectivo al iniciar
CONTRATO_COLECTIVO = obtener_contrato()

@app.post("/chat")
async def chat_laboral(question: dict):
    """Responde solo preguntas sobre el contrato colectivo."""
    user_question = question.get("message")

    if not user_question:
        raise HTTPException(status_code=400, detail="Debe incluir una pregunta.")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente que solo responde preguntas relacionadas con el contrato colectivo."},
            {"role": "user", "content": f"Contrato colectivo:\n\n{CONTRATO_COLECTIVO}\n\nPregunta: {user_question}"}
        ],
        temperature=0.2
    )

    return {"response": response["choices"][0]["message"]["content"]}
