"""manager.py"""
import logging
from googleapiclient import errors

import gtm_manager.account


class GTMManager(gtm_manager.base.GTMBase):
    """Authenticates a users base gtm access.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.accounts_service = self.service.accounts()  # pylint: disable=E1101

    def list_accounts(self):
        """Loads from the API and lists all GTM Accounts that a user has access to.

        Returns:
            A list of :class:`gtm_manager.account.GTMAccount` that the user has access to.
        """
        try:
            request = self.accounts_service.list()
            response = request.execute()
            return [
                gtm_manager.account.GTMAccount(account=x, service=self.service)
                for x in response.get("account")
            ]
        except errors.HttpError as error:
            logging.error(error)
            return []
