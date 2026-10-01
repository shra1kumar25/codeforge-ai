from sqlalchemy.orm import Session

from app.services.conversation_service import (
    create_conversation,
    get_conversations,
)
from app.services.gemini_service import ask_gemini


def run_agent(
    db: Session,
    project_id: int,
    user_message: str,
    tool_results=None,
):
    history = get_conversations(
        db=db,
        project_id=project_id,
    )

    context = ""

    for conversation in history:
        context += f"""
User: {conversation.user_message}
Agent: {conversation.agent_response}
"""

    tool_context = ""

    if tool_results:
        tool_context = f"""
Tool execution results:
{tool_results}
"""

    prompt = f"""
You are CodeForge AI, an AI coding agent.

Previous conversation history:
{context}

New user request:
{user_message}

{tool_context}

Use the previous conversation and tool execution results when useful.

Provide a clear and helpful response to the user's request.
"""

    agent_response = ask_gemini(prompt)

    conversation = create_conversation(
        db=db,
        project_id=project_id,
        user_message=user_message,
        agent_response=agent_response,
    )

    return conversation
