from django.contrib import admin

from .models import TypeEvent
from .utils import get_template_params


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    """Displaying the TypeEvent model in the admin panel."""

    search_fields = ('name',)
    fields = ['name', 'template_file', 'template_params', 'created']
    list_display = ('name', 'template_file', 'template_params', 'created')
    readonly_fields = ('id', 'created', 'modified', 'template_params')

    def save_model(self, request, obj, form, change):
        field_template_file = request.FILES.get('template_file')
        if field_template_file:
            contents = field_template_file.read().decode()
            params = get_template_params(contents)
            obj.template_params = params
        obj.save()
