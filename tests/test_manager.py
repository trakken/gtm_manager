# pylint: disable=missing-docstring
from gtm_manager.manager import GTMManager
from gtm_manager.account import GTMAccount


def test_list_accounts(mock_service):
    service, responses = mock_service("account_list.json")
    account_list_dict = responses[0]

    manager = GTMManager(service=service)
    accounts = manager.list_accounts()

    assert len(accounts) == len(account_list_dict["account"])
    assert isinstance(accounts[0], GTMAccount)


def test_list_accounts_empty(mock_service):
    service, _ = mock_service("empty.json")

    manager = GTMManager(service=service)
    accounts = manager.list_accounts()

    assert accounts == []
