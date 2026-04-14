"""
-------------------------------------------------------------------------------
PROYECTO: AI Travel Assistant - Premium Experience
DESCRIPCIÓN: Chatbot interactivo que utiliza IA (Groq/Llama 3.3) y Function 
             Calling para proporcionar recomendaciones de viaje y clima real.
AUTOR: Jose Eduardo del Real Rico
FECHA DE CREACIÓN: 12 de Abril de 2026
ÚLTIMA MODIFICACIÓN: 13 de Abril de 2026
VERSIÓN: 1.1.2
-------------------------------------------------------------------------------
"""

import os
import json
import time
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"

def get_weather(location: str) -> str:
    """Consulta clima real usando la API de Open-Meteo."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=es&format=json"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response.get("results"):
            return json.dumps({"location": location, "weather": "No encontré ese lugar."})
            
        res = geo_response["results"][0]
        lat, lon = res["latitude"], res["longitude"]
        pais = res.get("country", "📍")
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()
        
        temp = weather_res["current_weather"]["temperature"]
        return json.dumps({"location": f"{location}, {pais}", "weather": f"{temp}°C"})
    except Exception:
        return json.dumps({"location": location, "weather": "Error de conexión con el satélite."})


tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Obtiene el clima real de una ciudad para dar recomendaciones de viaje.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Ciudad y país"}
            },
            "required": ["location"],
        },
    }
}]

SYSTEM_PROMPT = """
Conviértete en un Asistente de nivel experto de Viajes Senior con experiencia en turismo internacional.
Tu nombre es 'Vía' y tu objetivo es ayudar a los usuarios con datos reales y entusiasmo.

REGLAS DE ORO:
1. SIEMPRE usa la herramienta 'get_weather' si el usuario menciona un lugar o pregunta por el clima.
2. Está PROHIBIDO inventar temperaturas.
3. Tras recibir el clima, estructura tu respuesta de forma amigable:
   - 🌍 **Destino y Clima**: Informa la temperatura actual.
   - 🧥 **Guía de Equipaje**: Qué ropa y accesorios empacar.
   - 📸 **Agenda de Actividades**: Qué hacer según el clima.
4. Usa un tono experto, servicial y utiliza emojis para mejorar la experiencia.
"""

def main():
    api_key = os.getenv("GROQ_API_KEY")

    # Valida si hay API KEY
    if not api_key or not api_key.startswith("gsk_"):
        api_key = None

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("\n" + " 🛩️ " * 15)
    print("  🌍 ¡HOLA! SOY VÍA, TU GUÍA EXPERTA DE VIAJES  ")
    print("     Dime: ¿A qué lugar del mundo quieres ir hoy?" )
    print("(Escribe 'salir' o 'exit' para terminar la aventura)\n")

    # 🔥 MODO DEMO
    if not api_key:
        print("⚠️ Ejecutando en modo demo (sin API key válida)\n")

        while True:
            try:
                user_input = input("👤 Tú: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\n🤖 Vía: ¡Fue un placer ayudarte! ✈️🌍")
                    break

                print("\n🤖 Vía:")
                print(f"🌍 Destino: {user_input.title()}")
                print("🌤️ Clima: 24°C (simulado)")
                print("🧳 Recomendación: Lleva ropa cómoda")
                print("✨ Consejo: Ideal para explorar la ciudad.\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\n🤖 Vía: Sesión finalizada. ¡Hasta luego! ✈️")
                break

        return

    # 🔥 TU CÓDIGO ORIGINAL
    client = OpenAI(
        api_key=api_key, 
        base_url="https://api.groq.com/openai/v1"
    )

    while True:
        try:
            user_input = input("👤 Tú: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['salir', 'exit', 'quit']: 
                print("\n🤖 Vía: ¡Fue un placer ayudarte! ¡Buen viaje y hasta pronto! ✈️🌍")
                break
                
            messages.append({"role": "user", "content": user_input})
            print("🤖 Vía está analizando tu destino...", end="\r")

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools
            )
            
            msg = response.choices[0].message
            
            if msg.tool_calls:
                messages.append(msg)
                
                for tool_call in msg.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    ciudad = args.get("location")
                    
                    print(f"   🔎 Consultando el clima real para: {ciudad}... 🛰️")
                    time.sleep(1)
                    
                    info_clima = get_weather(ciudad)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "get_weather",
                        "content": info_clima
                    })
                
                final_res = client.chat.completions.create(model=MODEL_NAME, messages=messages)
                respuesta = final_res.choices[0].message.content
            else:
                respuesta = msg.content

            print(f"\n🤖 Vía: {respuesta}\n")
            messages.append({"role": "assistant", "content": respuesta})

        except (KeyboardInterrupt, EOFError):
            print("\n\n🤖 Vía: Sesión finalizada. ¡Hasta luego! ✈️")
            break
        except Exception as e:
            print(f"\n⚠️ Error con API: {e}")
            print("🔁 Cambiando a modo demo...\n")

            while True:
                user_input = input("👤 Tú: ").strip()

                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\n🤖 Vía: ¡Hasta luego! ✈️")
                    break

                print("\n🤖 Vía:")
                print(f"🌍 Destino: {user_input.title()}")
                print("🌤️ Clima: 24°C (simulado)")
                print("🧳 Recomendación: Lleva ropa cómoda\n")

            break


if __name__ == "__main__":
    main()