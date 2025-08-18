

from flask import redirect, url_for, session
from _datetime import datetime



def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Day"
    else:
        return "Good Evening"

def log_out():
    session.clear()
    return redirect(url_for("home"))

