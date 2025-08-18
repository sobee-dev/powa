import json
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'course_data.json')
with open(file_path,encoding="utf-8") as f:
    courses = json.load(f)



