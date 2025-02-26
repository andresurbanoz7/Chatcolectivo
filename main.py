from fastapi import FastAPI, HTTPException
import openai
import requests

app = FastAPI()

# Configura tu clave de API de OpenAI
openai.api_key = "OPENAI_API_KEY"

# URL del contrato colectivo en GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/andresurbanoz7/contrato-colectivo/main/contrato_colectivo.txt"

def obtener_contrato():
    """Obtiene el contenido del contrato colectivo desde GitHub."""
    response = requests.get(GITHUB_RAW_URL)
    if response.status_code == 200:
        return response.text
    else:
        return "No se pudo obtener el contrato colectivo."

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
