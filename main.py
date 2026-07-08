from pawpal_system import Task, Pet, Owner, Scheduler


def print_schedule(tasks):
    """Prints a list of tasks in a clean, readable format."""
    if not tasks:
        print("  No tasks scheduled.")
        return
    for task in tasks:
        status = "✅" if task.completed else "⬜"
        print(f"  {status} {task.time} — {task.title} ({task.pet_name}, {task.duration_minutes} min) [priority: {task.priority}]")


def main():
    # Create an owner
    owner = Owner(name="Jordan")

    # Create two pets
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")

    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Add tasks to each pet (at least 3 total, with different times)
    biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00", frequency="daily"))
    biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="08:30", frequency="daily"))
    mochi.add_task(Task(title="Vet appointment", duration_minutes=45, priority="medium", time="14:00", frequency="once"))

    # Build the scheduler
    scheduler = Scheduler(owner)

    # Print today's schedule, sorted by time
    print(f"Today's Schedule for {owner.name}:\n")
    sorted_tasks = scheduler.sort_by_time()
    print_schedule(sorted_tasks)

    # Demonstrate marking a task complete
    print("\nMarking 'Morning walk' complete...")
    sorted_tasks[0].mark_complete()
    print_schedule(scheduler.sort_by_time())

    # Demonstrate recurring task logic
    print("\nHandling recurrence for 'Morning walk'...")
    next_occurrence = scheduler.handle_recurring(sorted_tasks[0])
    if next_occurrence:
        print(f"  New task created for tomorrow: {next_occurrence.title} at {next_occurrence.time}")

    # Demonstrate conflict detection
    print("\nChecking for scheduling conflicts...")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found.")


if __name__ == "__main__":
    main()