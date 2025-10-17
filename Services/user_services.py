

from _datetime import datetime

from flask import redirect, url_for, current_app
from flask_login import logout_user, UserMixin

from extensions import login_manager


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Day"
    else:
        return "Good Evening"



class Admin(UserMixin):
    def __init__(self, admin_id, admin_email):
        self.id = str(admin_id)
        self.admin_email = admin_email


def log_out():
    logout_user()

    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(admin_id):
    admin_email = current_app.config['ADMIN_EMAIL']
    return Admin(admin_id=admin_id,admin_email= admin_email)
