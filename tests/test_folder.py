# pylint: disable=missing-docstring
from gtm_manager.folder import GTMFolder


def test_init(mock_service):
    service, responses = mock_service("folders_get.json")
    folder_get = responses[0]

    folder = GTMFolder(
        path="accounts/1234/containers/1234/workspace/1/folders/1", service=service
    )

    assert folder.containerId == folder_get.get("containerId")
    assert folder.notes == folder_get.get("notes", "")
    assert folder.workspaceId == folder_get.get("workspaceId")
    assert folder.tagManagerUrl == folder_get.get("tagManagerUrl")
    assert folder.fingerprint == folder_get.get("fingerprint")
    assert folder.folderId == folder_get.get("folderId")
    assert folder.accountId == folder_get.get("accountId")
    assert folder.name == folder_get.get("name")

    folder = GTMFolder(folder=folder_get, service=service)

    assert folder.containerId == folder_get.get("containerId")
    assert folder.notes == folder_get.get("notes", "")
    assert folder.workspaceId == folder_get.get("workspaceId")
    assert folder.tagManagerUrl == folder_get.get("tagManagerUrl")
    assert folder.fingerprint == folder_get.get("fingerprint")
    assert folder.folderId == folder_get.get("folderId")
    assert folder.accountId == folder_get.get("accountId")
    assert folder.name == folder_get.get("name")


def test_update():
    pass


def test_delete(mock_service):
    service, _ = mock_service("folders_get.json", "echo_request_body")

    folder = GTMFolder(
        path="accounts/1234/containers/1234/workspace/1/folders/1", service=service
    )

    folder.delete()
