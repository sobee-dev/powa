import os

from flask import Flask

from views.controller import controller
from config.config import Config
from extensions import db, mail, login_manager
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail.init_app(app)

from models.database import User,Interests
migrate = Migrate(app, db)

login_manager.init_app(app)



# ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.context_processor
def inject_year():
    from datetime import datetime
    return {"year": datetime.now().year}

app.register_blueprint(controller)

if __name__ == "__main__":
    with app.app_context():
        print(User.query.all())
    app.run(debug= False)








