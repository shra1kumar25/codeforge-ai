from app.services.agent_executor import execute_agent_tool
from app.tools.search_tools import search_code


MAX_RETRIES = 1


def recover_from_failure(
    tool_name: str,
    arguments: dict,
    failure_result: dict,
):
    if tool_name == "read_file":
        file_path = arguments.get("file_path")

        if file_path:
            file_name = file_path.split("/")[-1]

            search_result = search_code(file_name)

            if search_result["results"]:
                corrected_path = search_result["results"][0]["file"]

                return {
                    "action": "retry_with_corrected_path",
                    "arguments": {
                        "file_path": corrected_path,
                    },
                }

    return {
        "action": "retry_same",
        "arguments": arguments,
    }


def run_execution_loop(
    selected_tools: dict,
):
    results = []

    for tool in selected_tools.get("tools", []):

        tool_name = tool.get("name")
        arguments = tool.get("arguments", {})

        attempt = 0

        while attempt <= MAX_RETRIES:

            result = execute_agent_tool(
                tool_name=tool_name,
                arguments=arguments,
            )

            results.append(result)

            if result["verification"]["verified"]:
                break

            if attempt >= MAX_RETRIES:
                break

            recovery = recover_from_failure(
                tool_name=tool_name,
                arguments=arguments,
                failure_result=result,
            )

            arguments = recovery["arguments"]

            attempt += 1

    return results
