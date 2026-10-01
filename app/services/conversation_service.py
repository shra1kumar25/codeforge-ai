from sqlalchemy.orm import Session

from app.database.models import Conversation


def create_conversation(
    db: Session,
    project_id: int,
    user_message: str,
    agent_response: str | None = None,
):
    conversation = Conversation(
        project_id=project_id,
        user_message=user_message,
        agent_response=agent_response,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversations(
    db: Session,
    project_id: int,
):
    return (
        db.query(Conversation)
        .filter(Conversation.project_id == project_id)
        .order_by(Conversation.id)
        .all()
    )
