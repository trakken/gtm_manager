# pylint: disable=missing-docstring
from unittest.mock import patch
from gtm_manager.base import GTMBase


@patch("gtm_manager.utils_auth.build_http")
def test_base_service(build_http_mock, mock_service):
    service, _ = mock_service()
    base = GTMBase(service=service)
    assert base.service == service

    build_http_mock.assert_not_called()


@patch("gtm_manager.utils_auth.get_credentials")
@patch("googleapiclient.discovery.build")
def test_base_credentials_empty(build_mock, get_credentials_mock):
    get_credentials_mock.return_value = True
    build_mock.return_value = True

    GTMBase(service=None, credentials=None)

    get_credentials_mock.assert_called()
    build_mock.assert_called()


@patch("gtm_manager.utils_auth.get_credentials")
@patch("googleapiclient.discovery.build")
def test_base_credentials_true(build_mock, get_credentials_mock):
    get_credentials_mock.return_value = True
    build_mock.return_value = True

    GTMBase(service=None, credentials=True)

    get_credentials_mock.assert_not_called()
    build_mock.assert_called()
