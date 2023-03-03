import json
import logging

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config.celery import app as celery_app
from config.components.env_setting import env_settings
from scheduler.notify_service import get_notify_service
from scheduler.users import (sorting_users_for_timezones, 
                             sorting_delayed_users_for_timezones)


logger = logging.getLogger(__name__)


class TaskError(Exception):
   """User task Exception."""

   pass


def create_task_delayed_send(name_task: str, template: str, user_ids: list) -> None:
    """Sends a template and users ID to delayed celery task."""
    logger.info(f'{len(user_ids)} users delayed sending')
    schedule_delay, created = IntervalSchedule.objects.get_or_create(
        every=env_settings.schedule_delay_min,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.update_or_create(
        name=f'{name_task}_delayed',
        defaults={
            'enabled': True,
            'interval': schedule_delay,
            'task': 'scheduler.tasks.send_delayed_massege',
            'args': json.dumps(user_ids),
            'kwargs': json.dumps(
                {'template': template,
                 'name_task': name_task}
            ),
        }
    )


def user_ids_to_notify_service(
    tamplate: str,
    name_task: str, 
    sending_ids: list, 
    not_sending_ids: list
) -> None:
    """Sending to the notification service and delayed task."""

    if len(sending_ids) > 0:
        notify_service = get_notify_service()
        fault_send = notify_service.send_user_ids_to_notify(tamplate, sending_ids)
        if fault_send is True:
            raise TaskError(
                f'Failure send task to notify api service {env_settings.notify_api_url}'
            )    
    if len(not_sending_ids) > 0:
        create_task_delayed_send(name_task, tamplate, not_sending_ids)
    else:
        delayed_task = PeriodicTask.objects.filter(name=f'{name_task}_delayed')
        if delayed_task is not None:
            delayed_task.delete()      


@celery_app.task
def send_group_massege(*args, **kwargs):
    """sends a task to send a message to each user to the notification api service."""

    group_sending = kwargs['group']
    sending_user_ids, not_sending_user_ids = sorting_users_for_timezones(group_sending)
    user_ids_to_notify_service(kwargs['template'], kwargs['name_task'], 
                               sending_user_ids, not_sending_user_ids)
    

@celery_app.task
def send_delayed_massege(*args, **kwargs):
    """sends a task to send a delayed message to each user to the api notification."""

    sending_user_ids, not_sending_user_ids = sorting_delayed_users_for_timezones(args)
    user_ids_to_notify_service(kwargs['template'], kwargs['name_task'], 
                               sending_user_ids, not_sending_user_ids)
