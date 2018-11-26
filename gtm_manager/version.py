"""version"""
import gtm_manager
import gtm_manager.container


class GTMVersion(gtm_manager.base.GTMBase):
    """Open a specific GTM Version.

    Args:
        version (dict): An API representation of the GTM Forlder. If provided, the resource will be
            not be loaded from the API. :code:`version` or :code:`path` argument must be set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/containers/1234/version/123". If provided instead of
            :code:`version`, the representation will be loaded from the API. :code:`path` or
            :code:`version` argument must be set.
        parent (str): Required, when the instance is initialized with a :code:`version` argument to
            explizitly set the parent path, i.e. "accounts/1234/containers/1234/workspaces/1234"
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, version=None, path=None, workspaceId=None, **kwargs):
        super().__init__(**kwargs)

        self.versions_service = (
            self.service.accounts().containers().versions
        )  # pylint: disable=E1101

        if version:
            pass
        elif path:
            version = self._get_version(path)
        else:
            raise ValueError("Please pass either a version obj or version path.")

        self._container = gtm_manager.container.GTMContainer(
            container=version.get("container"), service=self.service
        )
        self._containerId = version.get("containerId")
        self._zone = version.get("zone")
        self._deleted = version.get("deleted")
        self._trigger = version.get("trigger") or []
        self._description = version.get("description")
        self._builtInVariable = version.get("builtInVariable")
        self._name = version.get("name")
        self._tag = version.get("tag") or []
        self._tagManagerUrl = version.get("tagManagerUrl")
        self._containerVersionId = version.get("containerVersionId")
        self._workspaceId = workspaceId
        self._fingerprint = version.get("fingerprint")
        self._variable = version.get("variable") or []
        self._path = version.get("path")
        self._folder = version.get("folder") or []
        self._accountId = version.get("accountId")

        workspace_path = (
            "accounts/{}/containers/{}/workspaces/{}".format(
                self._accountId, self._containerId, self._workspaceId
            )
            if workspaceId
            else None
        )

        self._tag = [
            gtm_manager.tag.GTMTag(tag=x, parent=workspace_path, service=self.service)
            for x in self._tag
        ]
        self._trigger = [
            gtm_manager.trigger.GTMTrigger(
                trigger=x, parent=workspace_path, service=self.service
            )
            for x in self._trigger
        ]
        self._variable = [
            gtm_manager.variable.GTMVariable(
                variable=x, parent=workspace_path, service=self.service
            )
            for x in self._variable
        ]
        self._folder = [
            gtm_manager.folder.GTMFolder(
                folder=x, parent=workspace_path, service=self.service
            )
            for x in self._folder
        ]

        self.raw_body = version

    @property
    def container(self):
        """:class:`gtm_manager.container.GTMContainer`: The container that this version was taken
        from.
        """
        return self._container

    @property
    def containerId(self):
        """str: GTM Container ID.
        """
        return self._containerId

    @property
    def zone(self):
        """list: The zones in the container that this version was taken from.
        """
        return self._zone

    @property
    def deleted(self):
        """bool: A value of true indicates this container version has been deleted.
        """
        return self._deleted

    @property
    def trigger(self):
        """list: The triggers in the container that this version was taken from.
        """
        return self._trigger

    @property
    def description(self):
        """str: Container version description.
        """
        return self._description

    @property
    def builtInVariable(self):
        """list: The built-in variables in the container that this version was taken from.
        """
        return self._builtInVariable

    @property
    def name(self):
        """str: Container version display name.
        """
        return self._name

    @property
    def tag(self):
        """list: The tags in the container that this version was taken from.
        """
        return self._tag

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def containerVersionId(self):
        """str: The Container Version ID uniquely identifies the GTM Container Version.
        """
        return self._containerVersionId

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Container Version as computed at storage
        time. This value is recomputed whenever the container version is modified.
        """
        return self._fingerprint

    @property
    def variable(self):
        """list: The variables in the container that this version was taken from.
        """
        return self._variable

    @property
    def path(self):
        """str: GTM ContainerVersions's API relative path.
        """
        return self._path

    @property
    def folder(self):
        """list: The folders in the container that this version was taken from.
        """
        return self._folder

    @property
    def accountId(self):
        """str: GTM Account ID.
        """
        return self._accountId

    def _get_version(self, path):
        """_get_version"""
        request = self.versions_service().get(path=path)
        response = request.execute()
        return response

    def publish(self):
        """publish"""
        request = self.versions_service().publish(path=self.path)
        response = request.execute()
        return response


class GTMVersionHeader(object):
    """GTMVersionHeader"""

    def __init__(self, versionHeader):
        self._path = versionHeader.get("path")
        self._accountId = versionHeader.get("accountId")
        self._containerId = versionHeader.get("containerId")
        self._containerVersionId = versionHeader.get("containerVersionId")
        self._name = versionHeader.get("name")
        self._numMacros = versionHeader.get("numMacros")
        self._numRules = versionHeader.get("numRules")
        self._numTags = versionHeader.get("numTags")
        self._numTriggers = versionHeader.get("numTriggers")
        self._deleted = versionHeader.get("deleted")
        self._numVariables = versionHeader.get("numVariables")
        self._numZones = versionHeader.get("numZones")

        self.raw_body = versionHeader
