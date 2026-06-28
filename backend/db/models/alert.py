from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from db.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    keyword = Column(String(100), nullable=False, index=True)

    threshold = Column(Integer, nullable=False, server_default=text("20"))

    is_active = Column(Boolean, nullable=False, server_default=expression.true())

    owner = relationship("User", back_populates="alerts")