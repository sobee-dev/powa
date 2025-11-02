import json
import os

from models.database import User

file_path = os.path.join(os.path.dirname(__file__), '..', 'course_data.json')
with open(file_path,encoding="utf-8") as f:
    courses = json.load(f)


def get_all_users():
    return User.query.all()



file_path2 = os.path.join(os.path.dirname(__file__), '..', 'faq.json')
with open(file_path2,encoding="utf-8") as faq:
    information = json.load(faq)

file_path3 = os.path.join(os.path.dirname(__file__), '..', 'team.json')
with open(file_path3,encoding="utf-8") as my_team:
    team = json.load(my_team)