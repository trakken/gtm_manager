# pylint: disable=missing-docstring, redefined-outer-name
import os
import json

import pytest

from googleapiclient.http import HttpMockSequence
from googleapiclient.discovery import build

from gtm_manager import SERVICE_NAME, SERVICE_VERSION

HTTP_MOCK_KEYWORDS = [
    "echo_request_headers",
    "echo_request_headers_as_json",
    "echo_request_body",
    "echo_request_uri",
]


@pytest.fixture
def data_file():
    def func(file_name, data_dir="data"):
        if file_name in HTTP_MOCK_KEYWORDS:
            return file_name

        data_dir = os.path.join(os.path.dirname(__file__), data_dir)

        with open(os.path.join(data_dir, file_name)) as file:
            return file.read()

    return func


@pytest.fixture
def mock_service(data_file):
    def func(*args):
        arg_files = [data_file(x) for x in list(args)]

        sequence = [
            ({"status": "200"}, x)
            for x in [data_file("tagmanager_v2_discovery.json"), *arg_files]
        ]

        http = HttpMockSequence(sequence)
        return (
            build(SERVICE_NAME, SERVICE_VERSION, http=http, cache_discovery=False),
            [json.loads(x) if x not in HTTP_MOCK_KEYWORDS else x for x in arg_files],
        )

    return func
