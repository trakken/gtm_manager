"""permission.py"""

import gtm_manager


class GTMPermission(gtm_manager.base.GTMBase):
    """Open a specific GTM Permission.

    Args:
        permission (dict): An API representation of the GTM Permission. If provided, the resource
            will be not be loaded from the API. :code:`permission` or :code:`path` argument must be
            set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/permissions/1234". If provided instead of :code:`permission`,
            the representation will be loaded from the API. :code:`path` or :code:`permission`
            argument must be set.
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, permission=None, path=None, **kwargs):
        super().__init__(**kwargs)

        self.permission_service = (
            self.service.accounts().user_permissions()
        )  # pylint: disable=E1101

        if permission:
            pass
        elif path:
            permission = self._get_permission(path)
        else:
            raise ValueError("Please pass either a permission obj or permission path.")

        self._containerAccess = [
            GTMContainerAccess(x) for x in permission.get("containerAccess")
        ]
        self._path = permission.get("path")
        self._accountAccess = permission.get("accountAccess")
        self._emailAddress = permission.get("emailAddress")
        self._accountId = permission.get("accountId")

    def __repr__(self):
        return "{} {}".format(self.path, self._emailAddress)

    @property
    def path(self):
        """str: GTM Permission's API relative path."""
        return self._path

    @property
    def accountAccess(self):
        """str: GTM Permission's API relative path."""
        return self._accountAccess

    @property
    def emailAddress(self):
        """str: GTM Permission's API relative path."""
        return self._emailAddress

    @property
    def accountId(self):
        """str: GTM Permission's API relative path."""
        return self._accountId

    def _get_permission(self, path):
        """_get_container"""
        request = self.permission_service.get(path=path)
        response = request.execute()
        return response


class GTMContainerAccess(object):
    """GTMContainerAccess"""

    def __init__(self, containerAccess):
        self.containerId = containerAccess.get("containerId")
        self.permission = containerAccess.get("permission")
