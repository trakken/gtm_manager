# pylint: disable=missing-docstring
from gtm_manager.parameter import GTMParameter


def test_init():
    parameter_dict = {
        "type": "boolean",
        "key": "supportDocumentWrite",
        "value": "false",
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter.map == parameter_dict.get("map")
    assert parameter.value == parameter_dict.get("value")
    assert parameter.key == parameter_dict.get("key")
    assert parameter.type == parameter_dict.get("type")

    assert parameter.list == parameter_dict.get("list")

    parameter_dict = {
        "type": "list",
        "key": "fieldsToSet",
        "list": [{"type": "map", "key": "anonymizeIp", "value": "true"}],
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter.map == parameter_dict.get("map")
    assert parameter.value == parameter_dict.get("value")
    assert parameter.key == parameter_dict.get("key")
    assert parameter.type == parameter_dict.get("type")

    assert len(parameter.list) == len(parameter_dict.get("list"))
    assert isinstance(parameter.list[0], GTMParameter)


def test_to_obj():

    parameter_dict = {
        "type": "boolean",
        "key": "supportDocumentWrite",
        "value": "false",
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter_dict == parameter.to_obj()

    parameter_dict = {
        "type": "list",
        "key": "fieldsToSet",
        "list": [{"type": "map", "key": "anonymizeIp", "value": "true"}],
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter_dict == parameter.to_obj()


def test_copy():
    parameter_dict = {
        "type": "boolean",
        "key": "supportDocumentWrite",
        "value": "false",
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter_dict == parameter.copy().to_obj()

    parameter_dict = {
        "type": "list",
        "key": "fieldsToSet",
        "list": [{"type": "map", "key": "anonymizeIp", "value": "true"}],
    }

    parameter = GTMParameter(parameter_dict)

    assert parameter_dict == parameter.copy().to_obj()
