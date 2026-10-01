import json

from app.services.gemini_service import ask_gemini


def create_plan(user_message: str, intent: dict):
    prompt = f"""
You are the planning component of CodeForge AI.

Create a clear step-by-step development plan for the user's request.

User request:
{user_message}

Detected intent:
{json.dumps(intent, indent=2)}

Return ONLY valid JSON in this format:

{{
    "goal": "short description of the final goal",
    "steps": [
        {{
            "step": 1,
            "description": "first task"
        }},
        {{
            "step": 2,
            "description": "second task"
        }}
    ]
}}

Rules:
- Keep the plan practical.
- Order the steps logically.
- Do not execute anything.
- Do not write code.
- Only create the plan.
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "goal": "Unable to parse planning response",
            "steps": [
                {
                    "step": 1,
                    "description": response,
                }
            ],
        }
