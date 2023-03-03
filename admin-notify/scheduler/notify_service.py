import logging
import requests

from abc import ABC, abstractmethod
from config.components.env_setting import env_settings


logger = logging.getLogger(__name__)


class BaseNotifyService(ABC):
    @abstractmethod
    def send_user_ids_to_notify(self, template: str, user_ids: list) -> bool:
        """Sends a template and users ID to the notification service.
        
        return False if not fault.
        """
        return False


class DebugNotifyService(BaseNotifyService):

    def send_user_ids_to_notify(self, template: str, user_ids: list) -> bool:
        logger.info(f'{len(user_ids)} users were sent to the notification service')
        logger.info(f'<sending_user_ids>  {template}: {user_ids}')
        return False


class ApiNotifyService(BaseNotifyService):

    def send_user_ids_to_notify(self, template: str, user_ids: list) -> bool:
        response = requests.post(
            env_settings.notify_api_url,
            json = {'template': template, 'users': user_ids},
            timeout = env_settings.notify_api_timeout   
        )
        if response.status_code is not requests.codes.ok:
            return True
        return False
    

notify_service = ApiNotifyService()


def get_notify_service() -> BaseNotifyService:
    return notify_service