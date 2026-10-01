import json

from app.services.gemini_service import ask_gemini
from app.tools.tool_registry import get_available_tools


AVAILABLE_TOOLS = {
    "list_directory": {
        "arguments": {
            "path": "string"
        }
    },
    "read_file": {
        "arguments": {
            "file_path": "string"
        }
    },
    "write_file": {
        "arguments": {
            "file_path": "string",
            "content": "string"
        }
    },
    "create_file": {
        "arguments": {
            "file_path": "string",
            "content": "string"
        }
    },
    "execute_command": {
        "arguments": {
            "command": "string"
        }
    },
    "inspect_workflow": {
        "arguments": {
            "workflow": "object"
        }
    },
    "diagnose_workflow": {
        "arguments": {
            "workflow_data": "object"
        }
    },
    "fix_workflow": {
        "arguments": {
            "workflow_data": "object",
            "issue": "object"
        }
    }
}


def decide_next_action(
    goal: str,
    previous_results: list,
):
    prompt = f"""
You are the decision engine of a local autonomous AI coding agent.

Your job is to decide the NEXT action the agent should take.

USER GOAL:
{goal}

PREVIOUS TOOL RESULTS:
{json.dumps(previous_results, indent=2, default=str)}

AVAILABLE TOOLS:
{json.dumps(AVAILABLE_TOOLS, indent=2)}

SELF-HEALING WORKFLOW:

1. If the workflow has not been inspected yet and the goal involves
   understanding or fixing a workflow, choose:

   {{
       "action": "tool",
       "tool": "inspect_workflow",
       "arguments": {{}}
   }}

2. After inspection, if the workflow needs analysis, choose:

   {{
       "action": "tool",
       "tool": "diagnose_workflow",
       "arguments": {{}}
   }}

3. If diagnosis reports problems that can be fixed, choose:

   {{
       "action": "tool",
       "tool": "fix_workflow",
       "arguments": {{}}
   }}

4. After a fix has been performed, diagnose the workflow again.

5. If the latest diagnosis reports:

   "healthy": true

   then the workflow is fixed and verified. Return:

   {{
       "action": "finish"
   }}

6. Never choose a tool that is not listed in AVAILABLE TOOLS.

7. Choose only ONE action at a time.

8. Use the previous tool results to determine the next action.

9. Do not repeat a successful tool unnecessarily.

10. If there is no safe or useful action to take, return:

    {{
        "action": "finish"
    }}

11. Return ONLY valid JSON.
Do not return markdown.
Do not return explanations.
"""

    response = ask_gemini(prompt).strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    decision = json.loads(response)

    # ---------------------------------------------------------
    # VALIDATE DECISION STRUCTURE
    # ---------------------------------------------------------

    action = decision.get("action")

    if action not in {"tool", "finish", "pause"}:
        return {
            "action": "pause",
            "reason": "Invalid decision action returned by Gemini",
        }

    # ---------------------------------------------------------
    # VALIDATE TOOL NAME
    # ---------------------------------------------------------

    if action == "tool":
        tool_name = decision.get("tool")

        registered_tools = get_available_tools()

        if tool_name not in registered_tools:
            return {
                "action": "pause",
                "reason": f"Unknown tool requested: {tool_name}",
            }

        if "arguments" not in decision:
            decision["arguments"] = {}

    return decision
