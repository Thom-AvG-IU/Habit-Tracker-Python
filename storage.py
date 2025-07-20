import json
from datetime import date
import user
import habits

def save_user(user, filename="user_data.json"):
    with open(filename, "w") as f:
        json.dump(user.to_dict(), f, indent=4)

def load_user(filename="user_data.json") -> user:
    with open(filename, "r") as f:
        data = json.load(f)
        return user.from_dict(data)