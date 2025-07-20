import json
from datetime import date
from user import User
from habits import Habit
from analytics2_0 import Analytics
import questionary
import sys
from reminderclass import ReminderClass

DATA_FILE = "data.json"


#method used at different stages of the program to quit the app
@staticmethod
def quit_app():
     print("killing the app")
     sys.exit()
    
#checks for data persisted in the past, looks for a file called data.json
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return [User.from_dict(u) for u in json.load(f)]
    except:
        return []
    
#called when new user is created, writes to json file
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=4)
#calls the method above
users = load_users()

#functions as main menu, where the user can choose to create a user, select a user or quit the app, 'select user' calls the user menu. 'See analytics' calls the 'analytics menu'
#made use of questionary module, very helpful, firstly I did not use it, after live session I was reminded of the modules recommended. Hence the name of the file mainq (questionary), I also tried Click, but this was most convenient for me.
def main_menu():
    while True:
        action = questionary.select(
            "Main Menu - Choose an action:",
            choices=["Create User", "Select User", "See Analytics", "Quit"]
        ).ask()
        #appends user to list defined in methods save_users, load_users
        if action == "Create User":
            name = questionary.text("Username:").ask()
            email = questionary.text("Email:").ask()
            users.append(User(name, email))
            print(f"User '{name}' has been created.")
            save_users(users)

        elif action == "Select User":
            if not users:
                print("No users yet. Please register with Create User.")
                continue

            selected = questionary.select(
                "Select a user:",
                choices=[f"{i+1}. {u.username}" for i, u in enumerate(users)]
            ).ask()

            index = int(selected.split(".")[0]) - 1
            user = users[index]
            user_menu(user)

        elif action == "See Analytics":
              analytics_menu()

        elif action == "Quit":
            print("Goodbye!")
            quit_app()

#analytics menu is a seperate method, similar technical approach as the main menu, but methods called are in different class analytics. file analytics2_0.py was my seccond attempt at this class (I had some issues at first)
#Uses same questionary methods as in main menu

def analytics_menu():
                
    while True:
        action = questionary.select(
            "You are now in the analytics view, select an action:",
            choices=["See Highest Streak", "See Hardest Habit", "See Highest Failrate", "See Highest Completionrate", "See Completionrate For Habit","Quit"]
            ).ask()

        if action == "See Highest Streak":
                Analytics.get_highest_streak()

        elif action == "See Hardest Habit":
                Analytics.get_hardest_habit()

        elif action == "See Highest Failrate":
                Analytics.get_hardest_habit

        elif action == "See Highest Completionrate":
                Analytics.get_highest_completion_rate
        #variable input_name has the be an exact match with the name used in Habit, definitely one of the most inconvenient parts of the app.
        #alternatively I could also iterate through all habits to have the user select, but this could then become too big in case of many habits. 
        elif action == "See Completionrate For Habit":
                print("insert habit name\n")
                input_name = input("5. Enter a habit name to get its completion rate: ")
                Analytics.get_completion_rate_for_name(input_name)

        elif action == "Quit":
            print("Goodbye!")
            quit_app()


#the user menu is essentially the main menu when a user is 'logged in', this is where a user interacts with habits.

def user_menu(user):

    #prints the user selected, and calls the reminder class upon selecting a user.

    print(f"\nYou selected user: {user.username}")

    print("\n=== Habit Reminders for Today ===")
    ReminderClass.send_reminders(user, date.today())
    print("=================================")

    #moves on to questionary options for the interacting with habits
    while True:
        ua = questionary.select(
            "User Menu - Choose an action:",
            choices=[
                "Add Habit", "Complete Habit", "Remove Habit",
                "View Habits", "Due Habits", "Back"
            ]
        ).ask()

        if ua == "Add Habit":
            name = questionary.text("Habit name:").ask()
            desc = questionary.text("Description:").ask()
            timeframe = questionary.select(
                "Timeframe:",
                choices=["daily", "weekly", "monthly"]
            ).ask()
            user.add_habit(Habit(name, desc, date.today(), timeframe))
            print("Habit added.")

        elif ua == "Complete Habit":
            name = questionary.text("Habit name:").ask()
            user.complete_habit(name)

        elif ua == "Remove Habit":
            name = questionary.text("Habit name:").ask()
            user.remove_habit(name)

        elif ua == "View Habits":
            for h in user.show_all_habits():
                print(f"\n{h}")

        elif ua == "Due Habits":
            due = user.habits_to_do(date.today())
            if not due:
                print("No habits due today.")
            else:
                for h in due:
                    print(f"- {h.name} (due: {h.get_next_due_date()})")

        elif ua == "Back":
            break


#upon running calls main_menu method to initiate.
main_menu()