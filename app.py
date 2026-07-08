from datetime import datetime
import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — a pet care planning assistant. Add pets, assign
care tasks, and generate a smart daily schedule.
"""
)

# --- Session state setup ---
# Streamlit reruns the whole script on every interaction, so we store the
# Owner object in session_state to keep it from being wiped out each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="", key="new_pet_name")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet"):
    if new_pet_name:
        owner.add_pet(Pet(name=new_pet_name, species=new_pet_species))
        st.success(f"Added {new_pet_name} ({new_pet_species})!")
    else:
        st.warning("Enter a pet name first.")

st.divider()

# --- Add a task ---
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before assigning tasks.")
else:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Which pet?", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col5:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        # Normalize time input so "8:00" and "08:00" are treated as identical
        try:
            normalized_time = datetime.strptime(task_time.strip(), "%H:%M").strftime("%H:%M")
        except ValueError:
            st.error("Please enter time as HH:MM (e.g. 08:00 or 14:30).")
            normalized_time = None

        if normalized_time:
            # Find the selected pet and add the task to it
            for pet in owner.pets:
                if pet.name == selected_pet_name:
                    pet.add_task(
                        Task(
                            title=task_title,
                            duration_minutes=int(duration),
                            priority=priority,
                            time=normalized_time,
                            frequency=frequency,
                        )
                    )
                    st.success(f"Added '{task_title}' to {selected_pet_name}!")
                    break

st.divider()

# --- Build and display schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    if not sorted_tasks:
        st.info("No tasks yet. Add a pet and some tasks first.")
    else:
        st.write("### Today's Schedule")
        table_data = [
            {
                "Time": t.time,
                "Task": t.title,
                "Pet": t.pet_name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Completed": "✅" if t.completed else "⬜",
            }
            for t in sorted_tasks
        ]
        st.table(table_data)

        # Show any scheduling conflicts
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts found.")