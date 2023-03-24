from flask import Flask, Blueprint, render_template, request
from src.web.config import get_config
import src.core.db as database
from src.web.controllers.discipline import discipline_blueprint
from src.web.controllers.associate import associate_blueprint
from src.web.controllers.configuration import configuration_blueprint
from src.web.controllers.api.configuration import configuration_api_blueprint
from src.web.controllers.api.auth import auth_api_blueprint
from src.web.controllers.api.discipline import discipline_api_blueprint
from src.web.controllers.api.associate import associate_api_blueprint
from src.web.controllers.api.user import user_api_blueprint
from src.web.controllers.api.payment import payment_api_blueprint
from src.web.controllers.api.info import info_api_blueprint
from src.web.controllers.api.statistics import statistics_api_blueprint
from src.web.controllers.api.resetdb import resetdb_api_blueprint
from src.web.controllers.user import user_blueprint
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.payments import payments_blueprint
from src.web.helpers import handlers, auth
from flask_session import Session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager


def create_app(env="development", static_folder="/static", template_folder="templates"):
    """Args:
        env (str, optional): Environment to be used. Defaults to "development".
        static_folder (str, optional): Static folder to be used. Defaults to "/static".
        template_folder (str, optional): Template folder to be used. Defaults to "templates".
    Returns:
        Flask: Flask app
    """
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

    # uploading files config
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "public", "associate_pics")
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # cors
    if env == "development":
        white_list = [
            "http://localhost:5173",
            "https://grupo12.proyecto2022.linti.unlp.edu.ar",
            
        ]
        CORS(
            app,
            resources={r"/api/*": {"origins": white_list}},
            supports_credentials=True,
        )

    # load config
    config = get_config()
    app.config.from_object(config[env])

    # init db
    with app.app_context():
        database.init_app(app)

    # Session
    Session(app)

    # jwt
    jwt = JWTManager(app)

    # Controllers
    app.register_blueprint(discipline_blueprint)
    app.register_blueprint(associate_blueprint)
    app.register_blueprint(configuration_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(payments_blueprint)

    # Api
    api_blueprint = Blueprint("api", __name__, url_prefix="/api")
    api_blueprint.register_blueprint(resetdb_api_blueprint)
    api_blueprint.register_blueprint(configuration_api_blueprint)
    api_blueprint.register_blueprint(auth_api_blueprint)
    api_blueprint.register_blueprint(statistics_api_blueprint)

    # Api me
    api_me_blueprint = Blueprint("api_me", __name__, url_prefix="/me")
    api_me_blueprint.register_blueprint(associate_api_blueprint)
    api_me_blueprint.register_blueprint(payment_api_blueprint)
    api_blueprint.register_blueprint(api_me_blueprint)

    # Api club
    api_club_blueprint = Blueprint("api_club", __name__, url_prefix="/club")
    api_club_blueprint.register_blueprint(info_api_blueprint)
    api_club_blueprint.register_blueprint(discipline_api_blueprint)
    api_club_blueprint.register_blueprint(user_api_blueprint)
    api_blueprint.register_blueprint(api_club_blueprint)

    app.register_blueprint(api_blueprint)

    # Routes
    @app.get("/")
    def home():
        """Returns:
        HTML: Redirects to the home page
        """
        return render_template("home.html")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Args:
        exception (Exception, optional): Exception to be handled. Defaults to None.
        """
        database.db.session.remove()

    @app.cli.command("resetdb")
    def resetdb():
        """Resets the database"""
        database.reset_db()

    # error handlers
    app.register_error_handler(400, handlers.bad_request_error)
    app.register_error_handler(401, handlers.unauthorized_error)
    app.register_error_handler(403, handlers.forbidden_error)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    # Jinja
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.jinja_env.globals.update(has_permission=auth.check_permission)

    return app
