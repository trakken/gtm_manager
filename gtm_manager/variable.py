"""variable.py"""
import copy

import gtm_manager.base
import gtm_manager.parameter
from gtm_manager.utils import param_dict


class GTMVariable(gtm_manager.base.GTMBase):
    """Open a specific GTM Variable.

    Args:
        trigger (dict): An API representation of the GTM trigger. If provided, the resource will be
            not be loaded from the API. :code:`trigger` or :code:`path` argument must be set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/containers/1234/workspaces/1234/trigger/123". If provided instead of
            :code:`trigger`, the representation will be loaded from the API. :code:`path` or
            :code:`trigger` argument must be set.
        parent (str): Required, when the instance is initialized with a trigger argument to
            explizitly set the parent path, i.e. "accounts/1234/containers/1234/workspaces/1234"
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, variable=None, path=None, parent=None, **kwargs):
        super().__init__(**kwargs)

        self.variables_service = (
            self.service.accounts().containers().workspaces().variables()
        )  # pylint: disable=E1101

        if variable:
            pass
        elif path:
            variable = self._get_variable(path)
        else:
            raise ValueError("Please pass either a container obj or container path.")

        self._scheduleStartMs = variable.get("scheduleStartMs")
        self._scheduleEndMs = variable.get("scheduleEndMs")
        self._name = variable.get("name")
        self._variableId = variable.get("variableId")
        self._type = variable.get("type")
        self._notes = variable.get("notes")
        self._enablingTriggerId = variable.get("enablingTriggerId")
        self._workspaceId = variable.get("workspaceId")
        self._tagManagerUrl = variable.get("tagManagerUrl")
        self._fingerprint = variable.get("fingerprint")
        self._accountId = variable.get("accountId")
        self._parameter = variable.get("parameter") or []
        self._parentFolderId = variable.get("parentFolderId")
        self._disablingTriggerId = variable.get("disablingTriggerId")
        self._containerId = variable.get("containerId")

        self._path = path or "{}/variables/{}".format(parent, self._variableId)

        self._parameter = [
            gtm_manager.parameter.GTMParameter(x) for x in self._parameter
        ]

    @property
    def scheduleStartMs(self):
        """str: The start timestamp in milliseconds to schedule a variable.
        """
        return self._scheduleStartMs

    @property
    def scheduleEndMs(self):
        """str: The end timestamp in milliseconds to schedule a variable.
        """
        return self._scheduleEndMs

    @property
    def name(self):
        """str: Variable display name.
        """
        return self._name

    @property
    def variableId(self):
        """str: The Variable ID uniquely identifies the GTM Variable.
        """
        return self._variableId

    @property
    def type(self):
        """str: GTM Variable Type.
        """
        return self._type

    @property
    def notes(self):
        """str: User notes on how to apply this variable in the container.
        """
        return self._notes

    @property
    def enablingTriggerId(self):
        """list: For mobile containers only - A list of trigger IDs for enabling
        conditional variables; the variable is enabled if one of the enabling
        triggers is true while all the disabling triggers are false.
        Treated as an unordered set.
        """
        return self._enablingTriggerId

    @property
    def workspaceId(self):
        """str: GTM Workspace ID.
        """
        return self._workspaceId

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Variable as computed at storage
        time. This value is recomputed whenever the variable is modified.
        """
        return self._fingerprint

    @property
    def path(self):
        """str: GTM Variable's API relative path.
        """
        return self._path

    @property
    def accountId(self):
        """str: GTM Account ID.
        """
        return self._accountId

    @property
    def parameter(self):
        """list: The variable's parameters.
        """
        return self._parameter

    @property
    def parentFolderId(self):
        """str: Parent folder id.
        """
        return self._parentFolderId

    @property
    def disablingTriggerId(self):
        """list: For mobile containers only - A list of trigger IDs for disabling
        conditional variables; the variable is enabled if one of the enabling
        trigger is true while all the disabling trigger are false. Treated as an
        unordered set.
        """
        return self._disablingTriggerId

    @property
    def containerId(self):
        """str: GTM Container ID.
        """
        return self._containerId

    @property
    def parameter_dict(self):
        """dict: GTM parameters acceable via their key value.
        """
        return param_dict(copy.deepcopy(self._parameter))

    def _get_variable(self, path):
        """_get_variable"""
        request = self.variables_service.get(path=path)
        response = request.execute()
        return response

    def constant_value(self):
        """constant_value"""
        if self.type == "c":
            return self.parameter[0]["value"]
        else:
            return None

    def update(self, refresh=False, parameter=None, **kwargs):
        """Update the current variable. The GTM API does not support a partial update. Therfore,
        this method will send all fields expliztily set in the method arguments and those cached in
        the instance properties.

        GTMParameters passed in a list as the :code:`parameter` argument, will be merged recursivly
        with the exsisting parameters based on their parameter key.

        All other API resource properties can be overwritten by specifying the property name as
        keyword arguments on the method call.

        Args:
            refresh (bool): Force a refresh of the entire GTMVariable instance to prevent implicitly
                sending stale property data.
            parameter (list): :class:`gtm_manager.parameter.GTMParameter` list to be merged
                recursivly with the exsisting parameters based on their parameter key.
            **kwargs: Additional resource properties to update with this call.

        Raises:
            ValueError
        """
        if refresh:
            self.__init__(path=self._path, service=self.service)

        default_asset = {
            "scheduleStartMs": self._scheduleStartMs,
            "scheduleEndMs": self._scheduleEndMs,
            "name": self._name,
            "variableId": self._variableId,
            "type": self._type,
            "notes": self._notes,
            "enablingTriggerId": self._enablingTriggerId,
            "workspaceId": self._workspaceId,
            "tagManagerUrl": self._tagManagerUrl,
            "fingerprint": self._fingerprint,
            "path": self._path,
            "accountId": self._accountId,
            "parentFolderId": self._parentFolderId,
            "disablingTriggerId": self._disablingTriggerId,
            "containerId": self._containerId,
        }
        update_asset = {**default_asset, **kwargs}

        if parameter:
            parameter_dict = {**param_dict(self._parameter), **param_dict(parameter)}
            parameter = list(parameter_dict.values())
        else:
            parameter = self._parameter

        update_asset["parameter"] = [x.to_obj() for x in parameter]

        update_asset = {k: v for k, v in update_asset.items() if v is not None}

        request = self.variables_service.update(path=self.path, body=update_asset)
        response = request.execute()
        self.__init__(variable=response, service=self.service)

    def delete(self):
        """Delete the current variable.
        """
        request = self.variables_service.delete(path=self._path)
        request.execute()
