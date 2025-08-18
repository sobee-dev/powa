

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String,Boolean
from flask_login import UserMixin
from extensions import db

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True,nullable=False)
    course: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    funnel: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    gender: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(String(255),nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    interests = relationship("Interests", backref="user", lazy=True)

class Interests(db.Model):
    __tablename__ = "interests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    ongoing_course: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)
    wishlist: Mapped[str] = mapped_column(String(255))
