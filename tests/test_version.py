# pylint: disable=missing-docstring
from gtm_manager.tag import GTMTag
from gtm_manager.version import GTMVersion
from gtm_manager.trigger import GTMTrigger
from gtm_manager.variable import GTMVariable
from gtm_manager.folder import GTMFolder
from gtm_manager.container import GTMContainer


def test_init(mock_service):
    service, responses = mock_service("version_get.json")
    version_get = responses[0]

    version = GTMVersion(
        path="accounts/1234/containers/1234/versions/1", service=service
    )

    assert version.containerId == version_get.get("containerId")
    assert version.zone == version_get.get("zone")
    assert version.deleted == version_get.get("deleted")
    assert version.description == version_get.get("description")
    assert version.builtInVariable == version_get.get("builtInVariable")
    assert version.name == version_get.get("name")
    assert version.tagManagerUrl == version_get.get("tagManagerUrl")
    assert version.containerVersionId == version_get.get("containerVersionId")
    assert version.fingerprint == version_get.get("fingerprint")
    assert version.accountId == version_get.get("accountId")
    assert version.path == version_get.get("path")

    assert isinstance(version.container, GTMContainer)
    assert all(isinstance(x, GTMTag) for x in version.tag)
    assert all(isinstance(x, GTMTrigger) for x in version.trigger)
    assert all(isinstance(x, GTMVariable) for x in version.variable)
    assert all(isinstance(x, GTMFolder) for x in version.folder)
    assert isinstance(version.raw_body, dict)

    version = GTMVersion(
        version=version_get, workspaceId="accounts/1234/containers/1234", service=service
    )

    assert version.containerId == version_get.get("containerId")
    assert version.zone == version_get.get("zone")
    assert version.deleted == version_get.get("deleted")
    assert version.description == version_get.get("description")
    assert version.builtInVariable == version_get.get("builtInVariable")
    assert version.name == version_get.get("name")
    assert version.tagManagerUrl == version_get.get("tagManagerUrl")
    assert version.containerVersionId == version_get.get("containerVersionId")
    assert version.fingerprint == version_get.get("fingerprint")
    assert version.accountId == version_get.get("accountId")
    assert version.path == version_get.get("path")

    assert isinstance(version.container, GTMContainer)
    assert all(isinstance(x, GTMTag) for x in version.tag)
    assert all(isinstance(x, GTMTrigger) for x in version.trigger)
    assert all(isinstance(x, GTMVariable) for x in version.variable)
    assert all(isinstance(x, GTMFolder) for x in version.folder)
    assert isinstance(version.raw_body, dict)
