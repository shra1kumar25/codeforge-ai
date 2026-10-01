import json

from app.services.gemini_service import ask_gemini


def detect_intent(user_message: str):
    prompt = f"""
You are the intent detection component of CodeForge AI.

Analyze the user's request and identify the primary intent.

Return ONLY valid JSON in this format:

{{
    "intent": "one short intent name",
    "description": "what the user wants to accomplish",
    "requires_code": true,
    "requires_tools": false
}}

User request:
{user_message}
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "intent": "unknown",
            "description": response,
            "requires_code": False,
            "requires_tools": False,
        }
