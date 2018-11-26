"""trigger.py"""
import gtm_manager.base
import gtm_manager.parameter
from gtm_manager.utils import param_dict


class GTMTrigger(gtm_manager.base.GTMBase):
    """Open a specific GTM Trigger.

    Args:
        trigger (dict): An API representation of the GTM Trigger. If provided, the resource will be
            not be loaded from the API. :code:`trigger` or :code:`path` argument must be set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/containers/1234/workspaces/1234/trigger/123". If provided instead of
            :code:`trigger`, the representation will be loaded from the API. :code:`path` or
            :code:`trigger` argument must be set.
        parent (str): Required, when the instance is initialized with a :code:`trigger` argument to
            explizitly set the parent path, i.e. "accounts/1234/containers/1234/workspaces/1234"
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, trigger=None, path=None, parent=None, **kwargs):
        super().__init__(**kwargs)

        self.triggers_service = (
            self.service.accounts().containers().workspaces().triggers()
        )  # pylint: disable=E1101

        if trigger:
            pass
        elif path:
            trigger = self._get_trigger(path)
        else:
            raise ValueError("Please pass either a container obj or container path.")

        self._maxTimerLengthSeconds = trigger.get("maxTimerLengthSeconds")
        self._totalTimeMinMilliseconds = trigger.get("totalTimeMinMilliseconds")
        self._uniqueTriggerId = trigger.get("uniqueTriggerId")
        self._verticalScrollPercentageList = trigger.get("verticalScrollPercentageList")
        self._horizontalScrollPercentageList = trigger.get(
            "horizontalScrollPercentageList"
        )
        self._containerId = trigger.get("containerId")
        self._waitForTagsTimeout = trigger.get("waitForTagsTimeout")
        self._accountId = trigger.get("accountId")
        self._waitForTags = trigger.get("waitForTags")
        self._intervalSeconds = trigger.get("intervalSeconds")
        self._eventName = trigger.get("eventName")
        self._visibilitySelector = trigger.get("visibilitySelector")
        self._workspaceId = trigger.get("workspaceId")
        self._customEventFilter = trigger.get("customEventFilter")
        self._parameter = trigger.get("parameter") or []
        self._parentFolderId = trigger.get("parentFolderId")
        self._continuousTimeMinMilliseconds = trigger.get(
            "continuousTimeMinMilliseconds"
        )
        self._selector = trigger.get("selector")
        self._triggerId = trigger.get("triggerId")
        self._tagManagerUrl = trigger.get("tagManagerUrl")
        self._fingerprint = trigger.get("fingerprint")
        self._visiblePercentageMax = trigger.get("visiblePercentageMax")
        self._name = trigger.get("name")
        self._visiblePercentageMin = trigger.get("visiblePercentageMin")
        self._type = trigger.get("type")
        self._notes = trigger.get("notes")
        self._interval = trigger.get("interval")
        self._filter = trigger.get("filter")
        self._autoEventFilter = trigger.get("autoEventFilter")
        self._limit = trigger.get("limit")
        self._checkValidation = trigger.get("checkValidation")

        self._path = path or "{}/triggers/{}".format(parent, self._triggerId)

        self._parameter = [
            gtm_manager.parameter.GTMParameter(x) for x in self._parameter
        ]

    @property
    def maxTimerLengthSeconds(self):
        """obj: Represents a Google Tag Manager Parameter. - Max time to fire Timer Events (in
        seconds). Only valid for AMP Timer trigger.
        """
        return self._maxTimerLengthSeconds

    @property
    def totalTimeMinMilliseconds(self):
        """obj:  Represents a Google Tag Manager Parameter. - A visibility trigger minimum total
        visible time (in milliseconds). Only valid for AMP Visibility trigger.
        """
        return self._totalTimeMinMilliseconds

    @property
    def uniqueTriggerId(self):
        """obj: Represents a Google Tag Manager Parameter. - Globally unique id of the trigger that
        auto-generates this (a Form Submit, Link Click or Timer listener) if any. Used to make
        incompatible auto-events work together with trigger filtering based on trigger ids. This
        value is populated during output generation since the tags implied by triggers don"t exist
        until then. Only valid for Form Submit, Link Click and Timer triggers.
        """
        return self._uniqueTriggerId

    @property
    def verticalScrollPercentageList(self):
        """obj: Represents a Google Tag Manager Parameter. - List of integer percentage values for
        scroll triggers. The trigger will fire when each percentage is reached when the view is
        scrolled vertically. Only valid for AMP scroll triggers.
        """
        return self._verticalScrollPercentageList

    @property
    def horizontalScrollPercentageList(self):
        """obj: Represents a Google Tag Manager Parameter. - List of integer percentage values for
        scroll triggers. The trigger will fire when each percentage is reached when the view is
        scrolled horizontally. Only valid for AMP scroll triggers.
        """
        return self._horizontalScrollPercentageList

    @property
    def containerId(self):
        """str: GTM Container ID.
        """
        return self._containerId

    @property
    def waitForTagsTimeout(self):
        """obj: Represents a Google Tag Manager Parameter. - How long to wait (in milliseconds) for
        tags to fire when "waits_for_tags" above evaluates to true. Only valid for Form Submission
        and Link Click triggers.
        """
        return self._waitForTagsTimeout

    @property
    def accountId(self):
        """str: GTM Account ID.
        """
        return self._accountId

    @property
    def waitForTags(self):
        """str: Represents a Google Tag Manager Parameter. - Whether or not we should delay the form
        submissions or link opening until all of the tags have fired (by preventing the default
        action and later simulating the default action). Only valid for Form Submission and Link
        Click triggers.
        """
        return self._waitForTags

    @property
    def intervalSeconds(self):
        """obj: Represents a Google Tag Manager Parameter. - Time between Timer Events to fire (in
        seconds). Only valid for AMP Timer trigger.
        """
        return self._intervalSeconds

    @property
    def eventName(self):
        """obj: Represents a Google Tag Manager Parameter. - Name of the GTM event that is fired.
        Only valid for Timer triggers.
        """
        return self._eventName

    @property
    def visibilitySelector(self):
        """obj: Represents a Google Tag Manager Parameter. - A visibility trigger CSS selector (i.e.
        "-id"). Only valid for AMP Visibility trigger.
        """
        return self._visibilitySelector

    @property
    def workspaceId(self):
        """str: GTM Workspace ID.
        """
        return self._workspaceId

    @property
    def customEventFilter(self):
        """list: Used in the case of custom event, which is fired iff all Conditions are true.
        """
        return self._customEventFilter

    @property
    def parameter(self):
        """list: Additional parameters.
        """
        return self._parameter

    @property
    def parentFolderId(self):
        """str: Parent folder id.
        """
        return self._parentFolderId

    @property
    def continuousTimeMinMilliseconds(self):
        """obj: Represents a Google Tag Manager Parameter. - A visibility trigger minimum continuous
        visible time (in milliseconds). Only valid for AMP Visibility trigger.
        """
        return self._continuousTimeMinMilliseconds

    @property
    def selector(self):
        """obj: Represents a Google Tag Manager Parameter. - A click trigger CSS selector (i.e. "a",
        "button" etc.). Only valid for AMP Click trigger.
        """
        return self._selector

    @property
    def triggerId(self):
        """str: The Trigger ID uniquely identifies the GTM Trigger.
        """
        return self._triggerId

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Trigger as computed at storage time. This value is
        recomputed whenever the trigger is modified.
        """
        return self._fingerprint

    @property
    def visiblePercentageMax(self):
        """obj: Represents a Google Tag Manager Parameter. - A visibility trigger maximum percent
        visibility. Only valid for AMP Visibility trigger.
        """
        return self._visiblePercentageMax

    @property
    def path(self):
        """str: GTM Trigger"s API relative path.
        """
        return self._path

    @property
    def name(self):
        """str: Trigger display name.
        """
        return self._name

    @property
    def visiblePercentageMin(self):
        """obj: Represents a Google Tag Manager Parameter. - A visibility trigger minimum percent
        visibility. Only valid for AMP Visibility trigger.
        """
        return self._visiblePercentageMin

    @property
    def type(self):
        """str: Defines the data layer event that causes this trigger.
        """
        return self._type

    @property
    def notes(self):
        """str: User notes on how to apply this trigger in the container.
        """
        return self._notes

    @property
    def interval(self):
        """obj: Represents a Google Tag Manager Parameter. - Time between triggering recurring Timer
        Events (in milliseconds). Only valid for Timer triggers.
        """
        return self._interval

    @property
    def filter(self):
        """list: The trigger will only fire iff all Conditions are true.
        """
        return self._filter

    @property
    def autoEventFilter(self):
        """list: Used in the case of auto event tracking.
        """
        return self._autoEventFilter

    @property
    def limit(self):
        """obj: Represents a Google Tag Manager Parameter. - Limit of the number of GTM events this
        Timer Trigger will fire. If no limit is set, we will continue to fire GTM events until the
        user leaves the page. Only valid for Timer triggers.
        """
        return self._limit

    @property
    def checkValidation(self):
        """obj: Represents a Google Tag Manager Parameter. - Whether or not we should only fire tags
         if the form submit or link click event is not cancelled by some other event handler (e.g.
         because of validation). Only valid for Form Submission and Link Click triggers.
        """
        return self._checkValidation

    def update(self, refresh=False, parameter=None, **kwargs):
        """Update the current trigger. The GTM API does not support a partial update. Therfore, this
        method will send all fields expliztily set in the method arguments and those cached in the 
        instance properties.

        GTMParameters passed in a list as the :code:`parameter` argument, will be merged recursivly
        with the exsisting parameters based on their parameter key.

        All other API resource properties can be overwritten by specifying the property name as
        keyword arguments on the method call. 

        Args:
            refresh (bool): Force a refresh of the entire GTMTrigger instance to prevent implicitly
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
            "maxTimerLengthSeconds": self._maxTimerLengthSeconds,
            "totalTimeMinMilliseconds": self._totalTimeMinMilliseconds,
            "uniqueTriggerId": self._uniqueTriggerId,
            "verticalScrollPercentageList": self._verticalScrollPercentageList,
            "horizontalScrollPercentageList": self._horizontalScrollPercentageList,
            "containerId": self._containerId,
            "waitForTagsTimeout": self._waitForTagsTimeout,
            "accountId": self._accountId,
            "waitForTags": self._waitForTags,
            "intervalSeconds": self._intervalSeconds,
            "eventName": self._eventName,
            "visibilitySelector": self._visibilitySelector,
            "workspaceId": self._workspaceId,
            "customEventFilter": self._customEventFilter,
            "parentFolderId": self._parentFolderId,
            "continuousTimeMinMilliseconds": self._continuousTimeMinMilliseconds,
            "selector": self._selector,
            "triggerId": self._triggerId,
            "tagManagerUrl": self._tagManagerUrl,
            "fingerprint": self._fingerprint,
            "visiblePercentageMax": self._visiblePercentageMax,
            "path": self._path,
            "name": self._name,
            "visiblePercentageMin": self._visiblePercentageMin,
            "type": self._type,
            "notes": self._notes,
            "interval": self._interval,
            "filter": self._filter,
            "autoEventFilter": self._autoEventFilter,
            "limit": self._limit,
            "checkValidation": self._checkValidation,
        }
        update_asset = {**default_asset, **kwargs}

        if parameter:
            parameter_dict = {**param_dict(self._parameter), **param_dict(parameter)}
            parameter = list(parameter_dict.values())
        else:
            parameter = self._parameter

        update_asset["parameter"] = [x.to_obj() for x in parameter]

        update_asset = {k: v for k, v in update_asset.items() if v is not None}

        request = self.triggers_service.update(path=self.path, body=update_asset)
        response = request.execute()
        self.__init__(trigger=response, service=self.service)

    def _get_trigger(self, path):
        """_get_trigger"""
        request = self.triggers_service.get(path=path)
        response = request.execute()
        return response

    def delete(self):
        """Delete the current trigger.
        """
        request = self.triggers_service.delete(path=self._path)
        request.execute()
