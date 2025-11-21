import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_calendar import calendar 
from calendar_options import calendar_options, custom_css

# ------------------------------------
# Basic Setup & Global CSS Styling
# ------------------------------------
# Configure Streamlit page settings and apply custom UI styling.
st.set_page_config(page_title="Sabin's To-Do App", layout="centered")

st.markdown("""
<style>
    /* Global card container styles */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #f0f2f6;
        padding: 10px 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        border-color: #dfe6ed;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] * {
        color: #333333;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    /* Secondary button styling */
    button[kind="secondary"] {
        border: none !important;
        background: transparent !important;
        color: #adb5bd !important;
        padding: 0 !important;
    }
    button[kind="secondary"]:hover {
        color: #ff6b6b !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Sabin's To-Do & Schedule Manager")

DB = "todo.db"

# ------------------------------------
# Database Initialization
# ------------------------------------
# Creates the SQLite database and `todos` table if they do not exist.
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            due_date TEXT,
            is_done INTEGER,
            priority TEXT DEFAULT 'Medium',
            category TEXT DEFAULT 'General'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------------------------
# Session State & Menu Management
# ------------------------------------
# Initialize the menu state on first load.
if "menu" not in st.session_state:
    st.session_state["menu"] = "Calendar View"

# Only two menus are exposed to the user.
menu_items = ["Calendar View", "Task Stats"]

sidebar_value = st.session_state["menu"]
if sidebar_value not in menu_items:
    sidebar_value = "Calendar View"

# When the menu changes, we clear temporary stored values.
def on_menu_change():
    st.session_state["menu"] = st.session_state["sidebar_selection"]
    st.session_state["prefill_date"] = None
    st.session_state["edit_id"] = None

# Sidebar navigation component.
st.sidebar.radio(
    "Menu", 
    menu_items, 
    index=menu_items.index(sidebar_value),
    key="sidebar_selection",
    on_change=on_menu_change
)

# ------------------------------------
# Menu 1: Calendar View (Main Page)
# ------------------------------------
if st.session_state["menu"] == "Calendar View":

    # Load all tasks from the database.
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM todos", conn)
    conn.close()

    # Convert due_date strings into Python date objects.
    df["due_date"] = pd.to_datetime(df["due_date"]).dt.date

    # Get today's date and tomorrow's date.
    today = datetime.now().date()
    tomorrow = today + pd.Timedelta(days=1)

    # Filter tasks for summary metrics.
    today_tasks = df[(df["due_date"] == today) & (df["is_done"] == 0)]
    tomorrow_tasks = df[(df["due_date"] == tomorrow) & (df["is_done"] == 0)]
    overdue_tasks = df[(df["due_date"] < today) & (df["is_done"] == 0)]

    # Summary banner HTML block.
    summary_html = f"""
<div style="background: #f8f9fa; padding: 18px 22px; border-radius: 12px; border: 1px solid #e4e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 16px;">
    <h3 style="margin-top:0;">🔔 Today's Summary</h3>
    <p style="font-size:16px; margin:6px 0;">📌 <b>Tasks Due Today:</b> {len(today_tasks)}</p>
    <p style="font-size:16px; margin:6px 0;">⏳ <b>Due Tomorrow:</b> {len(tomorrow_tasks)}</p>
    <p style="font-size:16px; margin:6px 0;">⚠️ <b>Overdue Tasks:</b> {len(overdue_tasks)}</p>
</div>
"""
    st.markdown(summary_html, unsafe_allow_html=True)

    # Calendar section title.
    st.subheader("📅 Calendar View")

    # ------------------------------------
    # Build FullCalendar event list
    # ------------------------------------
    events = []
    priority_colors = {"High": "#ff6b6b", "Medium": "#ffd93d", "Low": "#6bcb77"}

    for _, row in df.iterrows():
        # Completed tasks appear grey; others use priority color.
        color = "#a4b0be" if bool(row["is_done"]) else priority_colors.get(row["priority"], "#a4b0be")

        # Add task to the FullCalendar event list.
        events.append({
            "id": str(row["id"]),
            "title": row["task"],
            "start": row["due_date"].strftime("%Y-%m-%d"),
            "backgroundColor": color,
            "borderColor": color,
            "extendedProps": {
                "category": row["category"],
                "priority": row["priority"],
                "is_done": bool(row["is_done"])
            }
        })

    # Render FullCalendar using the provided configuration.
    calendar_state = calendar(
        events=events,
        options=calendar_options,
        custom_css=custom_css,
        key="my_calendar"
    )

    # ------------------------------------
    # Calendar Interaction Handlers
    # ------------------------------------
    # 1. User clicks a date → prefill Add Task page.
    if calendar_state.get("callback") == "dateClick":
        date_data = calendar_state.get("dateClick", {})
        clicked_date = date_data.get("dateStr")

        # Safety fallback when dateStr is unavailable.
        if not clicked_date and "date" in date_data:
            clicked_date = date_data["date"].split("T")[0]
        
        if clicked_date:
            st.session_state["prefill_date"] = clicked_date
            st.session_state["menu"] = "Add Task"
            st.rerun()

    # 2. User clicks an event → open Edit Task page.
    elif calendar_state.get("callback") == "eventClick":
        st.session_state["edit_id"] = calendar_state["eventClick"]["event"]["id"]
        st.session_state["menu"] = "Edit Task"
        st.rerun()

    # 3. User drags an event → update due date.
    elif calendar_state.get("callback") == "eventDrop":
        event_id = calendar_state["eventDrop"]["event"]["id"]
        raw = calendar_state["eventDrop"]["event"]["start"]
        new_start = raw.split("T")[0] if "T" in raw else raw

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("UPDATE todos SET due_date = ? WHERE id = ?", (new_start, event_id))
        conn.commit()
        conn.close()

        st.toast(f"📅 Task moved to {new_start}")
        st.rerun()

# ------------------------------------
# Menu 2: Add Task Page
# ------------------------------------
elif st.session_state["menu"] == "Add Task":
    if st.button("← Back to Calendar"):
        st.session_state["menu"] = "Calendar View"
        st.rerun()

    st.subheader("➕ Add New Task")

    # Autofill date when coming from calendar click.
    default_date = st.session_state.get("prefill_date")
    if default_date:
        try:
            default_date_obj = datetime.strptime(default_date, "%Y-%m-%d").date()
        except:
            default_date_obj = datetime.now().date()
        st.info(f"📅 Selected Date: {default_date}")
        st.session_state["prefill_date"] = None
    else:
        default_date_obj = datetime.now().date()

    with st.container(border=True):
        st.markdown("### New Task Details")
        task = st.text_input("Task Name", placeholder="Enter task description...")

        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input("Due Date", value=default_date_obj)
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        with col2:
            category = st.selectbox(
                "Category",
                ["General", "Work", "Home", "Study", "Baby", "Finance", "Other"]
            )

        if st.button("Save Task", type="primary", use_container_width=True):
            if task.strip() == "":
                st.warning("Task cannot be empty.")
            else:
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO todos (task, due_date, is_done, priority, category)
                    VALUES (?, ?, 0, ?, ?)
                """, (task, due_date.strftime("%Y-%m-%d"), priority, category))
                conn.commit()
                conn.close()
                st.success("Task added!")
                st.session_state["menu"] = "Calendar View"
                st.rerun()

# ------------------------------------
# Menu 3: Edit Task Page
# ------------------------------------
elif st.session_state["menu"] == "Edit Task":
    task_id = st.session_state.get("edit_id")

    if not task_id:
        st.warning("Please select a task first.")
        if st.button("Go Back"):
            st.session_state["menu"] = "Calendar View"
            st.rerun()
        st.stop()

    if st.button("← Back to Calendar"):
        st.session_state["menu"] = "Calendar View"
        st.rerun()

    st.subheader(f"📝 Edit Task (ID: {task_id})")

    conn = sqlite3.connect(DB)
    task_df = pd.read_sql_query("SELECT * FROM todos WHERE id=?", conn, params=(task_id,))
    conn.close()

    if task_df.empty:
        st.error("Task not found.")
        if st.button("Back"):
            st.session_state["menu"] = "Calendar View"
            st.rerun()
        st.stop()

    task_row = task_df.iloc[0]

    with st.container(border=True):
        new_task = st.text_input("Task Name", task_row["task"], key="edit_task_name")

        col1, col2 = st.columns(2)
        with col1:
            priority_options = ["High", "Medium", "Low"]
            curr_pri = task_row["priority"] if task_row["priority"] in priority_options else "Medium"
            new_priority = st.selectbox(
                "Priority",
                priority_options,
                index=priority_options.index(curr_pri),
                key="edit_priority"
            )
        with col2:
            category_options = ["General", "Work", "Home", "Study", "Baby", "Finance", "Other"]
            curr_cat = task_row["category"] if task_row["category"] in category_options else "General"
            new_category = st.selectbox(
                "Category",
                category_options,
                index=category_options.index(curr_cat),
                key="edit_category"
            )

        try:
            new_date_dt = pd.to_datetime(task_row["due_date"]).date()
        except:
            new_date_dt = datetime.now().date()

        new_date = st.date_input("Due Date", new_date_dt, key="edit_date")
        new_is_done = st.checkbox("Task Completed?", value=bool(task_row["is_done"]), key="edit_is_done")

        col_save, col_delete = st.columns([1, 1])

        # Save updated task.
        with col_save:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                cur.execute("""
                    UPDATE todos
                    SET task=?, priority=?, category=?, due_date=?, is_done=?
                    WHERE id=?
                """, (
                    new_task,
                    new_priority,
                    new_category,
                    new_date.strftime("%Y-%m-%d"),
                    1 if new_is_done else 0,
                    task_id
                ))
                conn.commit()
                conn.close()

                st.success("Changes saved.")
                st.session_state["menu"] = "Calendar View"
                st.rerun()

        # Delete task.
        with col_delete:
            if st.button("🗑 Delete Task", type="secondary", use_container_width=True):
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                cur.execute("DELETE FROM todos WHERE id=?", (task_id,))
                conn.commit()
                conn.close()

                st.success("Task deleted.")
                st.session_state["menu"] = "Calendar View"
                st.rerun()

# ------------------------------------
# Menu 4: Task Statistics Page
# ------------------------------------
elif st.session_state["menu"] == "Task Stats":
    st.subheader("📊 Task Statistics")

    # Load full task data.
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM todos", conn)
    conn.close()

    if df.empty:
        st.info("No data available.")
    else:
        df["due_date"] = pd.to_datetime(df["due_date"])

        # Determine the current week range (Mon–Sun).
        today = datetime.now()
        start_week = today - pd.Timedelta(days=today.weekday())
        end_week = start_week + pd.Timedelta(days=6)

        df_week = df[
            (df["due_date"].dt.strftime('%Y-%m-%d') >= start_week.strftime('%Y-%m-%d')) &
            (df["due_date"].dt.strftime('%Y-%m-%d') <= end_week.strftime('%Y-%m-%d'))
        ]

        st.markdown(f"### 📅 This Week: {start_week.strftime('%m.%d')} ~ {end_week.strftime('%m.%d')}")
        st.write(f"📌 **Total Tasks:** {len(df_week)}")

        done_rate = (df_week["is_done"].sum() / len(df_week) * 100) if len(df_week) > 0 else 0
        st.write(f"✅ **Completion Rate:** {done_rate:.1f}%")

        st.markdown("---")

        col1, col2 = st.columns(2)

        # Category breakdown pie chart.
        with col1:
            st.markdown("### 🏷️ Category Breakdown")
            cat_count = df["category"].value_counts().reset_index()
            cat_count.columns = ["category", "count"]
            fig_cat = px.pie(
                cat_count,
                names="category",
                values="count",
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        # Priority breakdown pie chart.
        with col2:
            st.markdown("### 🚦 Priority Breakdown")
            pr_count = df["priority"].value_counts().reset_index()
            pr_count.columns = ["priority", "count"]
            fig_pr = px.pie(
                pr_count,
                names="priority",
                values="count",
                color_discrete_map={"High": "#ff6b6b", "Medium": "#ffd93d", "Low": "#6bcb77"}
            )
            st.plotly_chart(fig_pr, use_container_width=True)
