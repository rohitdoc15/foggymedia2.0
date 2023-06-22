from django.db import migrations

def convert_topic_to_charfield(apps, schema_editor):
    Video = apps.get_model('pages', 'Video')
    for video in Video.objects.all():
        video.topic = str(video.topic)
        video.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_previous_migration'),  # Replace with the previous migration name
    ]

    operations = [
        migrations.RunPython(convert_topic_to_charfield),
    ]
