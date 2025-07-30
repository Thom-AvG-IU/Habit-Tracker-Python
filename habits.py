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
    # reset streak to 0, only activated by user purposely
    def reset_streak(self):
        self.streak = 0
    # returns streak of a habit
    def get_streak(self) -> int:
        return self.streak
    # check when the habit should be performed next
    #based on the timeframe, here called offsets.
    def get_next_due_date(self) -> date:
        if not self.last_completed:
            return self.creation_date
        offsets = {"daily": 1, "weekly": 7, "monthly": 30}
        return self.last_completed + timedelta(days=offsets.get(self.timeframe, 0))
    #completing a habit, calculates the delta between today and the last completed date. 
    def complete(self):
        today = date.today()
        #depending on the timeframe it checks if you are in the timerange if so increases by 1
        #checks if the habit has been completed in the past
        if self.last_completed:
            days = (today - self.last_completed).days
            # print(today) used for debugging
            # print("today^")
            # print (self.last_completed) 
            # print("last completed^")

            # print("days calculation")
            # print(days)

            #improved version of the complete function to account for early completions
            if (self.timeframe == "daily" and 1 <= days <= 2) or \
               (self.timeframe == "weekly" and 6 <= days <= 8) or \
               (self.timeframe == "monthly" and 28 <= days <= 31):
                self.streak += 1
                # print("streak calculation")
                # print(self.streak)
            #if not, then it considers you failed the habit, and are back to a streak of 1
            #a different operation, but the same outcome of the original if statement, in the future there can be different consequences for failing a streak
            #instead of starting a new one
            else:
                self.streak = 1
        else:
            self.streak = 1
        #keeps record of all completion dates.
        self.last_completed = today
        self.completions.append(today)

    #methods for converting habit to json, used sources for below design.
    def __str__(self):
        return (
            f"Habit: {self.name}\n"
            f"Description: {self.description}\n"
            f"Created: {self.creation_date}\n"
            f"Last Completed: {self.last_completed}\n"
            f"Streak: {self.streak}\n"
            f"Next Due: {self.get_next_due_date()}"
        )

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