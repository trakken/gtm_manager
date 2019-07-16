"""base.py"""
from googleapiclient import discovery

from gtm_manager.utils_auth import build_http

from gtm_manager import SERVICE_NAME, SERVICE_VERSION


class GTMBase(object):
    """GTMBase"""

    def __init__(self, service=None):
        if service:
            self.service = service
        else:
            self.service = discovery.build(
                SERVICE_NAME, SERVICE_VERSION, http=build_http(), cache_discovery=False
            )
