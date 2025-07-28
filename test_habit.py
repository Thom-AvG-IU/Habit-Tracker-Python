import unittest
from datetime import date, timedelta
from habits import Habit


class TestHabit(unittest.TestCase):

    def setUp(self):
        self.today = date.today()
        self.creation_date = self.today - timedelta(days=30)
        print(f"\n RUNNING TESTCASE - Today: {self.today}")

    def make_habit(self, name, timeframe, streak=0, last_completed=None):
        habit = Habit(name, "Test", self.creation_date, timeframe)
        habit.streak = streak
        habit.last_completed = last_completed
        print(f" Created habit: '{habit.name}' | Timeframe: '{habit.timeframe}' | Initial Streak: {habit.streak} | Last Completed: {habit.last_completed}")
        return habit


    def test_initial_and_first_completion(self):
        h = self.make_habit("Daily", "daily")
        self.assertEqual(h.streak, 0)
        self.assertEqual(h.get_next_due_date(), self.creation_date)
        h.complete()
        self.assertEqual(h.streak, 1)
        self.assertEqual(h.last_completed, self.today)
        self.assertIn(self.today, h.completions)

    def test_streaks(self):
        # daily success
        h = self.make_habit("Daily", "daily", 2, self.today - timedelta(days=1))
        h.complete()
        self.assertEqual(h.streak, 3)

        # daily fail
        h = self.make_habit("Late Daily", "daily", 4, self.today - timedelta(days=3))
        h.complete()
        self.assertEqual(h.streak, 1)

        # weekly success
        h = self.make_habit("Weekly", "weekly", 2, self.today - timedelta(days=7))
        h.complete()
        self.assertEqual(h.streak, 3)

        # weekly fail
        h = self.make_habit("Early Weekly", "weekly", 2, self.today - timedelta(days=3))
        h.complete()
        self.assertEqual(h.streak, 1)

        # monthly success
        h = self.make_habit("Monthly", "monthly", 1, self.today - timedelta(days=30))
        h.complete()
        self.assertEqual(h.streak, 2)

    def test_reset_streak(self):
        h = self.make_habit("Reset", "daily", 5)
        h.reset_streak()
        self.assertEqual(h.streak, 0)

    def test_serialization(self):
        h = self.make_habit("Serialize", "daily")
        h.complete()
        data = h.to_dict()
        copy = Habit.from_dict(data)
        self.assertEqual(h.name, copy.name)
        self.assertEqual(h.streak, copy.streak)
        self.assertEqual(h.last_completed, copy.last_completed)
        self.assertEqual(h.completions, copy.completions)

    def test_next_due(self):
        h = self.make_habit("Next Due", "weekly")
        h.last_completed = self.today
        self.assertEqual(h.get_next_due_date(), self.today + timedelta(days=7))

if __name__ == '__main__':
    unittest.main()