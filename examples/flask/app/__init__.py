from flask import Flask, session, redirect, jsonify
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from gtm_manager.manager import GTMManager


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "DEV"

    from app.blueprints import auth

    app.register_blueprint(auth.bp, url_prefix="/auth")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    @app.route("/")
    def home():
        authorized_user_info = session.get("authorized_user_info")

        if not authorized_user_info:
            return redirect("/auth")

        try:
            credentials = Credentials.from_authorized_user_info(authorized_user_info)
        except RefreshError:
            session["authorized_user_info"] = None
            return redirect("/auth")


        accounts = GTMManager(credentials=credentials).list_accounts()

        return jsonify({"accounts": [x.raw_body for x in accounts]})

    return app
