from django.contrib import admin 
from django.utils.translation import gettext_lazy as _

from scheduler.models import Group, GroupUser, User, Template, GroupPeriodicTask
from scheduler.admin_hooks import GroupTaskModelAdmin


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'file_path',
    )


class GroupUserInline(admin.TabularInline):
    model = GroupUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'id',
        'get_groups',
        'timezone',
    )
    list_prefetch_related = ('groups')
    inlines = (
        GroupUserInline,
    )
    search_fields = (
        'id',
        'timezone',
    )

    def get_groups(self, obj):
        return ','.join([group.name for group in obj.groups.all()])
    get_groups.short_description = _('groups')


@admin.register(GroupPeriodicTask)
class GroupPeriodicTaskAdmin(GroupTaskModelAdmin):
    list_display = ('name', 'group', 'enabled', 'interval', 'clocked', 
                    'start_time', 'one_off')
    search_fields = ('name', 'group',)
    list_filter = ['enabled', 'one_off', 'task', 'start_time']
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Group'), {
            'fields': ('group', 'template',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('interval', 'crontab', 'solar', 'clocked',
                       'start_time', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
    )
