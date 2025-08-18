
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase



# Custom base class
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


mail = Mail()