# GTM Manager (WIP)

[![Documentation Status](https://img.shields.io/pypi/v/gtm-manager.svg)](https://pypi.org/project/gtm-manager/)
[![Documentation Status](https://readthedocs.org/projects/gtm-manager/badge/?version=latest)](https://gtm-manager.readthedocs.io/en/latest/?badge=latest)

An object-oriented helper library wrapping the [Tag Manager API Client Library for Python]("https://developers.google.com/api-client-library/python/apis/tagmanager/v2") for the [Google Tag Manager API]("https://developers.google.com/tag-manager/api/v2/").

[Documentation]("https://gtm-manager.readthedocs.io/en/latest/index.html")

## Installation from Source

```bash
python3 setup.py sdist
pip3 install gtm_manager --find-links $(pwd)/dist/
```

## Getting Started

Use a Google account to create application credentials, download the JSON file and put it in the same directory as your script with the name `client_secret.json`. During the first execution of any API-dependent library code, you will be prompted to perform the auth flow.

```python
from gtm_manager import GTMManager

accounts = GTMManager().list_accounts()

for account in account:
    print(account.name)
```

## Authentication

This library currently only supports user-based oauth crendentials. Service accounts can not be used.

When using any of the classes from the resources that require loading data from the Google Tag Manager API, the library will look for an existing in OAuth token in the credentials file or prompt the user to authorize which requires a client secret file.

### Client Secrets

The Google OAuth flows requires you to provide a [client id and secret]("https://developers.google.com/api-client-library/python/guide/aaa_client_secrets") in the from of a `JSON` file. You can create these in any Google Cloud or Google Developer project:

> 1. Open the Google API Console Credentials page.
> 2. From the project drop-down, choose Create a new project, enter a name for the project, and optionally, edit the provided Project ID. Click Create.
> 3. On the Credentials page, select Create credentials, then select OAuth client ID.
> 4. You may be prompted to set a product name on the Consent screen; if so, click Configure consent screen, supply the requested information, and click Save to return to the Credentials screen.
> 5. Select Other for the Application type, and enter any additional information required.
> 6. Click Create.
> 7. On the page that appears, you can download client id and secret as a JSON file.

By default, the `gtm_manager` will look for client id and secret in the file `client_secret.json`. You can overwrite the default to any file name with absolute or relative path:

```python
gtm_manager.CLIENT_SECRET_FILE = "my_client_secret.json"
```

### Credentials File

OAuth user credentials will be stored in plain text. During every invocation of API-dependent library code, the `gtm_manager` will try to open this file for credentials. If no credentials are present, a new auth flow with the provided client id and secret will be started.

The auth flow will request _offline_ access from the user providing the script with an oauth refresh token to continue using the file as long as the user not explicitly revokes access.

By default, the `gtm_manager` will look for existing and store new credentials in the file `auth_credentials.json`. You can overwrite the default to any file name with absolute or relative path:

```python
gtm_manager.CREDENTIALS_FILE_NAME = "my_auth_credentials.json"
```

### Scopes

The Google OAuth system uses scopes to request different types of account access from a user. The Google Tag Manager API uses seven different scopes. Different API methods requires different scopes. Details can be found in the [Google Tag Manager API Reference]("https://developers.google.com/tag-manager/api/v2/"). After initial authorisation, the stored credentials can not extend or chang their scope.

By default, the `gtm_manager` will request all seven scopes from a user during the auth flow. For ease of use, all scopes are defined as constants under `gtm_manager.GoogleTagManagerScopes`.

You can overwritte the requested scopes to an array of scope strings:

```python
gtm_manager.AUTH_SCOPES = [
    gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERS,
    gtm_manager.GoogleTagManagerScopes.PUBLISH,
]
```

### Auth Best Practice

Even though the default settings get you up and running quickly, it is recommended to always **explicitly** set your settings. Every `gtm_manager` script should therefore contain the following code block:

```python
# explicitly set the location of your client secret file
gtm_manager.CLIENT_SECRET_FILE = "my_client_secret.json"
# explicitly set the location of your credentials file
gtm_manager.CREDENTIALS_FILE_NAME = "my_auth_credentials.json"
# explicitly set the required scopes
gtm_manager.AUTH_SCOPES = [
    gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERS,
    gtm_manager.GoogleTagManagerScopes.PUBLISH,
]
```

## Usage Examples

The `gtm_manager` speeds up interaction working with the Google Tag Manager API for various use cases. Some of these use cases are demoed below. If you are missing a use case, please open an issue and we will be happy to help and extend the demo!

### List all GTM containers in an account

```python
# import gtm_manager
# from gtm_manager.manager import GTMManager

# gtm_manager.CLIENT_SECRET_FILE = "my_client_secret.json"
# gtm_manager.CREDENTIALS_FILE_NAME = "my_auth_credentials.json"
# gtm_manager.AUTH_SCOPES = [gtm_manager.GoogleTagManagerScopes.READONLY]

accounts = GTMManager().list_accounts()

for account in accounts:
    print(account.name)
```

### Add a new tag, trigger, variable to all containers in an account

```python
# import gtm_manager
# from gtm_manager.account import GTMAccount

# gtm_manager.CLIENT_SECRET_FILE = "my_client_secret.json"
# gtm_manager.CREDENTIALS_FILE_NAME = "my_auth_credentials.json"
# gtm_manager.AUTH_SCOPES = [
#     gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERS,
#     gtm_manager.GoogleTagManagerScopes.PUBLISH,
#     gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERVERSIONS,
# ]

account = GTMAccount(path="accounts/1234")
containers = account.list_containers()

for container in containers:
    workspace = container.create_workspace("Global Update Workspace")

    trigger = workspace.create_trigger(
        {
            "name": "Custom - Generic Event",
            "type": "CUSTOM_EVENT",
            "customEventFilter": [
                {
                    "type": "EQUALS",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                        {"type": "TEMPLATE", "key": "arg1", "value": "Generic Event"},
                    ],
                }
            ],
        }
    )

    variable = workspace.create_variable(
        {
            "name": "cjs.randomNumber",
            "type": "jsm",
            "parameter": [
                {
                    "type": "TEMPLATE",
                    "key": "javascript",
                    "value": "function() {\n  return Math.random();\n}",
                }
            ],
        }
    )

    workspace.create_tag(
        {
            "name": "HTML - Hello Log",
            "type": "html",
            "parameter": [
                {
                    "type": "TEMPLATE",
                    "key": "html",
                    "value": '<script>\n  console.log("Hello World")\n</script>',
                }
            ],
            "firingTriggerId": [trigger.triggerId],
        }
    )

    version = workspace.create_version("Global Update Workspace")
    version.publish()
```

### Update a Variable on a Tag

```python
# import gtm_manager
# from gtm_manager.account import GTMAccount

# gtm_manager.CLIENT_SECRET_FILE = "my_client_secret.json"
# gtm_manager.CREDENTIALS_FILE_NAME = "my_auth_credentials.json"
# gtm_manager.AUTH_SCOPES = [
#     gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERS,
#     gtm_manager.GoogleTagManagerScopes.EDIT_CONTAINERVERSIONS,
#     gtm_manager.GoogleTagManagerScopes.PUBLISH,
# ]

account = GTMAccount(path="accounts/1985550951")
containers = account.list_containers()

for container in containers:
    workspace = container.create_workspace("Global Update Workspace")

    tag = workspace.get_tag_by_name("UA - Pageview")

    doubleClick_param = tag.parameter_dict["doubleClick"]
    doubleClick_param.value = "false"

    tag.update(parameter=[doubleClick_param])

    version = workspace.create_version("Global Update Workspace")
    version.publish()
```
