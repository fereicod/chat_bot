from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column
from datetime import datetime, timezone
from sqlalchemy import Enum


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default=None, primary_key=True)
    topic: str
    stance: str = Field(
        default="Stand firm on your initial position throughout the conversation.",
        max_length=255
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id")
    message_role: str = Field(
        sa_column=Column(
            Enum("user", "model", name="message_role_enum"),
            nullable=False
        )
    )
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
