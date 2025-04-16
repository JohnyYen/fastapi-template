from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class Role(Base):
    
    name_role = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="role")