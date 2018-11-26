"""test_manager"""
from gtm_manager.manager import GTMManager
from gtm_manager.account import GTMAccount


def test_list_accounts(mock_service):
    """test_list_accounts"""
    service, responses = mock_service("account_list.json")
    account_list_dict = responses[0]

    manager = GTMManager(service=service)
    accounts = manager.list_accounts()

    assert len(accounts) == len(account_list_dict["account"])
    assert isinstance(accounts[0], GTMAccount)
