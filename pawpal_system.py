from dataclasses import dataclass, field
from typing import List, Optional
from datetime import time


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    category: str  # "feeding", "walk", "medication", "grooming", "enrichment"
    recurring: bool = False  # does this task repeat daily?
    preferred_time: Optional[str] = None  # e.g. "morning", "afternoon", "evening"

    def is_high_priority(self) -> bool:
        return self.priority == "high"


@dataclass
class Pet:
    """Represents a pet with its care needs."""
    name: str
    species: str  # "dog", "cat", "other"
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_high_priority_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.is_high_priority()]

    def total_care_time(self) -> int:
        return sum(t.duration_minutes for t in self.tasks)


@dataclass
class Owner:
    """Represents a pet owner with preferences."""
    name: str
    available_minutes: int = 120  # total time available per day
    preferred_start: str = "08:00"  # when to start the day's schedule
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)


class Scheduler:
    """Builds and manages a daily care schedule."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule = []  # list of scheduled task dicts

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high first), then duration (shortest first)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (priority_order[t.priority], t.duration_minutes))

    def filter_tasks(self, tasks: List[Task]) -> List[Task]:
        """Filter out tasks that don't fit in available time."""
        selected = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                selected.append(task)
                time_used += task.duration_minutes
        return selected

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks that together exceed available time."""
        conflicts = []
        total = sum(t.duration_minutes for t in tasks)
        if total > self.owner.available_minutes:
            conflicts.append(
                f"Total task time ({total} min) exceeds available time ({self.owner.available_minutes} min)."
            )
        return conflicts

    def build_schedule(self) -> List[dict]:
        """Build a daily schedule for all pets."""
        self.schedule = []
        all_tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append({"pet": pet.name, "task": task})

        sorted_tasks = self.sort_tasks([item["task"] for item in all_tasks])
        filtered_tasks = self.filter_tasks(sorted_tasks)

        # assign time slots starting from preferred_start
        hour, minute = map(int, self.owner.preferred_start.split(":"))
        current_minutes = hour * 60 + minute

        for task in filtered_tasks:
            slot_hour = current_minutes // 60
            slot_min = current_minutes % 60
            self.schedule.append({
                "time": f"{slot_hour:02d}:{slot_min:02d}",
                "task": task.title,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "category": task.category,
            })
            current_minutes += task.duration_minutes

        return self.schedule

    def explain_schedule(self) -> str:
        """Return a human-readable explanation of the schedule."""
        if not self.schedule:
            return "No schedule generated yet."
        lines = [f"Daily plan for {self.owner.name}'s pet(s):\n"]
        for item in self.schedule:
            lines.append(
                f"  {item['time']} — {item['task']} ({item['duration']} min) [priority: {item['priority']}]"
            )
        return "\n".join(lines)