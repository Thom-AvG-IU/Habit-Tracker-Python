import unittest
from datetime import date, timedelta
from habits import Habit
from user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        print("Setting up User instance and some habits")
        self.today = date.today()
        self.user = User("testuser", "test@example.com")
        self.habit1 = Habit("Daily Read", "Read a book daily", self.today, "daily")
        self.habit2 = Habit("Weekly Exercise", "Go to the gym", self.today, "weekly")
        self.habit3 = Habit("Monthly Project", "Work on side project", self.today, "monthly")

    def test_initialization(self):
        print("Test user initialization and properties")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(len(self.user.habits), 0)

    def test_add_habit(self):

        self.user.add_habit(self.habit1)
        self.assertEqual(len(self.user.habits), 1)
        self.assertIn(self.habit1, self.user.habits)

        self.user.add_habit(self.habit2)
        self.assertEqual(len(self.user.habits), 2)
        self.assertIn(self.habit2, self.user.habits)

    def test_remove_habit(self):

        self.user.add_habit(self.habit1)
        self.user.add_habit(self.habit2)
        self.assertEqual(len(self.user.habits), 2)

        self.user.remove_habit("Daily Read")
        self.assertEqual(len(self.user.habits), 1)
        self.assertNotIn(self.habit1, self.user.habits)
        self.assertIn(self.habit2, self.user.habits)

        self.user.remove_habit("Weekly Exercise")
        self.assertEqual(len(self.user.habits), 0)

    def test_complete_habit(self):
        self.user.add_habit(self.habit1)
        self.user.add_habit(self.habit2)

        initial_streak_habit1 = self.habit1.streak
        self.user.complete_habit("Daily Read")
        self.assertEqual(self.habit1.streak, initial_streak_habit1 + 1)
        self.assertEqual(self.habit1.last_completed, self.today)

    def test_show_all_habits(self):
        self.assertEqual(self.user.show_all_habits(), [])

        self.user.add_habit(self.habit1)
        self.user.add_habit(self.habit2)
        all_habits = self.user.show_all_habits()
        self.assertEqual(len(all_habits), 2)
        self.assertIn(self.habit1, all_habits)
        self.assertIn(self.habit2, all_habits)

    def test_serialization_and_deserialization(self):
        self.user.add_habit(self.habit1)
        self.user.add_habit(self.habit2)
        self.user.complete_habit(self.habit1.name)

        user_data = self.user.to_dict()
        loaded_user = User.from_dict(user_data)

        self.assertEqual(self.user.username, loaded_user.username)
        self.assertEqual(self.user.email, loaded_user.email)
        self.assertEqual(len(self.user.habits), len(loaded_user.habits))

        for i in range(len(self.user.habits)):
            original_habit = self.user.habits[i]
            loaded_habit = loaded_user.habits[i]
            self.assertEqual(original_habit.name, loaded_habit.name)
            self.assertEqual(original_habit.description, loaded_habit.description)
            self.assertEqual(original_habit.creation_date, loaded_habit.creation_date)
            self.assertEqual(original_habit.timeframe, loaded_habit.timeframe)
            self.assertEqual(original_habit.streak, loaded_habit.streak)
            self.assertEqual(original_habit.last_completed, loaded_habit.last_completed)
            self.assertEqual(original_habit.completions, loaded_habit.completions)

    def test_str_representation(self):
        self.user.add_habit(self.habit1)
        self.user.add_habit(self.habit2)
        expected_str = f"User: testuser, Email: test@example.com, Habits: ['Daily Read', 'Weekly Exercise']"
        self.assertEqual(str(self.user), expected_str)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
