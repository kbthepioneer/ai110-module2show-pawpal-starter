from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    time: str  # "HH:MM" format, e.g. "08:00"
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Marks this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet and the list of care tasks assigned to it."""
    name: str
    species: str  # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a new task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks belonging to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents a pet owner and the pets they manage."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' that organizes and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> List[Task]:
        """Returns all of the owner's tasks sorted chronologically by time."""
        pass  # implemented in Phase 4

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Returns tasks filtered by completion status and/or pet name."""
        pass  # implemented in Phase 4

    def detect_conflicts(self) -> List[str]:
        """Returns a list of warning messages for tasks scheduled at the same time."""
        pass  # implemented in Phase 4

    def handle_recurring(self, task: Task) -> Optional[Task]:
        """If a completed task is daily/weekly, creates and returns the next occurrence."""
        pass  # implemented in Phase 4