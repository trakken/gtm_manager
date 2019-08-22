# pylint: disable=missing-docstring
from gtm_manager.permission import GTMContainerAccess, GTMPermission


def test_permission_init(mock_service):
    service, responses = mock_service("permission_get.json")
    permission_get = responses[0]

    permission = GTMPermission(
        path="accounts/1234/containers/1234/workspace/1/folders/1", service=service
    )

    assert len(permission.containerAccess) == len(
        permission_get.get("containerAccess", [])
    )
    assert isinstance(permission.containerAccess[0], GTMContainerAccess)
    assert permission.path == permission_get.get("path")
    assert permission.accountAccess == permission_get.get("accountAccess")
    assert permission.emailAddress == permission_get.get("emailAddress")
    assert permission.accountId == permission_get.get("accountId")

    permission = GTMPermission(permission=permission_get, service=service)

    assert len(permission.containerAccess) == len(
        permission_get.get("containerAccess", [])
    )
    assert isinstance(permission.containerAccess[0], GTMContainerAccess)
    assert permission.path == permission_get.get("path")
    assert permission.accountAccess == permission_get.get("accountAccess")
    assert permission.emailAddress == permission_get.get("emailAddress")
    assert permission.accountId == permission_get.get("accountId")


def test_container_access():
    container_access_dict = {"containerId": "123456", "permission": "publish"}

    container_access = GTMContainerAccess(containerAccess=container_access_dict)

    assert container_access.containerId == container_access_dict.get("containerId")
    assert container_access.permission == container_access_dict.get("permission")


# def test_permission_update(mock_service):
#     pass


# def test_permission_delete(mock_service):
#     pass
