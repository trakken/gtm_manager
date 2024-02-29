"""utils_auth.py"""
import json

from httplib2 import Http

import google.auth
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.errors import HttpError

from ratelimit import limits, sleep_and_retry, RateLimitException
from retrying import retry

from gtm_manager.exceptions import AuthError
from gtm_manager import (
    DEFAULT_HTTP_TIMEOUT_SEC,
    RATE_LIMIT_CALLS,
    RATE_LIMIT_PERIOD,
    BACKEND_ERROR,
    RATE_LIMIT_ERROR,
)


class LimittedHttp(Http):
    """LimittedHttp"""

    @retry(
        stop_max_attempt_number=6,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        retry_on_exception=lambda x: BACKEND_ERROR in str(x),
    )
    @retry(
        stop_max_attempt_number=6,
        wait_exponential_multiplier=10000,
        wait_exponential_max=100000,
        retry_on_exception=lambda x: RATE_LIMIT_ERROR in str(x),
    )
    @sleep_and_retry
    @limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
    def request(self, *args, **kwargs):
        """request"""
        try:
            return super().request(*args, **kwargs)
        except HttpError as error:
            if RATE_LIMIT_ERROR in str(error):
                raise RateLimitException("too many calls", RATE_LIMIT_PERIOD)
            raise error


def get_credentials():
    """get_credentials"""
    from . import AUTH_SCOPES, CLIENT_SECRET_FILE, SERVICE_PRIVATE_KEY, HEADLESS_AUTH, CREDENTIALS_FILE_NAME

    try:
        credentials, project = google.auth.default(scopes=AUTH_SCOPES)
        if credentials:
            return credentials
    except DefaultCredentialsError:
        credentials = None
        
    if SERVICE_PRIVATE_KEY:
      try: 
          credentials = service_account.Credentials.from_service_account_file(
            filename=SERVICE_PRIVATE_KEY, scopes=AUTH_SCOPES
          )
          if credentials:
              return credentials
      except FileNotFoundError:
          credentials = None
      except ValueError:
          credentials = None
            
    try:
        credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE_NAME)
    except FileNotFoundError:
        credentials = None
    except ValueError:
        credentials = None

    if credentials:
        return credentials

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=CLIENT_SECRET_FILE, scopes=AUTH_SCOPES
        )
    except FileNotFoundError:
        raise AuthError(
            "Please provide a client secrete file as %r" % CLIENT_SECRET_FILE
        )

    if not HEADLESS_AUTH:
        credentials = flow.run_local_server()
    else:
        credentials = flow.run_console()

    creds_data = {
        "token": None,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    with open(CREDENTIALS_FILE_NAME, "w") as outfile:
        json.dump(creds_data, outfile)

    return credentials


def build_http(credentials=None):
    """build_http"""
    if not credentials:
        credentials = get_credentials()
    return AuthorizedHttp(
        credentials, http=LimittedHttp(timeout=DEFAULT_HTTP_TIMEOUT_SEC)
    )
