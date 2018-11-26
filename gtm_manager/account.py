"""account.py"""
import gtm_manager.base
import gtm_manager.container
import gtm_manager.permission


class GTMAccount(gtm_manager.base.GTMBase):
    """Open a specific GTM account.

    Args:
        account (dict): An account API representation of the GTM Account. If provided, the account
            will be not be loaded from the API. `account` or `path` argument
            must be set.
        path (str): The GTM API path to the account, i.e "accounts/1234". If provided instead of 
            `account`, the account representation will be loaded from the API. `path` or `account`
            argument must be set.
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, account=None, path=None, **kwargs):

        super().__init__(**kwargs)

        self.accounts_service = self.service.accounts()  # pylint: disable=E1101

        if account:
            pass
        elif path:
            account = self._get_account(path)
        else:
            raise ValueError("Please pass either an account obj or account path.")

        self._name = account.get("name")
        self._shareData = account.get("shareData", False)
        self._tagManagerUrl = account.get("tagManagerUrl")
        self._fingerprint = account.get("fingerprint")
        self._path = account.get("path")
        self._accountId = account.get("accountId")

        self._list_containers = None
        self._list_permissions = None

        self._raw_body = account

    @property
    def name(self):
        """str: Account display name
        """
        return self._name

    @property
    def shareData(self):
        """bool: Whether the account shares data anonymously with Google and others
        """
        return self._shareData

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Account as computed at
        storage time. This value is recomputed whenever the account is modified.
        """
        return self._fingerprint

    @property
    def path(self):
        """str: GTM Account's API relative path
        """
        return self._path

    @property
    def raw_body(self):
        """obj: The raw asset body as returend from the API
        """
        return self._raw_body

    @property
    def accountId(self):
        """str: The Account ID uniquely identifies the GTM Account
        """
        return self._accountId

    def list_containers(self, refresh=True):
        """Load from API and list all containers in this account.

        Args:
            refresh (bool): If containers have already been loaded in the API, force another API
                request to get the latest list of containers.

        Returns:
            A list of :class:`gtm_manager.permission.GTMContainer`.
        """
        if refresh or not self._list_containers:
            self._refresh_list_containers()

        return self._list_containers

    def list_permissions(self, refresh=True):
        """Load from API and list all permissions in this account.

        Args:
            refresh (bool): If permissions have already been loaded in the API, force another API
                request to get the latest list of permissions.

        Returns:
            A list of :class:`gtm_manager.permission.GTMPermission`.
        """
        if refresh or not self._list_permissions:
            self._refresh_list_permissions()

        return self._list_permissions

    def update(self, name, shareData):
        """Update the current accounts `name` and `shareData` parameters via the API.

        Args:
            name (str): Account display name
            shareData (bool): Share data setting
        """
        asset_body = {"name": name, "shareData": shareData}

        request = self.accounts_service.update(path=self.path, body=asset_body)
        response = request.execute()
        self.__init__(account=response, service=self.service)

    def create_container(self, name, usage_context="web", domain_name=None, notes=None):
        """Create a new container in the current account.

        Args:
            name (str): Container display name
            usage_context (str): Usage Contexts for the Container.
                Valid values include: web, android, or ios.
            domain_name (str): List of domain names associated with the Container.
            notes (str): Container notes
        """
        asset_body = {
            "name": name,
            "usageContext": [usage_context] if usage_context else ["web"],
        }

        if domain_name:
            asset_body["domainName"] = [domain_name]
        if notes:
            asset_body["notes"] = notes

        request = self.accounts_service.containers().create(
            parent=self.path, body=asset_body
        )
        response = request.execute()
        return gtm_manager.container.GTMContainer(
            container=response, service=self.service
        )

    def _get_account(self, path):
        """_get_container"""
        request = self.accounts_service.get(path=path)
        response = request.execute()
        return response

    def _refresh_list_containers(self):
        """_refresh_list_container"""
        request = self.accounts_service.containers().list(parent=self.path)
        response = request.execute()
        self._list_containers = [
            gtm_manager.container.GTMContainer(container=x, service=self.service)
            for x in response.get("container")
        ]

    def _refresh_list_permissions(self):
        """_refresh_list_permissions"""
        request = self.accounts_service.user_permissions().list(parent=self.path)
        response = request.execute()
        self._list_permissions = [
            gtm_manager.permission.GTMPermission(permission=x, service=self.service)
            for x in response.get("userPermission")
        ]
