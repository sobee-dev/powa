import json
import os

from models.database import User

file_path = os.path.join(os.path.dirname(__file__), '..', 'course_data.json')
with open(file_path,encoding="utf-8") as f:
    courses = json.load(f)


def get_all_users():
    return User.query.all()
