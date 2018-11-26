"""folder.py"""

import gtm_manager.base


class GTMFolder(gtm_manager.base.GTMBase):
    """Open a specific GTM Folder.

    Args:
        folder (dict): An API representation of the GTM Folder. If provided, the resource will be not be
            loaded from the API. :code:`folder` or :code:`path` argument must be set.
        path (str): The API path to the resource, i.e.
            "accounts/1234/containers/1234/workspaces/1234/folders/123". If provided instead of
            :code:`folder`, the representation will be loaded from the API. :code:`path` or
            :code:`folder` argument must be set.
        parent (str): Required, when the instance is initialized with a :code:`folder` argument to
            explizitly set the parent path, i.e. "accounts/1234/containers/1234/workspaces/1234"
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, folder=None, path=None, parent=None, **kwargs):
        super().__init__(**kwargs)

        self.folders_service = (
            self.service.accounts().containers().workspaces().folders()
        )  # pylint: disable=E1101

        if folder:
            pass
        elif path:
            folder = self._get_folder(path)
        else:
            raise ValueError("Please pass either a folder obj or folder path.")

        self._containerId = folder.get("containerId")
        self._notes = folder.get("notes", "")
        self._workspaceId = folder.get("workspaceId")
        self._tagManagerUrl = folder.get("tagManagerUrl")
        self._fingerprint = folder.get("fingerprint")
        self._folderId = folder.get("folderId")
        self._accountId = folder.get("accountId")
        self._name = folder.get("name")
        self._path = path or "{}/folders/{}".format(parent, self.folderId)

    @property
    def containerId(self):
        """str: The container that this version was taken from.
        """
        return self._containerId

    @property
    def notes(self):
        """str: The container that this version was taken from.
        """
        return self._notes

    @property
    def workspaceId(self):
        """str: The container that this version was taken from.
        """
        return self._workspaceId

    @property
    def tagManagerUrl(self):
        """str: The container that this version was taken from.
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The container that this version was taken from.
        """
        return self._fingerprint

    @property
    def folderId(self):
        """str: The container that this version was taken from.
        """
        return self._folderId

    @property
    def accountId(self):
        """str: The container that this version was taken from.
        """
        return self._accountId

    @property
    def name(self):
        """str: The container that this version was taken from.
        """
        return self._name

    @property
    def path(self):
        """str: The container that this version was taken from.
        """
        return self._path

    def _get_folder(self, path):
        """_get_container"""
        request = self.folders_service.get(path=path)
        response = request.execute()
        return response

    def delete(self):
        """Delete the current folder.
        """
        request = self.folders_service.delete(path=self._path)
        request.execute()
