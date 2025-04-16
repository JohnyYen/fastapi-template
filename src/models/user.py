from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)


    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")