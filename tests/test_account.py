"""test_account"""
from gtm_manager.account import GTMAccount
from gtm_manager.container import GTMContainer
from gtm_manager.permission import GTMPermission


def test_init(mock_service):
    """test_list_accounts"""
    service, responses = mock_service("account_get.json")
    account_get_dict = responses[0]

    account = GTMAccount(path="accounts/1234567", service=service)

    assert account.path == account_get_dict["path"]
    assert account.accountId == account_get_dict["accountId"]
    assert account.name == account_get_dict["name"]
    assert account.fingerprint == account_get_dict["fingerprint"]
    assert account.tagManagerUrl == account_get_dict["tagManagerUrl"]

    account_2 = GTMAccount(account=account_get_dict, service=service)

    assert account.path == account_2.path
    assert account.accountId == account_2.accountId
    assert account.name == account_2.name
    assert account.fingerprint == account_2.fingerprint
    assert account.tagManagerUrl == account_2.tagManagerUrl


def test_list_containers(mock_service):
    """test_list_containers"""
    service, responses = mock_service("account_get.json", "containers_list.json")
    container_list_dict = responses[1]

    account = GTMAccount(path="accounts/1234567", service=service)

    container_list = account.list_containers()
    assert len(container_list) == len(container_list_dict["container"])
    assert isinstance(container_list[0], GTMContainer)

    account.list_containers(refresh=False)


def test_list_permissions(mock_service):
    """test_list_containers"""
    service, responses = mock_service("account_get.json", "permissions_list.json")
    permissions_list_dict = responses[1]

    account = GTMAccount(path="accounts/1234567", service=service)

    permissions_list = account.list_permissions()
    assert len(permissions_list) == len(permissions_list_dict["userPermission"])
    assert isinstance(permissions_list[0], GTMPermission)

    account.list_permissions(refresh=False)


def test_update(mock_service):
    """test_list_containers"""
    service, repsonses = mock_service("account_get.json", "account_update.json")
    account_update = repsonses[1]

    account = GTMAccount(path="accounts/1234567", service=service)

    account.update("name", True)

    assert account.name == account_update["name"]
    assert account.shareData == account_update["shareData"]


def test_create_container(mock_service):
    """test_create_container"""
    service, repsonses = mock_service("account_get.json", "container_get.json")
    container_get = repsonses[1]

    account = GTMAccount(path="accounts/1234567", service=service)

    container = account.create_container(container_get["name"])

    assert isinstance(container, GTMContainer)
    assert container.name == container_get["name"]
    assert container.publicId == container_get["publicId"]
    assert container.containerId == container_get["containerId"]
    assert container.domainName == container_get.get("domainName", "")
    assert container.notes == container_get.get("notes", "")
    assert container.tagManagerUrl == container_get["tagManagerUrl"]
    assert container.usageContext == container_get["usageContext"]
    assert container.fingerprint == container_get["fingerprint"]
    assert container.path == container_get["path"]
    assert container.accountId == container_get["accountId"]
