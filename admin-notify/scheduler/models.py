import uuid
import pytz

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (IntervalSchedule, CrontabSchedule, 
                                       SolarSchedule, ClockedSchedule, PeriodicTask)


MAX_LENGTH_NAME = 255


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(_('Name'), max_length=MAX_LENGTH_NAME)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        abstract = True


class Groop(UUIDMixin, TimeStampedMixin, NameMixin):
    """Grouping users for sending messages."""

    class Meta:
        db_table = 'notify\'.\'groop'
        verbose_name = _('groop')
        verbose_name_plural = _('groops')

    def __str__(self):
        return self.name
    

class User(TimeStampedMixin):
    """Timezone and permissions for each user.
    
    The model instances is not created or edited in the Admin Django.
    The user instances is created through the api notification service.
    """
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')
    email_permission = models.BooleanField(default=False)
    browser_permission = models.BooleanField(default=False)
    push_permission = models.BooleanField(default=False)
    mobile_permission = models.BooleanField(default=False)
    groops = models.ManyToManyField(Groop, through='GroopUser')

    class Meta:
        db_table = 'notify\'.\'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(
                fields=['timezone'],
                name='user_timezone_idx'
            )
        ]

    def __str__(self):
        return str(self.id)
    

class GroopUser(UUIDMixin):
    """Matching group to user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    groop = models.ForeignKey(
        Groop,
        on_delete=models.CASCADE,
        verbose_name=_('groop')
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notify\'.\'groop_user'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'groop_id'],
                name='user_groop_idx'
            ),
        ]


class Template(UUIDMixin, TimeStampedMixin, NameMixin):
    """Location and name of the template for sending messages."""

    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='template/')
    file_name = models.CharField(_('file_name'), max_length=MAX_LENGTH_NAME)

    class Meta:
        db_table = 'notify\'.\'template'
        verbose_name = _('template')
        verbose_name_plural = _('templates')

    def __str__(self):
        return self.name


class GroopPeriodicTask(UUIDMixin, TimeStampedMixin, NameMixin):
    """Task for group messaging.
    
    Acts as an intermediate link between group mailing and 
    periodic tasks django_celery_beat.
    """
    groop = models.ForeignKey(
        Groop,
        on_delete=models.CASCADE,
        verbose_name=_('Groop')
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        verbose_name=_('Template')
    )
    # fields according to scheduler django_celery_beat
    task = models.CharField(
        max_length=200,
        verbose_name=_('Task Name',),
    )
    one_off = models.BooleanField(
        default=False,
        verbose_name=_('One-off Task'),
    )
    start_time = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('Start Datetime'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Enabled'),
    )
    interval = models.ForeignKey(
        IntervalSchedule, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name=_('Interval Schedule'),
    )
    crontab = models.ForeignKey(
        CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Crontab Schedule'),
    )
    solar = models.ForeignKey(
        SolarSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Solar Schedule'),
    )
    clocked = models.ForeignKey(
        ClockedSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Clocked Schedule'),
    )
    periodic_tasks = models.ManyToManyField(PeriodicTask, through='GroopInPeriodicTask')

    class Meta:
        db_table = 'notify\'.\'groop_periodic_task'
        verbose_name = _('groop_periodic_task')
        verbose_name_plural = _('groop_periodic_tasks')

    def __str__(self):
        return self.name
    

class GroopInPeriodicTask(UUIDMixin):
    """Matching group to user."""

    periodic_task = models.ForeignKey(
        PeriodicTask,
        on_delete=models.CASCADE,
        verbose_name=_('periodic_task')
    )
    groop_periodic_task = models.ForeignKey(
        GroopPeriodicTask,
        on_delete=models.CASCADE,
        verbose_name=_('groop_periodic_task')
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notify\'.\'groop_in_periodic_task'
        constraints = [
            models.UniqueConstraint(
                fields=['periodic_task_id', 'groop_periodic_task_id'],
                name='groop_in_periodic_task_idx'
            ),
        ]
