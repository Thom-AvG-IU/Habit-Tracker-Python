import json
from datetime import datetime, timedelta
from habits import Habit


DATA_FILE = "data.json"

class Analytics:

    @staticmethod
    def _load_habits():
        #"Load and returns all habits from all users in data.json
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
        all_habits = []
        for user in users:
            for h in user.get("habits", []):
                all_habits.append(Habit.from_dict(h))
        return all_habits

    @staticmethod
    def get_highest_streak():
        habits = Analytics._load_habits()
        if not habits:
            print("No habits found.")
            return
        top = max(habits, key=lambda h: h.streak)
        print(f"Highest Streak: {top.name} with {top.streak} days")

    @staticmethod
    def get_hardest_habit():
        habits = Analytics._load_habits()
        if not habits:
            print("No habits found.")
            return
        hardest = min(habits, key=Analytics._get_completion_rate)
        print(f"Hardest Habit: {hardest.name} with {Analytics._get_completion_rate(hardest)*100:.1f}% completion rate")

    @staticmethod
    def get_highest_fail_rate():
        habits = Analytics._load_habits()
        if not habits:
            print("No habits found.")
            return
        hardest = max(habits, key=lambda h: 1 - Analytics._get_completion_rate(h))
        print(f"Highest Fail Rate: {hardest.name} with {(1 - Analytics._get_completion_rate(hardest)) * 100:.1f}% fail rate")

    @staticmethod
    def get_highest_completion_rate():
        habits = Analytics._load_habits()
        if not habits:
            print("No habits found.")
            return
        top = max(habits, key=Analytics._get_completion_rate)
        print(f"Highest Completion Rate: {top.name} with {Analytics._get_completion_rate(top)*100:.1f}%")

    @staticmethod
    def get_completion_rate_for_name(name: str):
        habits = Analytics._load_habits()
        habit = next((h for h in habits if h.name.lower() == name.lower()), None)
        if not habit:
            print(f"No habit found with name: {name}")
            return
        rate = Analytics._get_completion_rate(habit)
        print(f"Completion Rate for '{habit.name}': {rate*100:.1f}%")

    
    #improved completionrate calculation based on feedback phase 2
    #introduced seperate logic for different timeframes using timedelta

    @staticmethod
    def _get_completion_rate(habit) -> float:
        if not habit.completions:
            return 0.0
        
        end_date = habit.last_completed or datetime.today()
        total_periods = 0

        if habit.timeframe == "daily":
            total_periods = (end_date - habit.creation_date).days + 1

        elif habit.timeframe == "weekly":

            start_of_creation_week = habit.creation_date - timedelta(days=habit.creation_date.weekday())
            start_of_end_week = end_date - timedelta(days=end_date.weekday())
            total_periods = ((start_of_end_week - start_of_creation_week).days // 7) + 1

        elif habit.timeframe == "monthly":

            total_periods = (end_date.year - habit.creation_date.year) * 12 + \
                        (end_date.month - habit.creation_date.month) + 1
            
        else:
            # Fallback for unknown timeframe, treated as daily
            total_periods = (end_date - habit.creation_date).days + 1

        if total_periods <= 0:
            return 0.0

        return len(habit.completions) / total_periods