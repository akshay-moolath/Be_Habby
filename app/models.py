from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint # Import Relationship and UniqueConstraint
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import func # Import func for database-specific operations (like current_timestamp)


# --- 1. User Model ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str

    # Relationship to Habits: This allows you to access user.habits
    habits: List["Habit"] = Relationship(back_populates="owner")
    
    # Relationship to MoodEntries
    mood_entries: List["MoodEntry"] = Relationship(back_populates="user")


# --- 2. Habit Model ---
class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str = "active"
    
    # Foreign Key to User
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # **NEW FIELD for user-scoped ID**
    user_habit_number: int = Field(index=True, nullable=False)
    
    category: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Use a default_factory that calls the SQL function for better DB management
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column_kwargs={"onupdate": datetime.utcnow} # Optional: For automatic update on record change
    )

    # Relationship to User: This allows you to access habit.owner
    owner: User = Relationship(back_populates="habits")
    
    # Relationship to MoodEntries: This allows you to access habit.mood_entries
    mood_entries: List["MoodEntry"] = Relationship(back_populates="habit")
    
    # **NEW: Unique Constraint** (Ensures user A cannot have two habits both numbered 1)
    __table_args__ = (
        UniqueConstraint('owner_id', 'user_habit_number', name='_owner_habit_number_uc'),
    )


class HabitCreate(BaseModel):
    name: str
    status: Optional[str] = "active"
    category: Optional[str] = None


# --- 3. MoodEntry Model ---
class MoodEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key to User (Mood entry must belong to a user)
    user_id: int = Field(foreign_key="user.id")
    
    # Foreign Key to Habit (Mood entry can optionally be linked to a habit)
    habit_id: Optional[int] = Field(default=None, foreign_key="habit.id")
    
    text: str
    sentiment: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User: This allows you to access mood_entry.user
    user: User = Relationship(back_populates="mood_entries")
    
    # Relationship to Habit: This allows you to access mood_entry.habit
    habit: Optional[Habit] = Relationship(back_populates="mood_entries")