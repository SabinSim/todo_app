
# 📘 Sabin’s To-Do & Schedule Manager

🔗 Live Demo

👉 https://sabin-todo.streamlit.app

*A calendar-centric task management application built with Streamlit.*

---

## ⭐ Overview

This project is a modern, minimalistic, calendar-centric To-Do application designed for **clarity, speed, and real usability**.
Unlike traditional To-Do apps that separate views for adding, listing, and editing tasks, this app integrates all major workflows directly into an interactive calendar powered by **FullCalendar JS**.

The result is a clean, intuitive system where:

* Click a date → add a task
* Click an event → edit a task
* Drag a task → change its due date
* Colors represent priority
* Stats and charts give a weekly overview

This project showcases not only Python + Streamlit development, but also **UI/UX design, architectural decision-making, and iterative problem-solving.**

---

# 🧱 Features

### 📅 Interactive FullCalendar Integration

* Date click → Add Task screen
* Event click → Edit Task screen
* Drag & drop → Instantly update due dates
* Priority-based colors (High / Medium / Low)
* Auto-refresh logic (Summary & Events update instantly)

---

### 🔔 Smart Daily Summary

Displayed above the calendar:

* Tasks due today
* Tasks due tomorrow
* Overdue tasks
* Only counts incomplete tasks
* Auto-updates after drag & drop, add, or edit

---

### 📝 Task Management

* Add a new task directly from the calendar
* Edit task name, category, priority, due date
* Mark as completed
* Delete tasks
* Simple and minimal UI

---

### 📊 Weekly Statistics Dashboard

* Total tasks for the current week
* Completion rate
* Category distribution (Pie chart)
* Priority distribution (Pie chart)

---

# 🧭 Architecture & Design Decisions

This project went through multiple iterations to arrive at its final form.
Below is the **development journey**, explaining what was tried, what was removed, and why.

---

## 🔨 Initial Structure (Too Many Pages)

Early versions used a traditional multi-page approach:

* Add Task
* View Tasks
* Filter by Date
* Calendar View
* Task Stats
* Sort Tasks (Sortable UI test)

**Problems:**

* Redundant pages
* UX felt scattered
* Editing and adding tasks required too many clicks
* Calendar felt disconnected from task management
* Too much manual navigation

---

## 🎯 Major Redesign: *Calendar-Centric Architecture*

Sabin made a key decision:

> **“The calendar should become the heart of the entire app.”**

This changed everything.

### What changed:

✔ Removed:

* Separate Add Task menu
* Separate View / List pages
* Filter pages
* Sort tasks page
* Standalone navigation-heavy workflow

✔ Added:

* Calendar becomes the main dashboard
* All create/edit actions start from calendar interactions
* Hidden pages (Add Task / Edit Task) revealed only when needed
* Minimal menu:

  * Calendar View
  * Task Stats

This made the UI **cleaner, faster, and more professional.**

---

## 🧪 Experiments That Were Attempted (and Why They Were Removed)

### ❌ Sortable UI (streamlit-sortables)

* Custom drag-based manual task ordering attempted
* Unsupported `styles` argument caused errors
* UI result felt cluttered
* Removed for cleaner system
* But demonstrates ability to explore additional UI libraries

---

### ❌ Full postMessage + custom JS integration

Originally, a custom integration using JS:

```js
window.addEventListener("message", ...)
```

* Required low-level iframe messaging
* Later replaced with built-in `calendar_state` callback system
* More stable and maintainable

This shows deep willingness to explore advanced techniques.

---

### ❌ Separate Task View / Filter Pages

Attempted to build:

* “View Tasks”
* “Tasks Today”
* “Filter by Category”

Removed because:

* All information can be seen more intuitively inside FullCalendar
* Better UX when combined with color-coded priorities

---

### ❌ AI Summary (OpenAI API)

A prototype was built to:

* Analyze tasks
* Prioritize items
* Recommend time scheduling

Later removed to keep the app focused and lightweight.

**This will be revisited in a future project** (e.g., AI Personal Planner).

---

# 🏗 Tech Stack

| Layer                | Tools                                       |
| -------------------- | ------------------------------------------- |
| **Frontend**         | Streamlit, HTML/CSS-injection, FullCalendar |
| **Backend**          | Python, SQLite                              |
| **Visualization**    | Plotly Express (Pie charts)                 |
| **State Management** | Streamlit Session State                     |

---

# 📂 Project Structure

```
/todo_app
├── todo_app.py               # Main application
├── calendar_options.py       # FullCalendar settings + custom CSS
├── todo.db                   # SQLite database
├── requirements.txt
├── .streamlit/               # Light Mode using Streamlit's theme settings.
│   └── config.toml
└── README.md
```

---

# 🚀 How It Works (User Flow)

1. Open the app → Calendar appears
2. Click a date → Add new task
3. Click a task → Edit task
4. Drag task → Automatically update due date
5. Summary updates instantly
6. Go to Task Stats for weekly overview

---

# 📦 Installation & Run

```bash
pip install -r requirements.txt
streamlit run todo_app.py
```

---

# 🙌 About the Developer

**Sabin Sim**
A developer blending software engineering with clean UI/UX principles.
Focused on building practical, intuitive applications with modern tools.

---

# 🔮 Future Improvements

* AI task analysis (prioritization, focus recommendations)
* Category color customization
* Repeating tasks
* Google Calendar sync
* Mobile-friendly layout

