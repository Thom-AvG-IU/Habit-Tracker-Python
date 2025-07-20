from datetime import date, timedelta

class Habit:
    def __init__(self, name: str, description: str, creation_date: date, timeframe: str):
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.timeframe = timeframe.lower()  # 'daily', 'weekly', 'monthly'
        self.last_completed = None
        self.streak = 0
        self.completions = []

    def reset_streak(self):
        self.streak = 0

    def get_streak(self) -> int:
        return self.streak

    def get_next_due_date(self) -> date:
        if not self.last_completed:
            return self.creation_date
        offsets = {"daily": 1, "weekly": 7, "monthly": 30}
        return self.last_completed + timedelta(days=offsets.get(self.timeframe, 0))

    def complete(self):
        today = date.today()
        if self.last_completed:
            days = (today - self.last_completed).days
            if (self.timeframe == "daily" and days == 1) or \
               (self.timeframe == "weekly" and days <= 7) or \
               (self.timeframe == "monthly" and days <= 31):
                self.streak += 1
            else:
                self.streak = 1
        else:
            self.streak = 1

        self.last_completed = today
        self.completions.append(today)

    def __str__(self):
        return (
            f"Habit: {self.name}\n"
            f"Description: {self.description}\n"
            f"Created: {self.creation_date}\n"
            f"Last Completed: {self.last_completed}\n"
            f"Streak: {self.streak}\n"
            f"Next Due: {self.get_next_due_date()}"
        )


    #to_dict methods to work with JSON.

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "creation_date": self.creation_date.isoformat(),
            "timeframe": self.timeframe,
            "last_completed": self.last_completed.isoformat() if self.last_completed else None,
            "streak": self.streak,
            "completions": [d.isoformat() for d in self.completions]
        }

    @staticmethod
    def from_dict(data):
        habit = Habit(
            name=data["name"],
            description=data["description"],
            creation_date=date.fromisoformat(data["creation_date"]),
            timeframe=data["timeframe"]
        )
        habit.last_completed = date.fromisoformat(data["last_completed"]) if data["last_completed"] else None
        habit.streak = data["streak"]
        habit.completions = [date.fromisoformat(d) for d in data["completions"]]
        return habit