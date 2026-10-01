import json

from app.services.gemini_service import ask_gemini


AVAILABLE_TOOLS = [
    "read_file",
    "write_file",
    "search_code",
    "run_command",
]


def select_tools(user_message: str, plan: dict):
    prompt = f"""
You are the tool selection component of CodeForge AI.

Choose which tools are required to complete the user's request.

Available tools:
{json.dumps(AVAILABLE_TOOLS, indent=2)}

User request:
{user_message}

Development plan:
{json.dumps(plan, indent=2)}

Return ONLY valid JSON in this format:

{{
    "tools": [
        {{
            "name": "tool_name",
            "reason": "why this tool is needed",
            "arguments": {{
                "file_path": "app/main.py"
            }}
        }}
    ]
}}

Rules:
- Only select tools from the available tools list.
- Select only tools that are actually required.
- Provide the arguments required by the selected tool.
- Do not execute any tool.
- Do not write code.
- For read_file, use the argument name "file_path".
- For write_file, use "file_path" and "content".
- For search_code, use "search_term" and optionally "project_path".
- For run_command, use "command".
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "tools": []
        }
