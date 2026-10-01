from app.services.tool_execution_service import execute_selected_tool
from app.services.verification_service import verify_tool_result
from app.services.tool_policy import requires_approval
from app.services.approval_service import create_approval_request
from app.tools.tool_registry import get_available_tools


def execute_agent_tool(
    tool_name: str,
    arguments: dict,
):
    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    available_tools = get_available_tools()

    if tool_name not in available_tools:
        return {
            "tool": tool_name,
            "arguments": arguments,
            "status": "blocked",
            "result": None,
            "verification": {
                "verified": False,
                "message": f"Unknown tool blocked: {tool_name}",
            },
        }

    # ---------------------------------------------------------
    # APPROVAL CHECK
    # ---------------------------------------------------------

    if requires_approval(tool_name):
        approval = create_approval_request(
            tool_name=tool_name,
            arguments=arguments,
        )

        return {
            "tool": tool_name,
            "arguments": arguments,
            "status": "approval_required",
            "approval": approval,
            "result": None,
            "verification": {
                "verified": False,
                "message": "Tool requires user approval",
            },
        }

    # ---------------------------------------------------------
    # TOOL EXECUTION
    # ---------------------------------------------------------

    result = execute_selected_tool(
        tool_name=tool_name,
        arguments=arguments,
    )

    # ---------------------------------------------------------
    # VERIFICATION
    # ---------------------------------------------------------

    verification = verify_tool_result({
        "result": result,
    })

    return {
        "tool": tool_name,
        "arguments": arguments,
        "status": "executed",
        "result": result,
        "verification": verification,
    }


def execute_selected_tools(
    selected_tools: dict,
):
    results = []

    for tool in selected_tools.get("tools", []):
        tool_name = tool.get("name")
        arguments = tool.get("arguments", {})

        result = execute_agent_tool(
            tool_name=tool_name,
            arguments=arguments,
        )

        results.append(result)

    return results
