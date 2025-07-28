# Habit-Tracker-Python
A habit tracker application in python

This is a simple, terminal-based habit tracker. 
Made for users to track their habits over time, bulding up streaks, and analyse consistency. 
Habits can be set to be daily, weekly, or monthly occuring events.
Different user profiles can be made, so usable for multiple individuals.

Summary of the features:
*add your user to the application
*add habits for each user
*complete your habits through the terminal
*remove, add, reset and view habits
*saving and loading data via JSON
*do further analysis using the analytics menu

The project is split into the follwing files:
mainq.py - main script using questionary
habits.py - creates the habit object
user.py - creates the user object
reminderclass.py - runs an automatic reminder on due habits
analytics2_0.py - contains the methods for further analysis
data.json - JSON that data persists to and from
test_habit.py - unit test for habits
test_user.py -unit test for users
