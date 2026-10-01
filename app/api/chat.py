from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.agent_memory_service import run_agent
from app.services.intent_service import detect_intent
from app.services.planning_service import create_plan
from app.services.tool_selection_service import select_tools
from app.services.agent_loop import run_execution_loop
from app.services.autonomous_agent import run_autonomous_agent
from app.workflow.workflow_schema import Workflow

router = APIRouter()


class ChatRequest(BaseModel):
    project_id: int
    prompt: str


class AutonomousAgentRequest(BaseModel):
    goal: str
    workflow: Workflow | None = None

class ChatResponse(BaseModel):
    id: int
    project_id: int
    user_message: str
    agent_response: str | None


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    intent = detect_intent(request.prompt)

    print("\n===== DETECTED INTENT =====")
    print(intent)

    plan = create_plan(
        user_message=request.prompt,
        intent=intent,
    )

    print("\n===== GENERATED PLAN =====")
    print(plan)

    selected_tools = select_tools(
        user_message=request.prompt,
        plan=plan,
    )

    print("\n===== SELECTED TOOLS =====")
    print(selected_tools)

    tool_results = run_execution_loop(
        selected_tools=selected_tools,
    )

    print("\n===== TOOL RESULTS =====")
    print(tool_results)

    conversation = run_agent(
        db=db,
        project_id=request.project_id,
        user_message=request.prompt,
        tool_results=tool_results,
    )

    return ChatResponse(
        id=conversation.id,
        project_id=conversation.project_id,
        user_message=conversation.user_message,
        agent_response=conversation.agent_response,
    )


@router.post("/agent")
def autonomous_agent(
    request: AutonomousAgentRequest,
):
    result = run_autonomous_agent(
        goal=request.goal,
        workflow=request.workflow,
    )

    return result
