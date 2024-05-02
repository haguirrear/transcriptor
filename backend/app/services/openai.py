from openai import OpenAI
from backend.app.settings import settings

openai_client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
