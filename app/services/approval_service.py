from uuid import uuid4

from app.services.tool_execution_service import execute_selected_tool
from app.services.verification_service import verify_tool_result


APPROVAL_QUEUE = {}


def create_approval_request(
    tool_name: str,
    arguments: dict,
):
    approval_id = str(uuid4())

    request = {
        "id": approval_id,
        "tool": tool_name,
        "arguments": arguments,
        "status": "pending",
    }

    APPROVAL_QUEUE[approval_id] = request

    return request


def get_approval_request(approval_id: str):
    return APPROVAL_QUEUE.get(approval_id)


def list_approval_requests():
    return list(APPROVAL_QUEUE.values())


def approve_request(approval_id: str):
    request = APPROVAL_QUEUE.get(approval_id)

    if not request:
        return None

    request["status"] = "approved"

    result = execute_selected_tool(
        tool_name=request["tool"],
        arguments=request["arguments"],
    )

    verification = verify_tool_result({
        "result": result,
    })

    request["result"] = result
    request["verification"] = verification

    return request


def reject_request(approval_id: str):
    request = APPROVAL_QUEUE.get(approval_id)

    if not request:
        return None

    request["status"] = "rejected"

    return request
