
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager



login_manager = LoginManager()
login_manager.login_view = "controller.login"
# Custom base class
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


mail = Mail()