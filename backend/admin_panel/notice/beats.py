from django_celery_beat.models import (CrontabSchedule, IntervalSchedule,
                                       PeriodicTask)


def create_default_beats(apps, schema_editor):

    PeriodicTask.objects.create(
        interval=IntervalSchedule.objects.create(every=4, period=IntervalSchedule.HOURS),
        name="New review's likes",
        task='notice.tasks.generator_event_get_new_review_likes'
    )

    PeriodicTask.objects.create(
        crontab=CrontabSchedule.objects.create(minute='0', hour='1,5,9,13,17,21', day_of_week='1'),
        name="Forgotten Bookmarks",
        task='notice.tasks.generator_event_notification_bookmarks'
    )

    PeriodicTask.objects.create(
        crontab=CrontabSchedule.objects.create(minute='0', hour='2,6,10,14,18,22', day_of_week='3'),
        name="New movies",
        task='notice.tasks.generator_event_new_movies'
    )
