from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    project_id: Mapped[int] = mapped_column(
        nullable=False
    )

    user_message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    agent_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
