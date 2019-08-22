# pylint: disable=missing-docstring
from gtm_manager.container import GTMContainer
from gtm_manager.workspace import GTMWorkspace
from gtm_manager.version import GTMVersionHeader, GTMVersion


def test_init_container(mock_service):
    service, responses = mock_service("container_get.json")
    container_get_dict = responses[0]

    container = GTMContainer(path="accounts/12345/containers/12345", service=service)

    assert container.publicId == container_get_dict["publicId"]
    assert container.containerId == container_get_dict["accountId"]
    assert container.domainName == container_get_dict.get("domainName", [""])
    assert container.notes == container_get_dict["notes"]
    assert container.tagManagerUrl == container_get_dict["tagManagerUrl"]
    assert container.usageContext == container_get_dict["usageContext"]
    assert container.fingerprint == container_get_dict["fingerprint"]
    assert container.path == container_get_dict["path"]
    assert container.accountId == container_get_dict["accountId"]
    assert container.name == container_get_dict["name"]

    container_2 = GTMContainer(container=container_get_dict, service=service)

    assert container_2.publicId == container_get_dict["publicId"]
    assert container_2.containerId == container_get_dict["accountId"]
    assert container_2.domainName == container_get_dict["domainName"]
    assert container_2.notes == container_get_dict["notes"]
    assert container_2.tagManagerUrl == container_get_dict["tagManagerUrl"]
    assert container_2.usageContext == container_get_dict["usageContext"]
    assert container_2.fingerprint == container_get_dict["fingerprint"]
    assert container_2.path == container_get_dict["path"]
    assert container_2.accountId == container_get_dict["accountId"]
    assert container_2.name == container_get_dict["name"]


def test_live_version(mock_service):
    service, _ = mock_service("container_get.json", "version_get.json")

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    live_version = container.live_version()
    assert isinstance(live_version, GTMVersion)

    container.live_version(refresh=False)


def test_create_workspace(mock_service):
    service, _ = mock_service("container_get.json", "workspace_get.json")

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    workspace = container.create_workspace(
        "New Workspace", description="Workspace Description"
    )
    assert isinstance(workspace, GTMWorkspace)


def test_list_workspaces(mock_service):
    service, responses = mock_service("container_get.json", "workspace_list.json")
    workspace_list_dict = responses[1]

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    workspace_list = container.list_workspaces()
    assert len(workspace_list) == len(workspace_list_dict["workspace"])
    assert isinstance(workspace_list[0], GTMWorkspace)

    container.list_workspaces(refresh=False)


def test_list_workspaces_empty(mock_service):
    service, _ = mock_service("container_get.json", "empty.json")

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    workspace_list = container.list_workspaces()
    assert workspace_list == []

    container.list_workspaces(refresh=False)


def test_list_version_headers(mock_service):
    service, responses = mock_service("container_get.json", "version_headers_list.json")
    version_headers_dict = responses[1]

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    container_list = container.list_version_headers()
    assert len(container_list) == len(version_headers_dict["containerVersionHeader"])
    assert isinstance(container_list[0], GTMVersionHeader)

    container.list_version_headers(refresh=False)


def test_list_version_headers_empty(mock_service):
    service, _ = mock_service("container_get.json", "empty.json")

    container = GTMContainer(path="accounts/1234/containers/1234", service=service)

    container_list = container.list_version_headers()
    assert container_list == []

    container.list_version_headers(refresh=False)
