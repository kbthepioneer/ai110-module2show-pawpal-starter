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

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
