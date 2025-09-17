from app import db
from datetime import datetime
import enum

# Handle different SQLAlchemy versions
try:
    from sqlalchemy import Enum
except ImportError:
    from sqlalchemy.types import Enum

class TaskStatus(enum.Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)  # 1 = highest priority
    duration = db.Column(db.Integer, nullable=False, default=1)  # Duration in time units
    arrival_time = db.Column(db.Integer, nullable=False, default=0)  # For FCFS scheduling
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.Integer, nullable=True)  # When task execution started
    completion_time = db.Column(db.Integer, nullable=True)  # When task execution completed
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'priority': self.priority,
            'duration': self.duration,
            'arrival_time': self.arrival_time,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'start_time': self.start_time,
            'completion_time': self.completion_time
        }
    
    def __repr__(self):
        return f'<Task {self.name}>'
