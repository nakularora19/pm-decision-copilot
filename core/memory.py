import json
import os
from datetime import datetime, timezone

LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")


class Memory:
    """
    Memory — lightweight session and run persistence.

    Stores agent outputs for the current session and persists completed runs
    as JSON log files in logs/ for auditability.

    Log file format: logs/run_<UTC-ISO-timestamp>.json
    """

    def __init__(self):
        self._session: dict = {}
        os.makedirs(LOGS_DIR, exist_ok=True)

    def set(self, key: str, value) -> None:
        """Store a value in the current session."""
        self._session[key] = value

    def get(self, key: str, default=None):
        """Retrieve a value from the current session."""
        return self._session.get(key, default)

    def save_run(self, run_data: dict) -> str:
        """
        Persist a completed run to disk as a JSON log file.

        Args:
            run_data: The full run result from the orchestrator.

        Returns:
            The absolute file path of the saved log.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"run_{timestamp}.json"
        filepath = os.path.abspath(os.path.join(LOGS_DIR, filename))
        with open(filepath, "w") as f:
            json.dump(run_data, f, indent=2)
        return filepath

    def load_run(self, filepath: str) -> dict:
        """
        Load a previously saved run from disk.

        Args:
            filepath: Absolute or relative path to the JSON log file.

        Returns:
            The run data dict.
        """
        with open(filepath) as f:
            return json.load(f)
