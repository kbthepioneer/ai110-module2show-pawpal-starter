from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    time: str  # "HH:MM" format, e.g. "08:00"
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""  # set automatically when added to a Pet

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
        task.pet_name = self.name
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
        """Returns all of the owner's tasks sorted chronologically by time (HH:MM)."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Returns tasks filtered by completion status and/or pet name."""
        tasks = self.owner.get_all_tasks()

        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]

        return tasks

    def detect_conflicts(self) -> List[str]:
        """Returns a list of warning messages for tasks scheduled at the same time."""
        warnings = []
        tasks = self.owner.get_all_tasks()

        # Only consider incomplete tasks — a completed task isn't really "scheduled" anymore
        active_tasks = [t for t in tasks if not t.completed]

        # Group tasks by their time slot
        time_map = {}
        for task in active_tasks:
            time_map.setdefault(task.time, []).append(task)

        # Any time slot with more than one task is a conflict
        for time_slot, tasks_at_time in time_map.items():
            if len(tasks_at_time) > 1:
                names = ", ".join(f"{t.title} ({t.pet_name})" for t in tasks_at_time)
                warnings.append(f"⚠️ Conflict at {time_slot}: {names}")

        return warnings

    def handle_recurring(self, task: Task) -> Optional[Task]:
        """If a completed task is daily/weekly, creates and returns the next occurrence."""
        if not task.completed or task.frequency == "once":
            return None

        # Calculate the next date offset based on frequency
        days_ahead = 1 if task.frequency == "daily" else 7

        # NOTE: since we only track time (not full datetime), we just create
        # a fresh Task instance for the next occurrence with completed reset.
        next_task = Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            time=task.time,
            frequency=task.frequency,
            completed=False,
            pet_name=task.pet_name,
        )

        # Find the pet this task belongs to and add the new occurrence
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                break

        return next_task