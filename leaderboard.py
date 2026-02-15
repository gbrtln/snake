import json
import os
import datetime
from constants import LEADERBOARD_FILE, LEADERBOARD_MAX


class Leaderboard:
    def __init__(self, filepath=None):
        self.filepath = filepath or LEADERBOARD_FILE
        self.entries  = self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [
                e for e in data
                if isinstance(e, dict)
                and "name"  in e
                and "score" in e
                and "date"  in e
            ]
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # silently ignore write errors

    def add(self, name: str, score: int):
        clean_name = (name.strip()[:12] or "AAA")
        entry = {
            "name":  clean_name,
            "score": score,
            "date":  datetime.date.today().isoformat(),
        }
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[:LEADERBOARD_MAX]
        self._save()

    def is_high_score(self, score: int) -> bool:
        if score <= 0:
            return False
        if len(self.entries) < LEADERBOARD_MAX:
            return True
        return score > self.entries[-1]["score"]

    def top(self, n: int = LEADERBOARD_MAX):
        return self.entries[:n]
