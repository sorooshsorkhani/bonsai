import json
import os
from datetime import datetime
from pathlib import Path

# Determine the path to the feedback JSON file
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # ensure data directory exists
FEEDBACK_FILE = DATA_DIR / "feedback_log.json"

def record_feedback(message_index: int, message_text: str, feedback: str):
    """
    Append a feedback record to feedback.json.

    Args:
        message_index: index of the assistant message in session_state.
        message_text: the full text of the assistant's response.
        feedback: either 'up' or 'down'.
    """
    # Load existing feedback
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    # Create new record
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message_index": message_index,
        "feedback": feedback,
        "message_text": message_text
    }
    records.append(record)

    # Save back
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
