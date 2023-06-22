# Generated by Django 4.1.5 on 2023-06-13 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewsChannel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("channel_id", models.CharField(blank=True, max_length=255, null=True)),
                ("slug", models.SlugField(max_length=255, null=True, unique=True)),
                ("tagline", models.CharField(blank=True, max_length=255, null=True)),
                ("politcial_spectrum", models.IntegerField(blank=True, null=True)),
                ("youtube_rank", models.IntegerField(blank=True, null=True)),
                ("fake_news_index", models.IntegerField(blank=True, null=True)),
                ("credibility_index", models.IntegerField(blank=True, null=True)),
                ("description", models.TextField()),
                ("founded_year", models.IntegerField(blank=True, null=True)),
                (
                    "channel_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "headquarters",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("language", models.CharField(blank=True, max_length=255, null=True)),
                ("official_website", models.URLField(blank=True, null=True)),
                ("youtube_channel", models.URLField(blank=True, null=True)),
                (
                    "twitter_handle",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                ("facebook_page", models.URLField(blank=True, null=True)),
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="static/news_logos"
                    ),
                ),
                ("subscribers", models.IntegerField(blank=True, null=True)),
                ("twitter_followers", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="sarso",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="TrendingTopic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topic", models.CharField(max_length=200)),
                ("rank", models.IntegerField(unique=True)),
                ("synopsis", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["rank"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("transcript", models.TextField()),
                ("published_date", models.DateTimeField()),
                ("video_url", models.URLField(max_length=2000)),
                ("thumbnail_url", models.URLField(max_length=2000)),
                ("topic", models.CharField(max_length=255)),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="videos",
                        to="pages.newschannel",
                    ),
                ),
            ],
        ),
    ]
