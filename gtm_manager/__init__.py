"""__init__.py"""
__version__ = "0.2.3"


class GoogleTagManagerScopes:
    """Scopes available in the Google Tag Manager API."""

    MANAGE_USERS = "https://www.googleapis.com/auth/tagmanager.manage.users"
    READONLY = "https://www.googleapis.com/auth/tagmanager.readonly"
    EDIT_CONTAINERS = "https://www.googleapis.com/auth/tagmanager.edit.containers"
    EDIT_CONTAINERVERSIONS = (
        "https://www.googleapis.com/auth/tagmanager.edit.containerversions"
    )
    PUBLISH = "https://www.googleapis.com/auth/tagmanager.publish"
    MANAGE_ACCOUNTS = "https://www.googleapis.com/auth/tagmanager.manage.accounts"
    DELETE_CONTAINERS = "https://www.googleapis.com/auth/tagmanager.delete.containers"


AUTH_SCOPES = [
    GoogleTagManagerScopes.MANAGE_USERS,
    GoogleTagManagerScopes.READONLY,
    GoogleTagManagerScopes.EDIT_CONTAINERS,
    GoogleTagManagerScopes.EDIT_CONTAINERVERSIONS,
    GoogleTagManagerScopes.PUBLISH,
    GoogleTagManagerScopes.MANAGE_ACCOUNTS,
    GoogleTagManagerScopes.DELETE_CONTAINERS,
]

SERVICE_NAME = "tagmanager"
SERVICE_VERSION = "v2"
CREDENTIALS_FILE_NAME = "_auth_credentials.json"
CLIENT_SECRET_FILE = "client_secret.json"
HEADLESS_AUTH = False

GENERIC_REQUEST_ERROR = "Returned an error response for your request."
NO_LIVE_VERSION_ERROR = "Published container version not found"
BACKEND_ERROR = "Backend Error"
RATE_LIMIT_ERROR = "Quota exceeded for quota group"

DEFAULT_HTTP_TIMEOUT_SEC = 60
RATE_LIMIT_CALLS = 24
RATE_LIMIT_PERIOD = 100
