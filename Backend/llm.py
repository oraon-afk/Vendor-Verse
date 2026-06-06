import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def get_llm(temperature=0.7):
    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENROUTER_CHAT_MODEL", "google/gemma-4-31b-it:free")
    
    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "https://localhost:3000",
            "X-OpenRouter-Title": "Vendor Verse"
        }
    )
