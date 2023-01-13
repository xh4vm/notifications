import json
from datetime import date, datetime, timedelta

from django.contrib import admin
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import CreateManualMailing, TypeEvent
from .utils import get_template_params


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    """Displaying the TypeEvent model in the admin panel."""

    search_fields = ('name',)
    fields = ['name', 'subject', 'template_file', 'template_params', 'created']
    list_display = ('name', 'subject', 'template_file', 'template_params', 'created')
    readonly_fields = ('id', 'created', 'modified', 'template_params')

    def save_model(self, request, obj, form, change):
        field_template_file = request.FILES.get('template_file')
        if field_template_file:
            content = field_template_file.read().decode()
            params = get_template_params(content)
            obj.template_params = params
        obj.save()


@admin.register(CreateManualMailing)
class CreateManualMailing(admin.ModelAdmin):
    """Displaying the CreateManualMailing model in the admin panel."""

    fields = ['name', 'type_event', 'date_to_send', 'created', 'modified']
    search_fields = ('name',)
    list_display = ('name', 'get_template', 'get_template_params', 'date_to_send')
    readonly_fields = ('id', 'created', 'modified')
    list_filter = ('name', 'date_to_send')

    def get_template(self, obj):
        return obj.type_event.template_file

    get_template.short_description = 'Template'
    get_template.admin_order_field = 'type_event__template_file'

    def get_template_params(self, obj):
        return obj.type_event.template_params

    get_template_params.short_description = 'Template params'
    get_template_params.admin_order_field = 'type_event__template_params'

    def save_model(self, request, obj, form, change):
        date_today = date.today()

        if obj.date_to_send > date_today:
            start_time = datetime.combine(obj.date_to_send, datetime.min.time())
        else:
            start_time = datetime.utcnow()

        expires = start_time + timedelta(hours=25)

        schedule, created = IntervalSchedule.objects.get_or_create(every=4, period=IntervalSchedule.HOURS,)
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Task for mailing <{0}>, {1}, from {2} to {3}'.format(
                obj.name,
                obj.type_event.name,
                start_time.strftime('%d.%m.%Y %H:%M:%S'),
                expires.strftime('%d.%m.%Y %H:%M:%S'),
            ),
            task='notice.tasks.generator_event_manual_mailing',
            args=json.dumps([obj.type_event.name,]),
            start_time=start_time,
            expires=expires,
        )

        obj.save()
