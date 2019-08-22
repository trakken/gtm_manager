# pylint: disable=missing-docstring
from gtm_manager.workspace import GTMWorkspace
from gtm_manager.version import GTMVersion
from gtm_manager.tag import GTMTag
from gtm_manager.trigger import GTMTrigger
from gtm_manager.variable import GTMVariable
from gtm_manager.folder import GTMFolder
from gtm_manager.built_in_variable import GTMBuiltInVariable


def test_init_workspace(mock_service):
    service, responses = mock_service("workspace_get.json")
    workspace_get_dict = responses[0]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    assert workspace.description == workspace_get_dict["description"]
    assert workspace.name == workspace_get_dict["name"]
    assert workspace.workspaceId == workspace_get_dict["workspaceId"]
    assert workspace.tagManagerUrl == workspace_get_dict["tagManagerUrl"]
    assert workspace.fingerprint == workspace_get_dict["fingerprint"]
    assert workspace.path == workspace_get_dict["path"]
    assert workspace.accountId == workspace_get_dict["accountId"]
    assert workspace.containerId == workspace_get_dict["containerId"]

    workspace = GTMWorkspace(workspace=workspace_get_dict, service=service)

    assert workspace.description == workspace_get_dict["description"]
    assert workspace.name == workspace_get_dict["name"]
    assert workspace.workspaceId == workspace_get_dict["workspaceId"]
    assert workspace.tagManagerUrl == workspace_get_dict["tagManagerUrl"]
    assert workspace.fingerprint == workspace_get_dict["fingerprint"]
    assert workspace.path == workspace_get_dict["path"]
    assert workspace.accountId == workspace_get_dict["accountId"]
    assert workspace.containerId == workspace_get_dict["containerId"]


def test_quick_preview(mock_service):
    service, _ = mock_service("workspace_get.json", "quick_preview_get.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    quick_preview = workspace.quick_preview()

    assert isinstance(quick_preview, GTMVersion)

    quick_preview = workspace.quick_preview(refresh=False)


def test_delete(mock_service):
    service, _ = mock_service("workspace_get.json", "echo_request_body")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    workspace.delete()


def test_clear_all_assets(mock_service):
    service, _ = mock_service(
        "workspace_get.json",
        "quick_preview_get.json",
        "echo_request_body",  # tags
        "echo_request_body",  # trigger
        "echo_request_body",  # variables
        "echo_request_body",  # variables
        "quick_preview_get_empty.json",
    )

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    workspace.clear_all_assets()


def test_trigger_map(mock_service):
    service, responses = mock_service("workspace_get.json", "quick_preview_get.json")
    quick_preview_get = responses[1]["containerVersion"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    trigger_map = workspace.trigger_map()

    key_list = list(trigger_map.keys())
    value_list = list(trigger_map.values())

    # name and id for each trigger, "All Pages" name and id
    assert len(key_list) == len(quick_preview_get["trigger"]) * 2 + 2

    for trigger in quick_preview_get["trigger"]:
        assert trigger["name"] in key_list
        assert trigger["triggerId"] in key_list

        assert trigger["name"] in value_list
        assert trigger["triggerId"] in value_list


def test_folder_map(mock_service):
    service, responses = mock_service("workspace_get.json", "quick_preview_get.json")
    quick_preview_get = responses[1]["containerVersion"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    folder_map = workspace.folder_map()

    key_list = list(folder_map.keys())
    value_list = list(folder_map.values())

    assert len(key_list) == len(quick_preview_get["folder"]) * 2

    for folder in quick_preview_get["folder"]:
        assert folder["name"] in key_list
        assert folder["folderId"] in key_list

        assert folder["name"] in value_list
        assert folder["folderId"] in value_list


def test_disable_built_ins(mock_service):

    service, _ = mock_service("workspace_get.json", "built_in_variables_get.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    workspace.disable_built_ins(["clickElement"])


def test_create_tag(mock_service):
    service, responses = mock_service("workspace_get.json", "tag_get.json")
    tag_get = responses[1]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    tag = workspace.create_tag(
        {
            "name": "Tag 1",
            "type": "html",
            "parameter": [
                {
                    "type": "template",
                    "key": "html",
                    "value": '<script>console.log("Hello")</script>',
                },
                {"type": "boolean", "key": "supportDocumentWrite", "value": "false"},
            ],
        }
    )

    assert isinstance(tag, GTMTag)
    assert tag.path == tag_get.get("path")


def test_create_trigger(mock_service):
    service, responses = mock_service("workspace_get.json", "trigger_get.json")
    trigger_get = responses[1]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    trigger = workspace.create_trigger(
        {
            "name": "Trigger 1",
            "type": "linkClick",
            "filter": [
                {
                    "type": "matchRegex",
                    "parameter": [
                        {"type": "template", "key": "arg0", "value": "{{Click URL}}"},
                        {"type": "template", "key": "arg1", "value": "pdf"},
                        {"type": "boolean", "key": "ignore_case", "value": "true"},
                    ],
                }
            ],
            "autoEventFilter": [
                {
                    "type": "matchRegex",
                    "parameter": [
                        {"type": "template", "key": "arg0", "value": "{{Page URL}}"},
                        {"type": "template", "key": "arg1", "value": ".*"},
                    ],
                }
            ],
        }
    )

    assert isinstance(trigger, GTMTrigger)
    assert trigger.path == trigger_get.get("path")


def test_create_variable(mock_service):
    service, responses = mock_service("workspace_get.json", "variable_get.json")
    variable_get = responses[1]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    variable = workspace.create_variable(
        {
            "name": "const.brand",
            "type": "c",
            "parameter": [{"type": "template", "key": "value", "value": "brand"}],
            "parentFolderId": "13",
        }
    )

    assert isinstance(variable, GTMVariable)
    assert variable.path == variable_get.get("path")


def test_create_folder(mock_service):
    service, responses = mock_service("workspace_get.json", "folders_get.json")
    folder_get = responses[1]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    new_folder = workspace.create_folder("Folder 1", notes="Folder 1 Note")

    assert isinstance(new_folder, GTMFolder)
    assert new_folder.name == folder_get.get("name")
    assert new_folder.notes == folder_get.get("notes", "")


def test_create_build_ins(mock_service):
    service, responses = mock_service(
        "workspace_get.json", "built_in_variables_get.json"
    )
    built_in_variables_get = responses[1]["builtInVariable"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    new_built_ins = workspace.create_build_ins(["clickText", "clickId"])

    assert isinstance(new_built_ins[0], GTMBuiltInVariable)
    assert new_built_ins[0].name == built_in_variables_get[0].get("name")
    assert new_built_ins[0].type == built_in_variables_get[0].get("type")
    assert new_built_ins[1].name == built_in_variables_get[1].get("name")
    assert new_built_ins[1].type == built_in_variables_get[1].get("type")


def test_list_tags(mock_service):
    service, responses = mock_service("workspace_get.json", "tags_list.json")
    tags_list = responses[1]["tag"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    tags = workspace.list_tags(refresh=True)

    assert isinstance(tags[0], GTMTag)
    assert len(tags) == len(tags_list)

    workspace.list_tags(refresh=False)


def test_list_tags_empty(mock_service):
    service, _ = mock_service("workspace_get.json", "empty.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    tags = workspace.list_tags(refresh=True)

    assert tags == []

    workspace.list_tags(refresh=False)


def test_list_triggers(mock_service):
    service, responses = mock_service("workspace_get.json", "triggers_list.json")
    triggers_list = responses[1]["trigger"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    triggers = workspace.list_triggers(refresh=True)

    assert isinstance(triggers[0], GTMTrigger)
    assert len(triggers) == len(triggers_list)

    workspace.list_triggers(refresh=False)


def test_list_triggers_empty(mock_service):
    service, _ = mock_service("workspace_get.json", "empty.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    triggers = workspace.list_triggers(refresh=True)

    assert triggers == []

    workspace.list_triggers(refresh=False)


def test_list_variables(mock_service):
    service, responses = mock_service("workspace_get.json", "variables_list.json")
    variables_list = responses[1]["variable"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    variables = workspace.list_variables(refresh=True)

    assert isinstance(variables[0], GTMVariable)
    assert len(variables) == len(variables_list)

    workspace.list_variables(refresh=False)


def test_list_variables_empty(mock_service):
    service, _ = mock_service("workspace_get.json", "empty.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    variables = workspace.list_variables(refresh=True)

    assert variables == []

    workspace.list_variables(refresh=False)


def test_list_folder(mock_service):
    service, responses = mock_service("workspace_get.json", "folders_list.json")
    folders_list = responses[1]["folder"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    folders = workspace.list_folders(refresh=True)

    assert isinstance(folders[0], GTMFolder)
    assert len(folders) == len(folders_list)

    workspace.list_folders(refresh=False)


def test_list_folder_empty(mock_service):
    service, _ = mock_service("workspace_get.json", "empty.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    folders = workspace.list_folders(refresh=True)

    assert folders == []

    workspace.list_folders(refresh=False)


def test_list_built_in_variables(mock_service):
    service, responses = mock_service(
        "workspace_get.json", "built_in_variables_list.json"
    )
    built_in_variables_list = responses[1]["builtInVariable"]

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    built_in_variables = workspace.list_built_in_variables(refresh=True)

    assert isinstance(built_in_variables[0], GTMBuiltInVariable)
    assert len(built_in_variables) == len(built_in_variables_list)

    workspace.list_built_in_variables(refresh=False)


def test_list_built_in_variables_empty(mock_service):
    service, _ = mock_service("workspace_get.json", "empty.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    built_in_variables = workspace.list_built_in_variables(refresh=True)

    assert isinstance(built_in_variables, list)
    assert built_in_variables == []

    workspace.list_built_in_variables(refresh=False)


def test_get_tag_by_name(mock_service):
    service, _ = mock_service("workspace_get.json", "tags_list.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    tag = workspace.get_tag_by_name("Tag 1", refresh=True)

    assert isinstance(tag, GTMTag)

    workspace.get_tag_by_name("Tag 1", refresh=False)


def test_get_trigger_by_name(mock_service):
    service, _ = mock_service("workspace_get.json", "triggers_list.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    trigger = workspace.get_trigger_by_name("Trigger 1", refresh=True)

    assert isinstance(trigger, GTMTrigger)

    workspace.get_trigger_by_name("Trigger 1", refresh=False)


def test_get_variable_by_name(mock_service):
    service, _ = mock_service("workspace_get.json", "variables_list.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )
    variable = workspace.get_variable_by_name("Variable 1", refresh=True)

    assert isinstance(variable, GTMVariable)

    workspace.get_variable_by_name("Variable 1", refresh=False)


def test_create_version(mock_service):
    service, _ = mock_service("workspace_get.json", "version_create.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    version = workspace.create_version("New Version", notes="New Version Notes")

    assert isinstance(version, GTMVersion)


def test_get_status(mock_service):
    service, _ = mock_service("workspace_get.json", "status_get.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    status = workspace.get_status()

    assert isinstance(status, dict)


def test_sync(mock_service):
    service, _ = mock_service("workspace_get.json", "sync_clean.json")

    workspace = GTMWorkspace(
        path="accounts/1234/containers/1234/workspaces/1", service=service
    )

    workspace.sync()
