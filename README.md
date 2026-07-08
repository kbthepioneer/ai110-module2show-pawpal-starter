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
  ⬜ 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Marking 'Morning walk' complete...
  ✅ 08:00 — Morning walk (Biscuit, 30 min) [priority: high]
  ⬜ 08:30 — Feeding (Biscuit, 10 min) [priority: high]
  ⬜ 14:00 — Vet appointment (Mochi, 45 min) [priority: medium]
Handling recurrence for 'Morning walk'...
  New task created for tomorrow: Morning walk at 08:00
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
- Recurrence logic (daily tasks generate a new occurrence; one-time and incomplete tasks do not)
- Conflict detection (duplicate times are flagged; completed tasks are correctly excluded from conflicts; no false positives on distinct times)

Sample test output:

```
================================================== test session starts ==================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\kbayona\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items

tests\test_pawpal.py ..........                                                                                    [100%]

=================================================== 10 passed in 0.09s ===================================================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — All core behaviors and several edge cases are verified. I'd want to test multi-day recurrence chains and larger datasets before rating this 5/5.
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically by their "HH:MM" time string |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status and/or pet name |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks scheduled at the same time; only considers incomplete tasks |
| Recurring tasks | `Scheduler.handle_recurring()` | Creates a fresh incomplete Task instance for daily/weekly tasks once marked complete |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
