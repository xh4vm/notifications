import uuid
from datetime import date

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .utils import validate_doctype, validate_template


class TimeStampedMixin(models.Model):
    """Class mixin for field s with DateTimeField type."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        """Class Meta for TimeStampedMixin."""

        abstract = True


class UUIDMixin(models.Model):
    """Class mixin for field s with uuid4 type."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(object):
        """Class Meta for UUIDMixin."""

        abstract = True


def validate_file_contents(value):
    contents = value.read().decode()
    first_line, rest_of_file = contents.split('\n', 1)

    if not validate_doctype(first_line):
        raise ValidationError('File does not have valid doctype')
    if not validate_template(rest_of_file):
        raise ValidationError('The file does not contain correctly formatted html code.')

    value.seek(0)


def validate_date_to_send(value: date):
    if value < date.today():
        raise ValidationError('The sending date [{0}] cannot be a past date'.format(value.strftime('%d.%m.%Y')))


class TypeEvent(UUIDMixin, TimeStampedMixin):
    """Class for the type event model."""

    name = models.TextField(_('Name'), max_length=settings.MAX_TEXT_FIELD_LENGTH)
    subject = models.TextField(_('Subject'), max_length=512)
    template_file = models.FileField(upload_to=settings.EMAILS_TEMPLATE_PATH, validators=[validate_file_contents])
    template_params = ArrayField(
        models.CharField(max_length=settings.MAX_TEXT_FIELD_LENGTH, blank=True, null=True), blank=True, null=True,
    )

    class Meta(object):
        """Class Meta for Genre."""

        db_table = 'content"."type_event'
        verbose_name = _('Type event')
        verbose_name_plural = _('Type events')
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        """Represent class Genre as string.

        Returns:
            result
        """
        return '{0} ({1})'.format(self.name, self.template_file.name)


# post_delete.connect(
#     file_cleanup, sender=TypeEvent, dispatch_uid="type_event.file_cleanup"
# )


@receiver(post_delete, sender=TypeEvent)
def post_save_file(sender, instance, *args, **kwargs):
    """ Clean Old file """
    try:
        instance.template_file.delete(save=False)
    except Exception:
        pass


@receiver(pre_save, sender=TypeEvent)
def pre_save_file(sender, instance, *args, **kwargs):
    """ instance old file will delete from os """
    try:
        old_file = instance.__class__.objects.get(id=instance.id).template_file.path
        try:
            new_file = instance.template_file.path
        except Exception:
            new_file = None
        if new_file != old_file:
            import os

            if os.path.exists(old_file):
                os.remove(old_file)
    except Exception:
        pass


class CreateManualMailing(UUIDMixin, TimeStampedMixin):
    """Class for the admin model."""

    name = models.TextField(_('Name'), max_length=settings.MAX_TEXT_FIELD_LENGTH)
    type_event = models.ForeignKey('TypeEvent', on_delete=models.CASCADE, verbose_name=_('Type event (template)'),)
    date_to_send = models.DateField(validators=[validate_date_to_send])

    class Meta(object):
        """Class Meta for Genre."""

        db_table = 'content"."create_manual_mailing'
        verbose_name = _('Create manual mailing')
        verbose_name_plural = _('Create manual mailings')
        indexes = [models.Index(fields=['name'])]
