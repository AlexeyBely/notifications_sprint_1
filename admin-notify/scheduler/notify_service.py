import logging
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class BaseNotifyService(ABC):
    @abstractmethod
    def send_user_ids_to_notify(self, template: str, user_ids: list) -> bool:
        """Sends a template and users ID to the notification service."""
        pass


class DebugNotifyService(BaseNotifyService):

    def send_user_ids_to_notify(self, template: str, user_ids: list) -> bool:
        """Sends a template and users ID to the notification service."""

        logger.info(f'{len(user_ids)} users were sent to the notification service')
        logger.info(f'<sending_user_ids>  {template}: {user_ids}')


notify_service = DebugNotifyService()


def get_notify_service() -> BaseNotifyService:
    return notify_service