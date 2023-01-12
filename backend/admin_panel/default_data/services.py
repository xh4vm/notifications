from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from notice.utils import get_template_params


def insert_default_type_events(apps, schema_editor):

    insert_one_type_event(apps, settings.EVENT_NEW_REVIEW_LIKES, subject='Событие о новом лайке')
    insert_one_type_event(apps, settings.EVENT_FORGOTTEN_BOOKMARKS, subject='Событие о забытой закладке')
    insert_one_type_event(apps, settings.EVENT_NEW_MOVIES_FOR_PERIOD, subject='Событие о фильме')


def insert_one_type_event(apps, event: tuple, subject: str):

    type_event = apps.get_model('notice', 'TypeEvent')

    file_template_input_path = Path.joinpath(settings.BASE_DIR, event[1])

    file_template_upload_path = '{0}{1}'.format(settings.EMAILS_TEMPLATE_PATH, file_template_input_path.name)

    with open(file_template_input_path) as file_tmp:
        file_template = default_storage.save(file_template_upload_path, File(file_tmp))
        file_tmp.seek(0)
        content = file_tmp.read()

        params = get_template_params(content)

    type_event.objects.get_or_create(name=event[0], subject=subject, template_file=file_template, template_params=params)
