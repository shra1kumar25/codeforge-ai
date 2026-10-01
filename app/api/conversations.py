from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.conversation_service import (
    create_conversation,
    get_conversations,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


class ConversationCreate(BaseModel):
    project_id: int
    user_message: str
    agent_response: str | None = None


@router.post("/")
def create(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(
        db=db,
        project_id=conversation.project_id,
        user_message=conversation.user_message,
        agent_response=conversation.agent_response,
    )


@router.get("/{project_id}")
def list_conversations(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_conversations(
        db=db,
        project_id=project_id,
    )
