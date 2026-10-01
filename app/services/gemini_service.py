import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text

    except Exception as error:
        error_message = str(error)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
         return '{"action": "pause", "reason": "Gemini API quota exceeded", "retry_after": "Wait for the Gemini quota to reset before continuing."}'
        raise
