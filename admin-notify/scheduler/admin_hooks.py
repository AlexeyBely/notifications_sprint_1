import json

from django_celery_beat.admin import PeriodicTaskAdmin

from scheduler.models import GroupPeriodicTask


class GroupTaskModelAdmin(PeriodicTaskAdmin):

    def save_model(self, request, obj: GroupPeriodicTask, form, change):
        """Add to arguments calery template and group."""
        arguments = {
            'template': str(obj.template),
            'group': str(obj.group) if obj.group is not None else None,
            'name_task': obj.name
        }
        obj.kwargs = json.dumps(arguments)        
        obj.save()
