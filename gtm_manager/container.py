"""container.py"""
from googleapiclient.errors import HttpError

import gtm_manager.base
import gtm_manager.workspace
import gtm_manager.version

from gtm_manager import NO_LIVE_VERSION_ERROR


class GTMContainer(gtm_manager.base.GTMBase):
    """Open a specific GTM Container.

    Args:
        container (dict): An API representation of the GTM Container. If provided, the
            container will be not be loaded from the API. `container` or `path` argument must be
            set.
        path (str): The API path to the resource, i.e "accounts/1234/containers/1234". If
            provided instead of `container`, the api representation will be loaded from the API.
            `path` or `container` argument must be set.
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, container=None, path=None, **kwargs):

        super().__init__(**kwargs)

        self.containers_service = (
            self.service.accounts().containers()
        )  # pylint: disable=E1101

        if container:
            pass
        elif path:
            container = self._get_container(path)
        else:
            raise ValueError("Please pass either a container obj or container path.")

        self._publicId = container.get("publicId")
        self._containerId = container.get("containerId")
        self._domainName = container.get("domainName", [""])
        self._notes = container.get("notes", "")
        self._tagManagerUrl = container.get("tagManagerUrl")
        self._usageContext = container.get("usageContext")
        self._fingerprint = container.get("fingerprint")
        self._path = container.get("path")
        self._accountId = container.get("accountId")
        self._name = container.get("name")

        self._workspaces = []
        self._version_headers = []
        self._live_version = None
        self._raw_body = container

        self.workspaces = None

    def __repr__(self):
        return "{} {}".format(self.path, self.name)

    @property
    def publicId(self):
        """str: Container Public ID. Also known as the GTM-ID.
        """
        return self._publicId

    @property
    def containerId(self):
        """str: The Container ID uniquely identifies the GTM Container.
        """
        return self._containerId

    @property
    def domainName(self):
        """List[str]: List of domain names associated with the Container.
        """
        return self._domainName

    @property
    def notes(self):
        """str: Container Notes
        """
        return self._notes

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def usageContext(self):
        """List[str]: List of Usage Contexts for the Container.
        Valid values include: web, android, or ios.
        """
        return self._usageContext

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Container as computed
        at storage time. This value is recomputed whenever the account is modified.
        """
        return self._fingerprint

    @property
    def path(self):
        """str: GTM Container's API relative path.
        """
        return self._path

    @property
    def accountId(self):
        """str: GTM Account ID
        """
        return self._accountId

    @property
    def name(self):
        """str: Container display name
        """
        return self._name

    @property
    def raw_body(self):
        """obj: Container raw body
        """
        return self._raw_body

    def live_version(self, refresh=True):
        """Load from API and open the published GTM Version of the current container.

        Args:
            refresh (bool): If live_version has already been loaded from the API, force another API
                request to get the latest live_version.

        Returns:
            An instance of :class:`gtm_manager.version.GTMVersion` or `None` if the GTM Container
            has no published live version.

        """
        if refresh or not self._live_version:
            self._refresh_live_version()

        return self._live_version

    def create_workspace(self, name, description=""):
        """Create a new GTM Workspace in the current GTM Container.

        Args:
            name (str): Workspace display name
            description (str): Workspace description

        Returns:
            A new instance of the created :class:`gtm_manager.workspace.GTMWorkspace`.
        """
        body = {"description": description, "name": name}
        request = self.containers_service.workspaces().create(
            parent=self.path, body=body
        )
        response = request.execute()
        return gtm_manager.workspace.GTMWorkspace(
            workspace=response, service=self.service
        )

    def _get_container(self, path):
        """_get_container"""
        request = self.containers_service.get(path=path)
        response = request.execute()
        return response

    def _refresh_live_version(self):
        """_refresh_live_version"""
        try:
            request = self.containers_service.versions().live(parent=self.path)
            response = request.execute()
            self._live_version = gtm_manager.version.GTMVersion(
                version=response, service=self.service
            )
        except HttpError as error:
            if NO_LIVE_VERSION_ERROR in str(error):
                self._live_version = None
            else:
                raise error

    def list_workspaces(self, refresh=True):
        """Load from API and list all GTM Workspaces in this account.

        Args:
            refresh (bool): If workspaces have already been loaded from the API, force another API
                request to get the latest list of workspaces.

        Returns:
            A list of :class:`gtm_manager.workspace.GTMWorkspace`.
        """
        if not self._workspaces or refresh:
            request = self.containers_service.workspaces().list(parent=self.path)
            response = request.execute()
            self._workspaces = [
                gtm_manager.workspace.GTMWorkspace(workspace=x, service=self.service)
                for x in response.get("workspace")
            ]
        return self._workspaces

    def list_version_headers(self, refresh=True):
        """Load from API and list all GTM Version Headers in this account.

        Args:
            refresh (bool): If version_headers have already been loaded from the API, force another
                API request to get the latest list of version_headers.

        Returns:
            A list of :class:`gtm_manager.version.GTMVersionHeader`.
        """
        if not self._version_headers or refresh:
            request = (
                self.service.accounts()
                .containers()
                .version_headers()
                .list(parent=self.path)
            )
            response = request.execute()
            self._version_headers = [
                gtm_manager.version.GTMVersionHeader(versionHeader=x)
                for x in response.get("containerVersionHeader")
            ]
        return self._version_headers
