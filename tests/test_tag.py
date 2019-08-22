# pylint: disable=missing-docstring
from gtm_manager.tag import GTMTag
from gtm_manager.parameter import GTMParameter


def test_init(mock_service):
    service, responses = mock_service("tag_get.json")
    tag_get = responses[0]

    tag = GTMTag(
        path="accounts/1234/containers/1234/workspaces/1/tags/3", service=service
    )

    assert tag.paused == tag_get.get("paused")
    assert tag.setupTag == tag_get.get("setupTag")
    assert tag.firingRuleId == tag_get.get("firingRuleId", [])
    assert tag.accountId == tag_get.get("accountId")
    assert tag.teardownTag == tag_get.get("teardownTag")
    assert tag.priority == tag_get.get("priority")
    assert tag.workspaceId == tag_get.get("workspaceId")
    assert tag.parentFolderId == tag_get.get("parentFolderId")
    assert tag.scheduleStartMs == tag_get.get("scheduleStartMs")
    assert tag.scheduleEndMs == tag_get.get("scheduleEndMs")
    assert tag.containerId == tag_get.get("containerId")
    assert tag.tagFiringOption == tag_get.get("tagFiringOption")
    assert tag.tagId == tag_get.get("tagId")
    assert tag.blockingRuleId == tag_get.get("blockingRuleId", [])
    assert tag.tagManagerUrl == tag_get.get("tagManagerUrl")
    assert tag.fingerprint == tag_get.get("fingerprint")
    assert tag.firingTriggerId == tag_get.get("firingTriggerId", [])
    assert tag.name == tag_get.get("name")
    assert tag.type == tag_get.get("type")
    assert tag.notes == tag_get.get("notes")
    assert tag.liveOnly == tag_get.get("liveOnly")
    assert tag.blockingTriggerId == tag_get.get("blockingTriggerId", [])
    assert tag.path == tag_get.get("path")
    assert len(tag.parameter) == len(tag_get.get("parameter"))
    assert isinstance(tag.parameter[0], GTMParameter)

    tag = GTMTag(
        tag=tag_get,
        parent="accounts/1234/containers/1234/workspaces/1",
        service=service,
    )

    assert tag.paused == tag_get.get("paused")
    assert tag.setupTag == tag_get.get("setupTag")
    assert tag.firingRuleId == tag_get.get("firingRuleId", [])
    assert tag.accountId == tag_get.get("accountId")
    assert tag.teardownTag == tag_get.get("teardownTag")
    assert tag.priority == tag_get.get("priority")
    assert tag.workspaceId == tag_get.get("workspaceId")
    assert tag.parentFolderId == tag_get.get("parentFolderId")
    assert tag.scheduleStartMs == tag_get.get("scheduleStartMs")
    assert tag.scheduleEndMs == tag_get.get("scheduleEndMs")
    assert tag.containerId == tag_get.get("containerId")
    assert tag.tagFiringOption == tag_get.get("tagFiringOption")
    assert tag.tagId == tag_get.get("tagId")
    assert tag.blockingRuleId == tag_get.get("blockingRuleId", [])
    assert tag.tagManagerUrl == tag_get.get("tagManagerUrl")
    assert tag.fingerprint == tag_get.get("fingerprint")
    assert tag.firingTriggerId == tag_get.get("firingTriggerId", [])
    assert tag.name == tag_get.get("name")
    assert tag.type == tag_get.get("type")
    assert tag.notes == tag_get.get("notes")
    assert tag.liveOnly == tag_get.get("liveOnly")
    assert tag.blockingTriggerId == tag_get.get("blockingTriggerId", [])
    assert tag.path == tag_get.get("path")
    assert len(tag.parameter) == len(tag_get.get("parameter"))
    assert isinstance(tag.parameter[0], GTMParameter)


def test_update(mock_service):
    service, responses = mock_service("tag_get.json", "echo_request_body")
    tag_get = responses[0]

    tag = GTMTag(
        path="accounts/1234/containers/1234/workspaces/1/tags/3", service=service
    )

    update = {"name": "New Tag Name 1", "notes": "New Tag Notes"}

    new_paramter = {"type": "boolean", "key": "supportDocumentWrite", "value": "true"}

    tag.update(parameter=[GTMParameter(new_paramter)], **update)

    tag_get_updated = {**tag_get, **update}
    tag_get_updated["parameter"][1] = new_paramter

    assert tag.name == tag_get_updated.get("name")
    assert tag.notes == tag_get_updated.get("notes")
    assert len(tag.parameter) == len(tag_get_updated.get("parameter"))
    assert isinstance(tag.parameter[0], GTMParameter)

    assert tag.parameter[1].value == new_paramter["value"]


def test_delete(mock_service):
    service, _ = mock_service("tag_get.json", "echo_request_body")

    tag = GTMTag(
        path="accounts/1234/containers/1234/workspaces/1/tags/3", service=service
    )

    tag.delete()
