"""gtm workspace.py"""
import gtm_manager.base
import gtm_manager.version
import gtm_manager.tag
import gtm_manager.trigger
import gtm_manager.variable
import gtm_manager.folder
import gtm_manager.built_in_variable
from gtm_manager.exceptions import TagNotFound, TriggerNotFound, VariableNotFound


class GTMWorkspace(gtm_manager.base.GTMBase):
    """Open a specific GTM Workspace.

    Args:
        workspace (dict): An API representation of the GTM Workspace. If provided, the
            resource will be not be loaded from the API. `workspace` or `path` argument must be
            set.
        path (str): The API path to the resource, i.e
            "accounts/1234/containers/1234/workspaces/1234". If provided instead of `workspace`,
            the representation will be loaded from the API. `path` or `workspace` argument must be
            set.
        **kwargs: Additional keyword args to initialize the base class.
    """

    def __init__(self, workspace=None, path=None, **kwargs):
        super().__init__(**kwargs)

        self.workspaces_service = self.service.accounts().containers().workspaces()

        if workspace:
            pass
        elif path:
            workspace = self._get_workspace(path)
        else:
            raise ValueError(
                "Please pass either a workspace API representation or workspace path."
            )

        self._description = workspace.get("description")
        self._name = workspace.get("name")
        self._workspaceId = workspace.get("workspaceId")
        self._tagManagerUrl = workspace.get("tagManagerUrl")
        self._fingerprint = workspace.get("fingerprint")
        self._path = workspace.get("path")
        self._accountId = workspace.get("accountId")
        self._containerId = workspace.get("containerId")
        self._tags = []
        self._triggers = []
        self._variables = []
        self._folders = []
        self._built_in_variables = []
        self._quick_preview = None

    def __repr__(self):
        return "<GTM Workspace: {}>".format(self.name)

    @property
    def description(self):
        """str: Workspace description.
        """
        return self._description

    @property
    def name(self):
        """str: Workspace display name.
        """
        return self._name

    @property
    def workspaceId(self):
        """str: The Workspace ID uniquely identifies the GTM Workspace.
        """
        return self._workspaceId

    @property
    def tagManagerUrl(self):
        """str: Auto generated link to the tag manager UI
        """
        return self._tagManagerUrl

    @property
    def fingerprint(self):
        """str: The fingerprint of the GTM Workspace as computed at storage time.
        This value is recomputed whenever the workspace is modified.
        """
        return self._fingerprint

    @property
    def path(self):
        """str: GTM Workspace's API relative path.
        """
        return self._path

    @property
    def accountId(self):
        """str: GTM Account ID.
        """
        return self._accountId

    @property
    def containerId(self):
        """str: GTM Container ID.
        """
        return self._containerId

    def quick_preview(self, refresh=True):
        """Get a quick_preview of the current workspace state from the API.

        Args:
            Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            An instance of :class:`gtm_manager.version.GTMVersion`
        """
        if refresh or not self._quick_preview:
            self._refresh_quick_preview()

        return self._quick_preview

    def delete(self):
        """Delete the current workspace.
        """
        request = self.workspaces_service.delete(path=self.path)
        request.execute()

    def clear_all_assets(self, refresh=True):
        """Clear all assets from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        """
        if refresh or not self._quick_preview:
            self._refresh_quick_preview()

        if self._quick_preview.tag:
            for tag in self._quick_preview.tag:
                tag.delete()

        if self._quick_preview.trigger:
            for trigger in self._quick_preview.trigger:
                trigger.delete()

        for _ in range(10):
            if self._quick_preview.variable:
                for variable in reversed(self._quick_preview.variable):
                    variable.delete()
                self._refresh_quick_preview()
            else:
                break

        if self._quick_preview.folder:
            for folder in self._quick_preview.folder:
                folder.delete()

    def trigger_map(self, refresh=True):
        """Create a trigger map from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A dict having all triggerNames and triggerIds as strings keys with their corresponding
            triggerIds and triggerNames as string values. The *All Pages* trigger will always be
            added as default. For example::

                {
                    "2147479553": "All Pages",
                    "All Pages": "2147479553",
                    "Click - My Button": "1",
                    "1": "Click - My Button",
                }
        """
        if refresh or not self._quick_preview:
            self._refresh_quick_preview()

        trigger_map = {"2147479553": "All Pages", "All Pages": "2147479553"}

        if not self._quick_preview.trigger:
            return trigger_map

        for trigger in self._quick_preview.trigger:
            trigger_map[trigger.name] = trigger.triggerId
            trigger_map[trigger.triggerId] = trigger.name

        return trigger_map

    def folder_map(self, refresh=True):
        """Create a folder map from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A dict having all folderNames and folderIds as strings keys with their corresponding
            folderIds and folderName as string values. For example::

                {
                    "My Folder": "1",
                    "My Other Folder": "2",
                    "1":"My Folder",
                    "2": "My Other Folder",
                }
        """
        if refresh or not self._quick_preview:
            self._refresh_quick_preview()

        folder_map = {}

        if not self._quick_preview.folder:
            return folder_map

        for folder in self._quick_preview.folder:
            folder_map[folder.name] = folder.folderId
            folder_map[folder.folderId] = folder.name

        return folder_map

    def disable_built_ins(self, built_in_type):
        """Disable built-ins in the current workspace.

        Args:
            built_in_type (list of str): A list of the built in types as strings the call should
                disable.
        """
        self.workspaces_service.built_in_variables().delete(
            path=self.path, type=built_in_type
        )

    def create_tag(self, asset_body):
        """Create a tag in the current workspace.

        Args:
            asset_body (dict): An API representation of a GTM Tag. See the API documentation for
                all writable fields of the asset_body: https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/tags

        Returns:
            An instance of :class:`gtm_manager.tag.GTMTag`
        """
        request = self.workspaces_service.tags().create(
            parent=self.path, body=asset_body
        )
        return gtm_manager.tag.GTMTag(
            tag=request.execute(), parent=self.path, service=self.service
        )

    def create_trigger(self, asset_body):
        """Create a trigger in the current workspace.

        Args:
            asset_body (dict): An API representation of a GTM Trigger. See the API documentation for
                all writable fields of the asset_body: https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/triggers

        Returns:
            An instance of :class:`gtm_manager.trigger.GTMTrigger`
        """
        request = self.workspaces_service.triggers().create(
            parent=self.path, body=asset_body
        )
        return gtm_manager.trigger.GTMTrigger(
            trigger=request.execute(), parent=self.path, service=self.service
        )

    def create_variable(self, asset_body):
        """Create a variable in the current workspace.

        Args:
            asset_body (dict): An API representation of a GTM Variable. See the API documentation
                for all writable fields of the asset_body: https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/variables

        Returns:
            An instance of :class:`gtm_manager.variable.GTMVariable`
        """
        request = self.workspaces_service.variables().create(
            parent=self.path, body=asset_body
        )
        return gtm_manager.variable.GTMVariable(
            variable=request.execute(), parent=self.path, service=self.service
        )

    def create_folder(self, name, notes=""):
        """Create a folder in the current workspace.

        Args:
            asset_body (dict): An API representation of a GTM Folder. See the API documentation for
                all writable fields of the asset_body: https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/folders

        Returns:
            An instance of :class:`gtm_manager.folder.GTMFolder`
        """
        request = self.workspaces_service.folders().create(
            parent=self.path, body={"name": name, "notes": notes}
        )
        return gtm_manager.folder.GTMFolder(
            folder=request.execute(), parent=self.path, service=self.service
        )

    def create_build_ins(self, asset_body):
        """Create built-ins in the current workspace.

        Args:
            built_in_type (list of str): A list of the built in types as strings the call should
                enable. See the API documentation for possibles types: https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/workspaces/built_in_variables
        """
        request = self.workspaces_service.built_in_variables().create(
            parent=self.path, type=asset_body
        )
        response = request.execute()
        return [
            gtm_manager.built_in_variable.GTMBuiltInVariable(x)
            for x in response.get("builtInVariable") or []
        ]

    def list_tags(self, refresh=False):
        """List all tags from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A list of :class:`gtm_manager.tag.GTMTag`.
        """
        if self._tags is None or refresh:
            request = self.workspaces_service.tags().list(parent=self.path)

            response = request.execute()
            self._tags = [
                gtm_manager.tag.GTMTag(tag=x, service=self.service, parent=self.path)
                for x in response.get("tag") or []
            ]
        return self._tags

    def list_triggers(self, refresh=False):
        """List all triggers from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A list of :class:`gtm_manager.triggers.GTMTrigger`.
        """
        if self._triggers is None or refresh:
            request = self.workspaces_service.triggers().list(parent=self.path)

            response = request.execute()
            self._triggers = [
                gtm_manager.trigger.GTMTrigger(
                    trigger=x, service=self.service, parent=self.path
                )
                for x in response.get("trigger") or []
            ]
        return self._triggers

    def list_variables(self, refresh=False):
        """List all variables from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A list of :class:`gtm_manager.variable.GTMVariable`.
        """
        if self._variables is None or refresh:
            request = self.workspaces_service.variables().list(parent=self.path)

            response = request.execute()
            self._variables = [
                gtm_manager.variable.GTMVariable(
                    variable=x, service=self.service, parent=self.path
                )
                for x in response.get("variable") or []
            ]
        return self._variables

    def list_folders(self, refresh=False):
        """List all folders from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A list of :class:`gtm_manager.folder.GTMFolder`.
        """

        if self._folders is None or refresh:
            request = self.workspaces_service.folders().list(parent=self.path)

            response = request.execute()
            self._folders = [
                gtm_manager.folder.GTMFolder(
                    folder=x, service=self.service, parent=self.path
                )
                for x in response.get("folder") or []
            ]
        return self._folders

    def list_built_in_variables(self, refresh=False):
        """List all built in variables from the current workspace.

        Args:
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            A list of :class:`gtm_manager.built_in_variable.GTMBuiltInVariable`.
        """

        if self._built_in_variables is None or refresh:
            request = self.workspaces_service.built_in_variables().list(
                parent=self.path
            )

            response = request.execute()
            self._built_in_variables = [
                gtm_manager.built_in_variable.GTMBuiltInVariable(built_in_variable=x)
                for x in response.get("builtInVariable") or []
            ]
        return self._built_in_variables

    def get_tag_by_name(self, tag_name, refresh=False):
        """Get a GTM Tag from the GTM Workspace by its name.

        Args:
            tag_name (str): The exact name to look for in the GTM Workspace.
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            An instance of :class:`gtm_manager.tag.GTMTag`.

        Raises:
            :class:`gtm_manager.exceptions.TagNotFound`
        """
        tags = self.list_tags(refresh=refresh)

        for tag in tags:
            if tag.name == tag_name:
                return tag

        raise TagNotFound(tag_name, self.path)

    def get_trigger_by_name(self, trigger_name, refresh=False):
        """Get a GTM Trigger from the GTM Workspace by its name.

        Args:
            trigger_name (str): The exact name to look for in the GTM Workspace.
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            An instance of :class:`gtm_manager.trigger.GTMTrigger`.

        Raises:
            :class:`gtm_manager.exceptions.TriggerNotFound`
        """
        triggers = self.list_triggers(refresh=refresh)

        for trigger in triggers:
            if trigger.name == trigger_name:
                return trigger

        raise TriggerNotFound(trigger_name, self.path)

    def get_variable_by_name(self, variable_name, refresh=False):
        """Get a GTM Variable from the GTM Workspace by its name.

        Args:
            variable_name (str): The exact name to look for in the GTM Workspace.
            refresh (bool): If quick_preview has already been loaded from the API, force another API
                request to get the latest quick_preview.

        Returns:
            An instance of :class:`gtm_manager.variable.GTMVariable`.

        Raises:
            :class:`gtm_manager.exceptions.VariableNotFound`
        """
        variables = self.list_variables(refresh=refresh)

        for variable in variables:
            if variable.name == variable_name:
                return variable

        raise VariableNotFound(variable_name, self.path)

    def create_version(self, name, notes=""):
        """Create a new version from the current state of the workspace.

        @TODO: add descroption for sync or publishing errors

        Args:
            name (str): The GTM Version display name
            notes (str); The GTM Version notes

        Returns:
            An instance of :class:`gtm_manager.version.GTMVersion`.
        """
        request = self.workspaces_service.create_version(
            path=self.path, body={"name": name, "notes": notes}
        )
        response = request.execute()

        version = gtm_manager.version.GTMVersion(
            version=response.get("containerVersion"), service=self.service
        )

        if version.containerVersionId == "0":
            raise Exception(
                "Could not create version from workspace. Please visit {} for details".format(
                    self.tagManagerUrl
                )
            )

        return version

    def _get_workspace(self, path):
        """_get_workspace"""
        request = self.workspaces_service.get(path=path)
        response = request.execute()
        return response

    def _refresh_quick_preview(self):
        """_refresh_quick_preview"""
        request = self.workspaces_service.quick_preview(path=self.path)
        response = request.execute()
        self._quick_preview = gtm_manager.version.GTMVersion(
            version=response.get("containerVersion"),
            workspaceId=self.workspaceId,
            service=self.service,
        )
        return self._quick_preview

    def get_status(self):
        """Get the status with all workspace changes.

        @TODO: Add examples

        Returns:
            A list with all workspace changes.
        """
        request = self.workspaces_service.getStatus(path=self.path)
        return request.execute()

    def sync(self):
        """Synchronize the workspace to the latest GTM Version.

        Returns:
            @TODO: What is returned?
        """
        request = self.workspaces_service.sync(path=self.path)
        sync_resp = request.execute()

        mergeConflicts = []

        for conflict in sync_resp["mergeConflict"]:

            if conflict["entityInWorkspace"]["variable"]:
                conflict["entityInWorkspace"][
                    "variable"
                ] = gtm_manager.variable.GTMVariable(
                    variable=conflict["entityInWorkspace"]["variable"]
                )

            if conflict["entityInWorkspace"]["trigger"]:
                conflict["entityInWorkspace"][
                    "trigger"
                ] = gtm_manager.trigger.GTMTrigger(
                    trigger=conflict["entityInWorkspace"]["trigger"]
                )

            if conflict["entityInWorkspace"]["tag"]:
                conflict["entityInWorkspace"]["tag"] = gtm_manager.tag.GTMTag(
                    tag=conflict["entityInWorkspace"]["tag"]
                )

            if conflict["entityInWorkspace"]["folder"]:
                conflict["entityInWorkspace"]["folder"] = gtm_manager.folder.GTMFolder(
                    folder=conflict["entityInWorkspace"]["folder"]
                )

            if conflict["entityInBaseVersion"]["variable"]:
                conflict["entityInBaseVersion"][
                    "variable"
                ] = gtm_manager.variable.GTMVariable(
                    variable=conflict["entityInBaseVersion"]["variable"]
                )

            if conflict["entityInBaseVersion"]["trigger"]:
                conflict["entityInBaseVersion"][
                    "trigger"
                ] = gtm_manager.trigger.GTMTrigger(
                    trigger=conflict["entityInBaseVersion"]["trigger"]
                )

            if conflict["entityInBaseVersion"]["tag"]:
                conflict["entityInBaseVersion"]["tag"] = gtm_manager.tag.GTMTag(
                    tag=conflict["entityInBaseVersion"]["tag"]
                )

            if conflict["entityInBaseVersion"]["folder"]:
                conflict["entityInBaseVersion"][
                    "folder"
                ] = gtm_manager.folder.GTMFolder(
                    folder=conflict["entityInBaseVersion"]["folder"]
                )

            mergeConflicts.append(conflict)

        sync_resp["mergeConflict"] = mergeConflicts
