import sys
import os
from datetime import timedelta

# Allow tests to import pawpal_system.py from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def make_owner_with_tasks():
    """Helper: builds an Owner with two Pets and a few Tasks for reuse across tests."""
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="08:30", frequency="daily"))
    biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00", frequency="daily"))
    mochi.add_task(Task(title="Vet appointment", duration_minutes=45, priority="medium", time="14:00", frequency="once"))

    return owner


# --- Basic task/pet behavior ---

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


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    """Verify tasks are returned in chronological order regardless of insertion order."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]

    assert times == sorted(times)
    assert times == ["08:00", "08:30", "14:00"]


def test_sort_by_time_with_no_tasks_returns_empty_list():
    """Edge case: an owner with pets but no tasks should sort to an empty list."""
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Biscuit", species="dog"))
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == []


# --- Recurrence logic ---

def test_recurrence_creates_new_task_for_daily_frequency():
    """Confirm that marking a daily task complete creates a new task for the next occurrence,
    with its due_date correctly advanced by one day."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)

    walk_task = next(t for t in owner.get_all_tasks() if t.title == "Morning walk")
    original_due_date = walk_task.due_date
    walk_task.mark_complete()

    tasks_before = len(owner.get_all_tasks())
    next_task = scheduler.handle_recurring(walk_task)
    tasks_after = len(owner.get_all_tasks())

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == original_due_date + timedelta(days=1)
    assert tasks_after == tasks_before + 1


def test_recurrence_does_nothing_for_once_frequency():
    """Edge case: a one-time task should not generate a new occurrence, even if completed."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)

    vet_task = next(t for t in owner.get_all_tasks() if t.title == "Vet appointment")
    vet_task.mark_complete()

    result = scheduler.handle_recurring(vet_task)

    assert result is None


def test_recurrence_does_nothing_if_task_not_completed():
    """Edge case: an incomplete daily task should not generate a new occurrence yet."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)

    walk_task = next(t for t in owner.get_all_tasks() if t.title == "Morning walk")
    # Not marked complete

    result = scheduler.handle_recurring(walk_task)

    assert result is None


# --- Conflict detection ---

def test_detect_conflicts_flags_duplicate_times():
    """Verify that the Scheduler flags two tasks scheduled at the same time."""
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"))
    mochi.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="08:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_ignores_completed_tasks():
    """Edge case: a completed task shouldn't count toward a time-slot conflict."""
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    owner.add_pet(biscuit)

    old_task = Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00")
    old_task.mark_complete()
    biscuit.add_task(old_task)

    new_task = Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00")
    biscuit.add_task(new_task)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_detect_conflicts_returns_empty_when_no_overlap():
    """Happy path: distinct times should never be flagged as conflicts."""
    owner = make_owner_with_tasks()
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert conflicts == []