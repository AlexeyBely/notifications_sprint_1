from django.contrib import admin
from django_celery_beat.admin import PeriodicTaskForm, PeriodicTaskAdmin
from django.utils.translation import gettext_lazy as _
from django import forms

from scheduler.models import Groop, GroopUser, User, Template, GroopPeriodicTask
from scheduler.admin_hooks import GroopTaskModelAdmin


@admin.register(Groop)
class GroopAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


@admin.register(Template)
class GroopAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'file_name',
    )


class GroopUserInline(admin.TabularInline):
    model = GroopUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'id',
        'get_groops',
        'timezone',
    )
    list_prefetch_related = ('groops')
    inlines = (
        GroopUserInline,
    )
    search_fields = (
        'id',
        'timezone',
    )

    def get_groops(self, obj):
        return ','.join([groop.name for groop in obj.groops.all()])
    get_groops.short_description = _('groops')
    

class GroopPeriodicTaskForm(PeriodicTaskForm):
    """Form that lets you create and modify groop tasks."""

    class Meta:
        """Form metadata."""

        model = GroopPeriodicTask
        exclude = ()

    def clean(self):
        data = super().clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc

        count_schedule = 0
        if data.get('interval') is not None:
            count_schedule += 1
        if data.get('crontab') is not None:
            count_schedule += 1
        if data.get('solar') is not None:
            count_schedule += 1
        if data.get('clocked') is not None:
            count_schedule += 1
        if count_schedule != 1:
            raise forms.ValidationError(
                _('One scheduling must be specified')
            )
        
        return data


@admin.register(GroopPeriodicTask)
class GroopPeriodicTaskAdmin(GroopTaskModelAdmin):
    form = GroopPeriodicTaskForm
    list_display = ('name', 'groop', 'enabled', 'interval', 'clocked', 
                    'start_time', 'one_off')
    search_fields = ('name', 'groop',)
    list_filter = ['enabled', 'one_off', 'task', 'start_time']
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Groop'), {
            'fields': ('groop', 'template',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('interval', 'crontab', 'solar', 'clocked',
                       'start_time', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
    )
