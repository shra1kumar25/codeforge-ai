def verify_tool_result(tool_result: dict):
    result = tool_result.get("result")

    # Tool returned an error
    if isinstance(result, dict) and "error" in result:
        return {
            "verified": False,
            "message": result["error"],
        }

    # Tool explicitly reported success
    if isinstance(result, dict) and result.get("success") is True:
        return {
            "verified": True,
            "message": "Tool executed successfully",
        }

    # Tool returned a non-empty result
    if result is not None:
        if isinstance(result, (list, str, dict)) and len(result) > 0:
            return {
                "verified": True,
                "message": "Tool executed successfully",
            }

    # No usable result
    return {
        "verified": False,
        "message": "Tool execution returned no result",
    }
