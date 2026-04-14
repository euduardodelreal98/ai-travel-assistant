# ✈️ AI Travel Assistant – Chatbot con Clima en Tiempo Real

Este proyecto es un chatbot de consola que utiliza un modelo de lenguaje (LLM) con **Function Calling** para proporcionar información del clima en tiempo real y recomendaciones de viaje personalizadas.

El asistente detecta cuándo el usuario pregunta por un lugar, consulta datos reales desde una API y genera respuestas útiles y amigables.

---

## 🚀 Características

* 🤖 Chatbot conversacional con memoria (multi-turn)
* 🌍 Soporte para ciudades y países de todo el mundo
* 🌤️ Consulta de clima en tiempo real
* 🧠 Uso de LLM con Function Calling
* 🔐 Manejo seguro de credenciales con `.env`
* 🧪 Modo demo si no hay API key configurada

---

## 🛠️ Tecnologías utilizadas

* Python
* OpenAI SDK (usado con Groq)
* Open-Meteo API (clima real)
* requests
* python-dotenv

---

## 🔑 Cómo obtener tu API Key (Groq)

Para que el chatbot funcione completamente necesitas una API key gratuita de Groq:

1. Ve a 👉 https://console.groq.com/
2. Crea una cuenta (puedes usar Google)
3. En el menú, entra a **API Keys**
4. Da clic en **Create API Key**
5. Copia tu key (empieza con `gsk_...`)

---

## ⚙️ Configuración del proyecto

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/ai-travel-assistant.git
cd ai-travel-assistant
```

2. Instala dependencias:

```bash
pip install openai requests python-dotenv
```

3. Crea un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_api_key_aqui
```

---

## ▶️ Cómo ejecutar

```bash
python chatbot.py
```

---

## 🧪 Modo Demo

Si no configuras una API key válida:

* El chatbot seguirá funcionando
* Usará datos simulados
* Podrás probar el flujo completo sin errores

---

## 🔐 Seguridad

Por buenas prácticas:

* ❌ No se incluye ninguna API key en el repositorio
* ✅ Se utiliza `.env` para variables sensibles
* ✅ Se incluye `.env.example` como guía

---

## 🧪 Validación de APIs

Antes de integrar el código, se realizaron pruebas con herramientas como **Postman** para validar:

* Conexión con Groq (LLM)
* Estructura de Function Calling
* Respuesta de la API de clima

---

## 💡 Notas

Este proyecto fue desarrollado como parte de una prueba técnica, aplicando buenas prácticas de desarrollo, integración de APIs y diseño de sistemas conversacionales.

---

## 👨‍💻 Autor

Jose Eduardo del Real Rico
