# pylint: disable=missing-docstring
from gtm_manager.variable import GTMVariable
from gtm_manager.parameter import GTMParameter


def test_init(mock_service):
    service, responses = mock_service("variable_get.json")
    variable_get = responses[0]

    variable = GTMVariable(
        path="accounts/1234/containers/1234/workspaces/1/variables/3", service=service
    )

    assert variable.scheduleStartMs == variable_get.get("scheduleStartMs")
    assert variable.scheduleEndMs == variable_get.get("scheduleEndMs")
    assert variable.name == variable_get.get("name")
    assert variable.variableId == variable_get.get("variableId")
    assert variable.type == variable_get.get("type")
    assert variable.notes == variable_get.get("notes")
    assert variable.enablingTriggerId == variable_get.get("enablingTriggerId")
    assert variable.workspaceId == variable_get.get("workspaceId")
    assert variable.tagManagerUrl == variable_get.get("tagManagerUrl")
    assert variable.fingerprint == variable_get.get("fingerprint")
    assert variable.accountId == variable_get.get("accountId")
    assert variable.parentFolderId == variable_get.get("parentFolderId")
    assert variable.disablingTriggerId == variable_get.get("disablingTriggerId")
    assert variable.containerId == variable_get.get("containerId")

    assert variable.path == variable_get.get("path")

    assert len(variable.parameter) == len(variable_get.get("parameter"))


def test_update(mock_service):
    service, responses = mock_service("variable_get.json", "echo_request_body")
    variable_get = responses[0]

    variable = GTMVariable(
        path="accounts/1234/containers/1234/workspaces/1/variables/3", service=service
    )

    update = {"name": "New Variable Name 1", "notes": "New Variable Notes"}

    new_paramter = {"type": "template", "key": "value", "value": "brandss"}

    variable.update(parameter=[GTMParameter(new_paramter)], **update)

    variable_get_updated = {**variable_get, **update}
    variable_get_updated["parameter"][0] = new_paramter

    assert variable.name == variable_get_updated.get("name")
    assert variable.notes == variable_get_updated.get("notes")
    assert len(variable.parameter) == len(variable_get_updated.get("parameter"))
    assert isinstance(variable.parameter[0], GTMParameter)

    assert variable.parameter[0].value == new_paramter["value"]


def test_delete(mock_service):
    service, _ = mock_service("variable_get.json", "echo_request_body")

    variable = GTMVariable(
        path="accounts/1234/containers/1234/workspaces/1/variables/3", service=service
    )

    variable.delete()
