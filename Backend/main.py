from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
from openai import OpenAI
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

# 🚀 Create FastAPI app
app = FastAPI()

# 🌐 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🤖 Initialize OpenRouter (FREE API)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# 📩 Request model
class Message(BaseModel):
    text: str

# 🏠 Test route
@app.get("/")
def home():
    return {"message": "Server is running"}

# 💬 Chat endpoint
@app.post("/chat")
def chat(msg: Message):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert programming assistant. Always return clean, properly indented code inside code blocks. Format code correctly and make it readable."
                },
                {
                    "role": "user",
                    "content": msg.text
                }
            ]
        )

        reply = response.choices[0].message.content

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}