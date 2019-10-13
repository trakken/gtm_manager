from flask import Blueprint, redirect, request, abort, current_app, session
from google_auth_oauthlib.flow import Flow


bp = Blueprint("auth", __name__)


@bp.route("/", methods=["GET"])
def init_auth():
    flow = get_flow()
    auth_url, state = flow.authorization_url(access_type="offline")
    session["state"] = state

    return redirect(auth_url)


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if state != session.get("state"):
        current_app.logger.info("Miss matching state values")
        redirect("/")

    if not code:
        current_app.logger.info("Missing required 'code' query parameter")
        abort(400)

    flow = get_flow()
    flow.fetch_token(code=code)

    session["authorized_user_info"] = {
        "token": flow.credentials.token,
        "refresh_token": flow.credentials.refresh_token,
        "token_uri": flow.credentials.token_uri,
        "client_id": flow.credentials.client_id,
        "client_secret": flow.credentials.client_secret,
        "scopes": flow.credentials.scopes,
    }

    return redirect("/")


def get_flow():
    return Flow.from_client_secrets_file(
        "client_secret.json",
        redirect_uri="http://localhost:5000/auth/callback",
        scopes=["https://www.googleapis.com/auth/tagmanager.readonly"],
    )
