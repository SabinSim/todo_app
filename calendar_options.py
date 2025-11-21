# ---------------------------------------------------------
# FullCalendar Configuration & Custom Styling
# ---------------------------------------------------------

# 1. FullCalendar Options (Core behavior settings)
calendar_options = {
    "editable": True,        # Enable drag & drop to reschedule events
    "navLinks": True,        # Allow clicking on dates/week names to navigate
    "selectable": True,      # Allow selecting empty dates (used for Add Task logic)
    "selectMirror": True,    # Visual mirror effect when selecting
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        # Updated: replaced listWeek with listMonth for cleaner monthly list view
        "right": "dayGridMonth,timeGridWeek,listMonth",
    },
    "initialView": "dayGridMonth",  # Default view when calendar loads
}

# 2. Custom CSS (Visual design for calendar elements)
custom_css = """
    /* Make past events slightly faded */
    .fc-event-past {
        opacity: 0.8;
    }

    /* Style for event time text */
    .fc-event-time {
        font-style: italic;
    }

    /* Make event titles bold */
    .fc-event-title {
        font-weight: 700;
    }

    /* Toolbar title (month/week/day title) styling */
    .fc-toolbar-title {
        font-size: 1.5rem !important;
        color: #2c3e50;
    }

    /* Highlight today's background */
    .fc-day-today {
        background-color: #f0f9ff !important;
    }

    /* Primary button colors (Prev/Next/Today buttons) */
    .fc-button-primary {
        background-color: #2c3e50 !important;
        border-color: #2c3e50 !important;
    }

    /* Hover effect for primary buttons */
    .fc-button-primary:hover {
        background-color: #1a252f !important;
        border-color: #1a252f !important;
    }
"""

