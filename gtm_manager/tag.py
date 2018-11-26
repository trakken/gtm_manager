"""tag.py"""
import copy

import gtm_manager.base
import gtm_manager.parameter
from gtm_manager.utils import param_dict


class GTMTag(gtm_manager.base.GTMBase):
    """Open a specific GTM Tag.

    Args:
        tag (dict): An API representation of the GTM Tag. If provided, the resource will be not be
            loaded from the API. :code:`tag` or :code:`path` argument must be set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/containers/1234/workspaces/1234/tags/123". If provided instead of
            :code:`tag`, the representation will be loaded from the API. :code:`path` or :code:`tag`
            argument must be set.
        parent (str): Required, when the instance is initialized with a :code:`tag` argument to
            explizitly set the parent path, i.e. "accounts/1234/containers/1234/workspaces/1234"
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, tag=None, path=None, parent=None, **kwargs):
        super().__init__(**kwargs)

        self.tags_service = (
            self.service.accounts().containers().workspaces().tags()
        )  # pylint: disable=E1101

        if tag:
            pass
        elif path:
            tag = self._get_tag(path)
        else:
            raise ValueError(
                "Please pass either a container obj and parent or container path."
            )

        self._paused = tag.get("paused")
        self._setupTag = tag.get("setupTag")
        self._firingRuleId = tag.get("firingRuleId", [])
        self._accountId = tag.get("accountId")
        self._teardownTag = tag.get("teardownTag")
        self._priority = tag.get("priority")
        self._workspaceId = tag.get("workspaceId")
        self._parameter = tag.get("parameter", [])
        self._parentFolderId = tag.get("parentFolderId")
        self._scheduleStartMs = tag.get("scheduleStartMs")
        self._scheduleEndMs = tag.get("scheduleEndMs")
        self._containerId = tag.get("containerId")
        self._tagFiringOption = tag.get("tagFiringOption")
        self._tagId = tag.get("tagId")
        self._blockingRuleId = tag.get("blockingRuleId", [])
        self._tagManagerUrl = tag.get("tagManagerUrl")
        self._fingerprint = tag.get("fingerprint")
        self._firingTriggerId = tag.get("firingTriggerId", [])
        self._name = tag.get("name")
        self._type = tag.get("type")
        self._notes = tag.get("notes")
        self._liveOnly = tag.get("liveOnly")
        self._blockingTriggerId = tag.get("blockingTriggerId", [])
        self._path = path or "{}/tags/{}".format(parent, self._tagId)

        self._parameter = [
            gtm_manager.parameter.GTMParameter(x) for x in self._parameter
        ]

    @property
    def paused(self):
        """bool: Indicates whether the tag is paused, which prevents the tag from firing.
        """
        return self._paused

    @property
    def setupTag(self):
        """list: The list of setup tags. Currently we only allow one.
        """
        return self._setupTag

    @property
    def firingRuleId(self):
        """bool: Firing rule IDs. A tag will fire when any of the listed rules are true and all of
        its blockingRuleIds (if any specified) are false.
        """
        return self._firingRuleId

    @property
    def accountId(self):
        """str: GTM Account ID.
        """
        return self._accountId

    @property
    def teardownTag(self):
        """list: The list of teardown tags. Currently we only allow one.
        """
        return self._teardownTag

    @property
    def priority(self):
        """obj: Represents a Google Tag Manager Parameter. # User defined numeric priority of the
        tag. Tags are fired asynchronously in order of priority. Tags with higher numeric value fire
        first. A tag's priority can be a positive or negative value. The default value is 0.
        """
        return self._priority

    @property
    def workspaceId(self):
        """str: GTM Workspace ID.
        """
        return self._workspaceId

    @property
    def parameter(self):
        """list: The tag's parameters.
        """
        return self._parameter

    @property
    def parentFolderId(self):
        """str: Parent folder id.
        """
        return self._parentFolderId

    @property
    def scheduleStartMs(self):
        """str: The start timestamp in milliseconds to schedule a tag.
        """
        return self._scheduleStartMs

    @property
    def scheduleEndMs(self):
        """str: The end timestamp in milliseconds to schedule a tag.
        """
        return self._scheduleEndMs

    @property
    def containerId(self):
        """str: GTM Container ID.
        """
        return self._containerId

    @property
    def tagFiringOption(self):
        """str: Option to fire this tag.
        """
        return self._tagFiringOption

    @property
    def tagId(self):
        """str: The Tag ID uniquely identifies the GTM Tag.
        """
        return self._tagId

    @property
    def blockingRuleId(self):
        """list: Blocking rule IDs. If any of the listed rules evaluate to true, the tag will not
        fire.
        """
        return self._blockingRuleId

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Tag as computed at storage time. This value is recomputed
        whenever the tag is modified.
        """
        return self._fingerprint

    @property
    def path(self):
        """str: GTM Tag's API relative path.
        """
        return self._path

    @property
    def firingTriggerId(self):
        """list: Firing trigger IDs. A tag will fire when any of the listed triggers are true and
        all of its blockingTriggerIds (if any specified) are false.
        """
        return self._firingTriggerId

    @property
    def name(self):
        """str: Tag display name.
        """
        return self._name

    @property
    def type(self):
        """str: GTM Tag Type.
        """
        return self._type

    @property
    def notes(self):
        """str: User notes on how to apply this tag in the container.
        """
        return self._notes

    @property
    def liveOnly(self):
        """bool: If set to true, this tag will only fire in the live environment (e.g. not in
        preview or debug mode).
        """
        return self._liveOnly

    @property
    def blockingTriggerId(self):
        """list: Blocking trigger IDs. If any of the listed triggers evaluate to true, the tag will
        not fire.
        """
        return self._blockingTriggerId

    @property
    def parameter_dict(self):
        """dict: Deepcopy of GTMParameters acceable via their key value.
        """
        return param_dict(copy.deepcopy(self._parameter))

    def update(self, refresh=False, parameter=None, **kwargs):
        """Update the current tag. The GTM API does not support a partial update. Therfore, this
        method will send all fields expliztily set in the method arguments and those cached in the 
        instance properties.

        GTMParameters passed in a list as the `parameter` argument, will be merged recursivly with
        the exsisting parameters based on their parameter key.

        All other API resource properties can be overwritten by specifying the property name as
        keyword arguments on the method call. 

        Args:
            refresh (bool): Force a refresh of the entire GTMTag instance to prevent implicitly
                sending stale property data.
            parameter (list): :class:`gtm_manager.parameter.GTMParameter` s to be merged recursivly
                with the exsisting parameters based on their parameter key.
            **kwargs: Additional resource properties to update with this call.

        Raises:
            ValueError
        """
        if parameter and not isinstance(parameter, list):
            raise ValueError(
                "'parameter' has to be a list of :class:`GTMParameters` or 'None'."
            )

        if refresh:
            self.__init__(path=self._path, service=self.service)

        default_asset = {
            "paused": self._paused,
            "setupTag": self._setupTag,
            "firingRuleId": self._firingRuleId,
            "teardownTag": self._teardownTag,
            "priority": self._priority,
            "parentFolderId": self._parentFolderId,
            "scheduleStartMs": self._scheduleStartMs,
            "scheduleEndMs": self._scheduleEndMs,
            "tagFiringOption": self._tagFiringOption,
            "blockingRuleId": self._blockingRuleId,
            "firingTriggerId": self._firingTriggerId,
            "name": self._name,
            "type": self._type,
            "notes": self._notes,
            "liveOnly": self._liveOnly,
            "blockingTriggerId": self._blockingTriggerId,
        }
        update_asset = {**default_asset, **kwargs}

        if parameter:
            parameter_dict = {**param_dict(self._parameter), **param_dict(parameter)}
            parameter = list(parameter_dict.values())
        else:
            parameter = self._parameter

        update_asset["parameter"] = [x.to_obj() for x in parameter]

        update_asset = {k: v for k, v in update_asset.items() if v is not None}

        request = self.tags_service.update(path=self.path, body=update_asset)
        response = request.execute()
        self.__init__(tag=response, service=self.service)

    def _get_tag(self, path):
        """_get_tag"""
        request = self.tags_service.get(path=path)
        response = request.execute()
        return response

    def delete(self):
        """Delete the current tag.
        """
        request = self.tags_service.delete(path=self._path)
        request.execute()
