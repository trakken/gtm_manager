"""parameter.py"""
import copy


class GTMParameter(object):
    """GTMParameter"""

    def __init__(self, parameter):
        self.map = parameter.get("map")
        self.list = parameter.get("list")
        self.value = parameter.get("value")
        self.key = parameter.get("key")
        self.type = parameter.get("type")

        if self.list:
            self.list = [GTMParameter(x) for x in self.list]

    def __repr__(self):
        return "<GTM Parameter: {}>".format(self.key)

    def to_obj(self):
        """to_obj"""
        if self.list:
            self.list = [x.to_obj() for x in self.list]
            # new_list = []
            # for item in self.list:
            #     if isinstance(item, GTMParameter):
            #         new_list.append(item.to_obj())
            #     else:
            #         new_list.append(item)
            # self.list = new_list
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def copy(self):
        """copy"""
        return copy.deepcopy(self)
