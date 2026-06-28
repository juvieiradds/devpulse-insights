from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    alerts = relationship(
        "Alert",
        back_populates="owner",
        cascade="all, delete-orphan",
    )