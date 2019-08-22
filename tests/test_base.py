# pylint: disable=missing-docstring
from gtm_manager.base import GTMBase


def test_base(mock_service):
    service, _ = mock_service()
    base = GTMBase(service=service)
    assert base.service == service
    assert base.service.accounts()
