from app.tools.tool_registry import execute_tool


def execute_selected_tool(
    tool_name: str,
    arguments: dict,
):
    try:
        return execute_tool(
            tool_name=tool_name,
            arguments=arguments,
        )

    except Exception as error:
        return {
            "error": str(error),
            "success": False,
        }
