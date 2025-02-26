# Chat Laboral basado en OpenAI

Este proyecto implementa un chat laboral que responde preguntas exclusivamente sobre el contrato colectivo. Se compone de un backend en **FastAPI** y un frontend en **HTML + JavaScript**.

## Instalación y Uso

### 1. Configuración Backend
1. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### 2. Despliegue en Railway
1. Sube los archivos del backend a un repositorio en GitHub.
2. Conéctalo con [Railway](https://railway.app/).
3. Agrega la API Key de OpenAI en las variables de entorno.

### 3. Integración en PWA
- **Sube `chat.html`** a tu PWA.
- **Configura la URL del backend** en el archivo `chat.html`.

¡Listo! Tu chat laboral estará funcionando.
