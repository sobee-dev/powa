import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI' , 'sqlite:///powa_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Logout after 30 minutes of inactivity
    REMEMBER_COOKIE_DURATION = timedelta(hours=1)

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    FROM_EMAIL= os.getenv("MAIL_DEFAULT_SENDER", "info@thetechpowa.com")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')