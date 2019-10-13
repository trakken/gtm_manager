"""built_in_variable.py"""


class GTMBuiltInVariable(object):
    """Open a specifc GTM Built In Variable

    Args:
        - built_in_variable (dict): An API representation of the GTM Built In Variable.
    """

    def __init__(self, built_in_variable):
        self._path = built_in_variable.get("path")
        self._accountId = built_in_variable.get("accountId")
        self._containerId = built_in_variable.get("containerId")
        self._workspaceId = built_in_variable.get("workspaceId")
        self._type = built_in_variable.get("type")
        self._name = built_in_variable.get("name")

    @property
    def path(self):
        """str: GTM BuiltInVariable's API relative path.
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

    @property
    def workspaceId(self):
        """str: GTM Workspace ID.
        """
        return self._workspaceId

    @property
    def name(self):
        """str: Name of the built-in variable to be used to refer to the built-in variable.
        """
        return self._name

    @property
    def type(self):
        """str: Type of built-in variable.
        """
        return self._type
