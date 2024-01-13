from openai import OpenAI

from transcriptor.settings import settings

openai_client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
