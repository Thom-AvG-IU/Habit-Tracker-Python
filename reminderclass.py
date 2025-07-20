from datetime import date

class ReminderClass:
    @staticmethod
    def send_reminders(user, check_date: date):
        for habit in user.habits_to_do(check_date):
            print(f"Reminder: {habit.name}")