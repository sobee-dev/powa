import os

from flask import Flask
from models.database import User
from views.controller import controller
from config.config import Config
from extensions import db,mail
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.context_processor
def inject_year():
    from datetime import datetime
    return {"year": datetime.now().year}


with app.app_context():
    db.drop_all()
    db.create_all()

    print("db created successfully")

    print(User.query.all())

print("MAIL_SERVER:", app.config.get("MAIL_SERVER"))
print("MAIL_USERNAME:", app.config.get("MAIL_USERNAME"))
print("MAIL_USE_TLS:", app.config.get("MAIL_USE_TLS"))
print("MAIL_PORT:", app.config.get("MAIL_PORT"))

app.register_blueprint(controller)
if __name__ == "__main__":
    app.run(debug= True)








