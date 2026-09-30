from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Ключ подтянется из безопасных настроек Vercel, которые мы укажем позже
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://deepseek.com"

class MessageData(BaseModel):
    player_text: str

SYSTEM_PROMPT = """Ты — интерактивный NPC в Roblox. Отвечай коротко (1-2 фразы). 
Если игрок грубит/угрожает убить — ответь дерзко и в конце добавь [ACTION: KILL].
Если игрок вежлив/помогает/предлагает выгоду — ответь тепло и в конце добавь [ACTION: GIVE_SPEED].
Если диалог нейтральный — ответь обычно и в конце добавь [ACTION: NONE].
Не выдумывай факты, даты и цитаты."""

@app.post("/chat")
def chat_with_npc(data: MessageData):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is missing on server")
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.player_text}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        result = response.json()
        ai_text = result["choices"]["message"]["content"]
        return {"response": ai_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
