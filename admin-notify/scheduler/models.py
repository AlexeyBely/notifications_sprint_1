import uuid
import pytz
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask


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


class Group(UUIDMixin, TimeStampedMixin, NameMixin):
    """Grouping users for sending messages."""

    class Meta:
        db_table = 'notify\'.\'group'
        verbose_name = _('group')
        verbose_name_plural = _('groups')

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
    from_time = models.TimeField(default=datetime.time(9, 00))
    befor_time = models.TimeField(default=datetime.time(20, 00))
    email_permission = models.BooleanField(default=False)
    browser_permission = models.BooleanField(default=False)
    push_permission = models.BooleanField(default=False)
    mobile_permission = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, through='GroupUser')

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
    

class GroupUser(UUIDMixin):
    """Matching group to user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('group')
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notify\'.\'group_user'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'group_id'],
                name='user_group_idx'
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


class GroupPeriodicTask(PeriodicTask, TimeStampedMixin, NameMixin):
    """Task for group messaging.
    
    Acts as an intermediate link between group mailing and 
    periodic tasks django_celery_beat.
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_('Group'),
        blank=True, 
        null=True,
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        verbose_name=_('Template')
    )
    
    class Meta:
        db_table = 'notify\'.\'group_periodic_task'
        verbose_name = _('group_periodic_task')
        verbose_name_plural = _('group_periodic_tasks')

    def __str__(self):
        return self.name

