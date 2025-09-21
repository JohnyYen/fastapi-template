from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from src.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):

    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")