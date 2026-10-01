from app.tools.read_file_tool import read_file
from app.tools.write_file_tool import write_file
from app.tools.create_file_tool import create_file
from app.tools.list_directory_tool import list_directory
from app.tools.execute_command_tool import execute_command

from app.workflow.workflow_inspector import inspect_workflow
from app.workflow.workflow_diagnosis import diagnose_workflow
from app.workflow.workflow_fixer import fix_workflow


TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "create_file": create_file,
    "list_directory": list_directory,
    "execute_command": execute_command,
    "inspect_workflow": inspect_workflow,
    "diagnose_workflow": diagnose_workflow,
    "fix_workflow": fix_workflow,
}


def get_tool(tool_name: str):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    return TOOLS[tool_name]


def execute_tool(
    tool_name: str,
    arguments: dict,
):
    tool_function = get_tool(tool_name)

    return tool_function(**arguments)


def get_available_tools():
    return list(TOOLS.keys())
