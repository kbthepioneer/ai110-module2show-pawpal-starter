import sys
import os

# Allow tests to import pawpal_system.py from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(title="Feeding", duration_minutes=10, priority="high", time="08:00")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.get_tasks()) == 0

    task = Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00")
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1