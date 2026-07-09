# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Pet & task management** — Add multiple pets and assign each their own care tasks (title, duration, priority, time, and frequency)
- **Chronological scheduling** — `Scheduler.sort_by_time()` orders all tasks across every pet by time of day
- **Priority-based scheduling** — `Scheduler.sort_by_priority()` orders tasks by priority (high → medium → low) first, then by time within each priority level
- **Filtering** — `Scheduler.filter_tasks()` lets you view tasks by completion status and/or by pet
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any tasks scheduled at the exact same time, so a pet owner never double-books care
- **Recurring tasks with real dates** — `Scheduler.handle_recurring()` uses Python's `timedelta` to automatically generate the next occurrence of a daily/weekly task, advancing the calendar date correctly
- **Task completion tracking** — Mark tasks done directly in the UI, which also triggers recurrence logic for repeating tasks

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule for Jordan:
  ⬜ 2026-07-08 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 2026-07-08 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 2026-07-08 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Marking 'Morning walk' complete...
  ✅ 2026-07-08 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 2026-07-08 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 2026-07-08 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Handling recurrence for 'Morning walk'...
  New task created for 2026-07-09: Morning walk at 08:00
Checking for scheduling conflicts...
  No conflicts found.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

My test suite covers:
- Basic task/pet behavior (marking complete, adding tasks)
- Sorting correctness (chronological order, empty-list edge case)
- Recurrence logic (daily tasks generate a new occurrence with the correct due_date advanced by timedelta; one-time and incomplete tasks do not)
- Conflict detection (duplicate times are flagged; completed tasks are correctly excluded from conflicts; no false positives on distinct times)

Sample test output:

```
================================================== test session starts ==================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\kbayona\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items

tests\test_pawpal.py ..........                                                                                    [100%]

=================================================== 10 passed in 0.08s ===================================================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — All core behaviors and several edge cases are verified. I'd want to test multi-day recurrence chains and larger datasets before rating this 5/5.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically by their "HH:MM" time string |
| Priority scheduling | `Scheduler.sort_by_priority()` | Sorts tasks by priority (high → medium → low) first, then by time within each priority level |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status and/or pet name |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks scheduled at the same time; only considers incomplete tasks |
| Recurring tasks | `Scheduler.handle_recurring()` | Uses `timedelta` to create a new Task instance with `due_date` advanced by 1 day (daily) or 7 days (weekly) once the original is marked complete |

## 📸 Demo Walkthrough

1. **Add a pet** — Enter a pet's name and species (dog/cat/other), then click "Add pet." The pet is stored in the app's session so it persists as you keep interacting.
2. **Add tasks** — Select which pet the task belongs to, then fill in the task title, duration, priority, time, and frequency (once/daily/weekly), and click "Add task."
3. **Mark tasks complete** — In the "Manage Tasks" section, every task shows its status and a "Mark done" button. Clicking it calls `Task.mark_complete()` and immediately updates the checkmark.
4. **Generate a schedule** — Optionally filter by pet or completion status, then click "Generate schedule" to see a sorted table of tasks for the day.
5. **Conflict warnings** — If two tasks land on the same time slot, the app displays a warning (e.g. "Conflict at 08:00: Morning walk (Biscuit), Feeding (Mochi)") instead of silently allowing a double-booking.
6. **Recurring tasks** — Marking a daily/weekly task complete automatically creates its next occurrence with the correct future date, which then appears in the next generated schedule.

### Sample CLI output (from `main.py`)

```
Today's Schedule for Jordan:
  ⬜ 2026-07-08 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 2026-07-08 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 2026-07-08 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Marking 'Morning walk' complete...
  ✅ 2026-07-08 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 2026-07-08 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 2026-07-08 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Handling recurrence for 'Morning walk'...
  New task created for 2026-07-09: Morning walk at 08:00
Checking for scheduling conflicts...
  No conflicts found.
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->