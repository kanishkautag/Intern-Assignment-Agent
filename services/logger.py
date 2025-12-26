import streamlit as st
import pandas as pd
from datetime import datetime

class LiveLogger:
    """Handles the real-time logging of agent activities in the Streamlit UI."""

    def __init__(self, placeholder):
        """
        Initializes the logger with a specific UI placeholder.
        Ensures the 'logs' session state exists upon instantiation.
        """
        self.placeholder = placeholder
        # Ensure state initialization happens immediately
        if "logs" not in st.session_state:
            st.session_state.logs = []

    def log(self, step: str, tool: str, status: str):
        """
        Adds or updates a log entry and re-renders the UI table.
        
        Args:
            step: Description of the current action.
            tool: The app, URL, or library being used (e.g., 'PyAutoGUI', 'Groq').
            status: Execution status ('STARTED', 'SUCCESS', 'FAILED', or 'RETRIED').
        """
        # Re-check initialization for safety during reruns
        if "logs" not in st.session_state:
            st.session_state.logs = []

        now = datetime.now().strftime("%H:%M:%S")
        
        # logic: Update the status of the last matching 'STARTED' entry
        # rather than creating a duplicate line for the same step
        updated = False
        if status != "STARTED":
            for item in reversed(st.session_state.logs):
                if item["Step Description"] == step and item["Status"] == "STARTED":
                    item["Status"] = status
                    item["Timestamp"] = now
                    updated = True
                    break
        
        if not updated:
            entry = {
                "Timestamp": now,
                "Order": len(st.session_state.logs) + 1,
                "Step Description": step,
                "Tool/App/URL/EXE": tool,
                "Status": status
            }
            st.session_state.logs.append(entry)

        # Rendering the logs with custom CSS color coding
        self._render_table()

    def _render_table(self):
        """Converts logs to a DataFrame and applies visual styling for the UI."""
        if not st.session_state.logs:
            return

        df = pd.DataFrame(st.session_state.logs)

        # Define color logic for different status codes
        def style_status(val):
            color_map = {
                "STARTED": "color: #3498db;", # Blue
                "SUCCESS": "color: #27ae60; font-weight: bold;", # Green
                "FAILED": "color: #e74c3c; font-weight: bold;", # Red
                "RETRIED": "color: #f39c12;" # Orange
            }
            return color_map.get(val, "color: black;")

        # Apply styles and display in the Streamlit placeholder
        styled_df = df.style.map(style_status, subset=['Status'])
        
        self.placeholder.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )