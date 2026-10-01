READ_ONLY_TOOLS = {
    "read_file",
    "search_code",
    "list_directory",
    "inspect_workflow",
    "diagnose_workflow",
}


MUTATION_TOOLS = {
    "write_file",
    "create_file",
    "execute_command",
}


def get_tool_tier(tool_name: str):
    if tool_name in READ_ONLY_TOOLS:
        return "read_only"

    if tool_name in MUTATION_TOOLS:
        return "mutation"

    return "unknown"


def requires_approval(tool_name: str):
    return get_tool_tier(tool_name) == "mutation"
