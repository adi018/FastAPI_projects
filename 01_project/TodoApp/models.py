from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<TodoItem(id={self.id}, title={self.title}, completed={self.completed})>"