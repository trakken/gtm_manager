# pylint: disable=missing-docstring
from gtm_manager.built_in_variable import GTMBuiltInVariable


def test_init(mock_service):
    _, responses = mock_service("built_in_variables_get.json")
    built_in_variable_get = responses[0]

    built_in_variable = GTMBuiltInVariable(built_in_variable_get)

    assert built_in_variable.path == built_in_variable_get.get("path")
    assert built_in_variable.accountId == built_in_variable_get.get("accountId")
    assert built_in_variable.containerId == built_in_variable_get.get("containerId")
    assert built_in_variable.workspaceId == built_in_variable_get.get("workspaceId")
    assert built_in_variable.type == built_in_variable_get.get("type")
    assert built_in_variable.name == built_in_variable_get.get("name")
