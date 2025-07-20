from datetime import date
from habits import Habit

class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.habits = []

    def add_habit(self, habit: Habit):
        self.habits.append(habit)

    def remove_habit(self, name: str):
        self.habits = [h for h in self.habits if h.name.lower() != name.lower()]

    def complete_habit(self, name: str):
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                habit.complete()
                return
        print(f"Habit '{name}' not found.")

    def show_all_habits(self) -> list:
        return self.habits

    def habits_to_do(self, check_date: date) -> list:
        return [h for h in self.habits if h.get_next_due_date() <= check_date]

    def __str__(self):
        habit_names = [h.name for h in self.habits]
        return f"User: {self.username}, Email: {self.email}, Habits: {habit_names}"

# to_dict, and from_dict methods for working with JSON. 
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "habits": [habit.to_dict() for habit in self.habits]
        }

    @staticmethod
    def from_dict(data):
        user = User(data["username"], data["email"])
        user.habits = [Habit.from_dict(h) for h in data["habits"]]
        return user