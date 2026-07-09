# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three core actions a user needs are: (1) adding a pet along with its care tasks,
(2) viewing a generated daily schedule ordered by priority and time, and (3) marking
tasks complete, including handling recurring tasks. These map to four classes:
Task, Pet, Owner, and Scheduler.

I designed four classes: Task represents a single care activity with its own
priority, time, and completion status. Pet holds a list of Tasks belonging to
that animal. Owner manages multiple Pets and can pull tasks across all of them.
Scheduler is separate from these data classes — it holds a reference to the
Owner and is responsible for the "smart" behavior: sorting, filtering, conflict
detection, and recurring task logic.

**b. Design changes**

During UI integration, I discovered that free-text time input allowed inconsistent
formats (e.g. "8:00" vs "08:00"), which caused sorting and conflict detection to
silently fail since they compared raw strings. I fixed this by normalizing all
time input through Python's datetime.strptime/strftime before creating a Task,
ensuring every task's time is stored in a consistent "HH:MM" format.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers time (to sort and detect conflicts) and priority (low/medium/high,
displayed alongside each task). I prioritized time-based conflict detection first since
double-booking a pet's care is the most concrete, checkable failure mode; priority is
currently informational rather than used to reorder tasks, since the base requirements
only asked for time-based sorting.

**b. Tradeoffs**

My scheduler only tracks time-of-day (HH:MM) for sorting and conflict comparisons, not
overlapping durations — a 30-minute walk and a 10-minute feeding at the same start time
are flagged as a conflict even though a real owner might handle them back-to-back. This
is a reasonable tradeoff for a simple daily planner like PawPal+, since exact-time
matching is easy to reason about and catches the most obvious double-booking cases,
even though a more advanced version could check for overlapping time ranges instead.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant throughout every phase: brainstorming the four-class
design in Phase 1, generating the full implementation of Task/Pet/Owner/Scheduler in
Phase 2, wiring the Streamlit UI to that logic in Phase 3, and writing the sorting,
filtering, conflict detection, and recurring-task algorithms in Phase 4. The most
helpful prompts were specific ones tied to a concrete symptom — for example, describing
an actual bug I saw in the app (a false conflict warning appearing after a recurring
task was created) rather than just asking it to "check my code." Giving it the exact
output I was seeing led to a much faster, more targeted fix than a general review would
have.

**b. Judgment and verification**

I didn't accept the recurring-task logic as-is on the first pass. The initial version
recreated a task with completed=False but never actually calculated a new calendar
date, even though the project instructions explicitly called for using timedelta to
compute "today + 1 day." I caught that gap myself by re-reading the instructions against
my own code, asked for it to be fixed properly with a real due_date field, and verified
it by running main.py and confirming the new task showed tomorrow's actual date instead
of just today's again.

---

## 4. Testing and Verification

**a. What you tested**

I tested: task completion (mark_complete changes status), task addition (adding a task
increases a pet's task count), sorting correctness (tasks return in chronological order,
including an empty-list edge case), recurrence logic (a completed daily task generates
a new task with its due_date advanced by exactly one day, while a "once" task or an
incomplete task generates nothing), and conflict detection (two tasks at the same time
are flagged, but a completed task is correctly excluded from counting as a conflict).
These mattered because they're the core "smart" behaviors of the app — if any of them
silently failed, the schedule would look right but actually be wrong (e.g. missing a
real double-booking, or falsely flagging one).

**b. Confidence**

I'm fairly confident (4/5) in the current implementation — all 10 tests pass, covering
both happy paths and several edge cases I specifically added after finding real bugs
during manual testing (the string time-formatting bug, the completed-task conflict bug).
If I had more time, I'd test: multiple recurring tasks chained across several days,
weekly recurrence specifically (I've mostly exercised the daily path), and a larger
number of pets/tasks to make sure sorting and conflict detection still perform correctly
at scale.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with catching and fixing real bugs through actual manual testing in
the Streamlit UI, not just trusting that the code "looked right." The time-format bug
(8:00 vs 08:00 breaking both sorting and conflict detection) and the timedelta gap
in recurring tasks were both things I noticed by comparing what the instructions
actually asked for against what my code was doing, rather than just accepting AI-generated
code at face value.

**b. What you would improve**

If I did another iteration, I'd make priority actually affect the schedule (not just
display it), and I'd add real weekly-recurrence testing since I mostly verified the
daily case. I'd also consider giving Task a proper unique ID instead of relying on
pet_name string matching, which is a little fragile if two pets ever shared a name.

**c. Key takeaway**

The biggest thing I learned about being the "lead architect" is that AI-generated code
can look complete and still miss something the instructions explicitly asked for — like
the timedelta requirement — so it's on me to actually re-read the spec against my own
code rather than assuming a working demo means every requirement was met.