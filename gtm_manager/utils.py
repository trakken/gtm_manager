"""utils.py"""


def param_dict(param_list):
    """param_dict"""
    dct = {}
    for param in param_list:
        dct[param.key] = param
    return dct
