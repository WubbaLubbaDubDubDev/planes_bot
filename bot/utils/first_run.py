import json
import os


class FirstRun:
    def __init__(self, sessions_dir: str):
        self.sessions_state_file = os.path.join(sessions_dir, "sessions_state.json")

    def load_sessions(self):
        if os.path.exists(self.sessions_state_file):
            with open(self.sessions_state_file, "r") as file:
                return json.load(file)
        return []

    def save_sessions(self, sessions: list):
        with open(self.sessions_state_file, "w") as file:
            json.dump(sessions, file)

    def is_first_run(self, session_name: str) -> bool:
        sessions = self.load_sessions()
        return session_name not in sessions

    def add_session(self, session_name: str):
        sessions = self.load_sessions()
        sessions.append(session_name)
        self.save_sessions(sessions)

    def check_session(self, session_name: str):
        first_run = self.is_first_run(session_name)
        if first_run:
            self.add_session(session_name)
        return first_run
