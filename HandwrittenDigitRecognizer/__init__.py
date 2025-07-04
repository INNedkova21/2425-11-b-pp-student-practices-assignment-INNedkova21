from flask import Flask
from HandwrittenDigitRecognizer.users import users
from HandwrittenDigitRecognizer.ai import ai
from HandwrittenDigitRecognizer.config import Config
from HandwrittenDigitRecognizer.errors import errors
from HandwrittenDigitRecognizer.extensions import db, login_manager, mail
from HandwrittenDigitRecognizer.main.routes import main
from HandwrittenDigitRecognizer.auth import auth
from HandwrittenDigitRecognizer.models.user import User
from .feedback import feedback
from .models.feedback import Feedback

def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(ai, url_prefix='/ai')
    app.register_blueprint(errors)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(feedback, url_prefix='/feedback')

    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))