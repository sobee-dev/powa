

from flask import redirect, url_for, session, current_app
from _datetime import datetime

from flask_login import  logout_user
from werkzeug.security import generate_password_hash

from extensions import db,login_manager
from models.database import Admin


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Day"
    else:
        return "Good Evening"

def create_admin():
    admin_email = current_app.config['ADMIN_EMAIL']
    admin_password = current_app.config['ADMIN_PASSWORD']
    hashed_password = generate_password_hash(admin_password)

    if not Admin.query.filter_by(admin_email=admin_email).first():

        admin = Admin(admin_email=admin_email, hashed_password= hashed_password)
        db.session.add(admin)
        db.session.commit()
        print("Default admin created")


def log_out():
    logout_user()

    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

