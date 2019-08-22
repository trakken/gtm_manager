# pylint: disable=missing-docstring
from gtm_manager.trigger import GTMTrigger


def test_init(mock_service):
    service, responses = mock_service("trigger_get.json")
    trigger_get = responses[0]

    trigger = GTMTrigger(
        path="accounts/1234/containers/1234/workspaces/1/triggers/1", service=service
    )

    assert trigger.maxTimerLengthSeconds == trigger_get.get("maxTimerLengthSeconds")
    assert trigger.totalTimeMinMilliseconds == trigger_get.get(
        "totalTimeMinMilliseconds"
    )
    assert trigger.uniqueTriggerId == trigger_get.get("uniqueTriggerId")
    assert trigger.verticalScrollPercentageList == trigger_get.get(
        "verticalScrollPercentageList"
    )
    assert trigger.horizontalScrollPercentageList == trigger_get.get(
        "horizontalScrollPercentageList"
    )
    assert trigger.containerId == trigger_get.get("containerId")
    assert trigger.waitForTagsTimeout == trigger_get.get("waitForTagsTimeout")
    assert trigger.accountId == trigger_get.get("accountId")
    assert trigger.waitForTags == trigger_get.get("waitForTags")
    assert trigger.intervalSeconds == trigger_get.get("intervalSeconds")
    assert trigger.eventName == trigger_get.get("eventName")
    assert trigger.visibilitySelector == trigger_get.get("visibilitySelector")
    assert trigger.workspaceId == trigger_get.get("workspaceId")
    assert trigger.customEventFilter == trigger_get.get("customEventFilter")
    assert trigger.parentFolderId == trigger_get.get("parentFolderId")
    assert trigger.continuousTimeMinMilliseconds == trigger_get.get(
        "continuousTimeMinMilliseconds"
    )
    assert trigger.selector == trigger_get.get("selector")
    assert trigger.triggerId == trigger_get.get("triggerId")
    assert trigger.tagManagerUrl == trigger_get.get("tagManagerUrl")
    assert trigger.fingerprint == trigger_get.get("fingerprint")
    assert trigger.visiblePercentageMax == trigger_get.get("visiblePercentageMax")
    assert trigger.name == trigger_get.get("name")
    assert trigger.visiblePercentageMin == trigger_get.get("visiblePercentageMin")
    assert trigger.type == trigger_get.get("type")
    assert trigger.notes == trigger_get.get("notes")
    assert trigger.interval == trigger_get.get("interval")
    assert trigger.filter == trigger_get.get("filter")
    assert trigger.autoEventFilter == trigger_get.get("autoEventFilter")
    assert trigger.limit == trigger_get.get("limit")
    assert trigger.checkValidation == trigger_get.get("checkValidation")
    assert trigger.path == trigger_get.get("path")

    trigger = GTMTrigger(
        trigger=trigger_get,
        parent="accounts/1234/containers/1234/workspaces/1",
        service=service,
    )

    assert trigger.maxTimerLengthSeconds == trigger_get.get("maxTimerLengthSeconds")
    assert trigger.totalTimeMinMilliseconds == trigger_get.get(
        "totalTimeMinMilliseconds"
    )
    assert trigger.uniqueTriggerId == trigger_get.get("uniqueTriggerId")
    assert trigger.verticalScrollPercentageList == trigger_get.get(
        "verticalScrollPercentageList"
    )
    assert trigger.horizontalScrollPercentageList == trigger_get.get(
        "horizontalScrollPercentageList"
    )
    assert trigger.containerId == trigger_get.get("containerId")
    assert trigger.waitForTagsTimeout == trigger_get.get("waitForTagsTimeout")
    assert trigger.accountId == trigger_get.get("accountId")
    assert trigger.waitForTags == trigger_get.get("waitForTags")
    assert trigger.intervalSeconds == trigger_get.get("intervalSeconds")
    assert trigger.eventName == trigger_get.get("eventName")
    assert trigger.visibilitySelector == trigger_get.get("visibilitySelector")
    assert trigger.workspaceId == trigger_get.get("workspaceId")
    assert trigger.customEventFilter == trigger_get.get("customEventFilter")
    assert trigger.parentFolderId == trigger_get.get("parentFolderId")
    assert trigger.continuousTimeMinMilliseconds == trigger_get.get(
        "continuousTimeMinMilliseconds"
    )
    assert trigger.selector == trigger_get.get("selector")
    assert trigger.triggerId == trigger_get.get("triggerId")
    assert trigger.tagManagerUrl == trigger_get.get("tagManagerUrl")
    assert trigger.fingerprint == trigger_get.get("fingerprint")
    assert trigger.visiblePercentageMax == trigger_get.get("visiblePercentageMax")
    assert trigger.name == trigger_get.get("name")
    assert trigger.visiblePercentageMin == trigger_get.get("visiblePercentageMin")
    assert trigger.type == trigger_get.get("type")
    assert trigger.notes == trigger_get.get("notes")
    assert trigger.interval == trigger_get.get("interval")
    assert trigger.filter == trigger_get.get("filter")
    assert trigger.autoEventFilter == trigger_get.get("autoEventFilter")
    assert trigger.limit == trigger_get.get("limit")
    assert trigger.checkValidation == trigger_get.get("checkValidation")
    assert trigger.path == trigger_get.get("path")


def test_update(mock_service):
    service, responses = mock_service("trigger_get.json", "echo_request_body")
    trigger_get = responses[0]

    trigger = GTMTrigger(
        path="accounts/1234/containers/1234/workspaces/1/triggers/3", service=service
    )

    update = {"name": "New Trigger Name 1", "notes": "New Trigger Notes"}

    trigger.update(**update)

    trigger_get_updated = {**trigger_get, **update}

    assert trigger.name == trigger_get_updated.get("name")
    assert trigger.notes == trigger_get_updated.get("notes")


def test_delete(mock_service):
    service, _ = mock_service("trigger_get.json", "echo_request_body")

    trigger = GTMTrigger(
        path="accounts/1234/containers/1234/workspaces/1/triggers/1", service=service
    )

    trigger.delete()
