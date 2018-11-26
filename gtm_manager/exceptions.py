"""excpetions.py"""


class GTMManagerException(Exception):
    """GTMManagerException"""

    pass


class AuthError(GTMManagerException):
    pass


class VariableNotFound(GTMManagerException):
    """VariableNotFound"""

    def __init__(self, variable_name, parent):
        super(VariableNotFound, self).__init__()
        self.variable_name = variable_name
        self.parent = parent

    def __str__(self):
        return "Variable {!r} not found in parent {!r}".format(
            self.variable_name, self.parent
        )


class TagNotFound(GTMManagerException):
    """TagNotFound"""

    def __init__(self, tag_name, parent):
        super(TagNotFound, self).__init__()
        self.tag_name = tag_name
        self.parent = parent

    def __str__(self):
        return "Tag {!r} not found in parent {!r}".format(self.tag_name, self.parent)


class TriggerNotFound(GTMManagerException):
    """TriggerNotFound"""

    def __init__(self, trigger_name, parent):
        super(TriggerNotFound, self).__init__()
        self.trigger_name = trigger_name
        self.parent = parent

    def __str__(self):
        return "Trigger {!r} not found in parent {!r}".format(
            self.trigger_name, self.parent
        )


class RateLimitExceeded(GTMManagerException):
    """RateLimitExceeded"""

    pass
