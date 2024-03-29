# Generated by Django 4.2 on 2023-04-07 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("apps", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                ("object_type", models.CharField(max_length=25)),
                ("object_id", models.CharField(max_length=25)),
                ("target_type", models.CharField(max_length=25)),
                ("target_id", models.CharField(max_length=25)),
                (
                    "rating",
                    models.IntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        default=0,
                    ),
                ),
                (
                    "message",
                    models.TextField(blank=True, null=True, verbose_name="message"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviews",
                        to="apps.application",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
            },
        ),
        migrations.CreateModel(
            name="Reaction",
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
                ("object_type", models.CharField(max_length=25)),
                ("object_id", models.CharField(max_length=25)),
                (
                    "value",
                    models.CharField(
                        choices=[
                            ("like", "like"),
                            ("love", "love"),
                            ("pray", "pray"),
                            ("flap", "flap"),
                            ("funny", "funny"),
                            ("sad", "sad"),
                            ("angry", "angry"),
                        ],
                        default="like",
                        max_length=25,
                        verbose_name="value",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reactions",
                        to="apps.application",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Reaction",
                "verbose_name_plural": "Reactions",
            },
        ),
        migrations.CreateModel(
            name="Flag",
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
                ("object_type", models.CharField(max_length=25)),
                ("object_id", models.CharField(max_length=25)),
                (
                    "value",
                    models.CharField(
                        choices=[
                            ("spam", "spam"),
                            ("sexual", "sexual"),
                            ("hate", "hate"),
                            ("violence", "violence"),
                            ("bullying", "bullying"),
                            ("hoax", "hoax"),
                            ("scam", "scam"),
                            ("illegal", "illegal"),
                            ("others", "others"),
                        ],
                        default="spam",
                        max_length=25,
                        verbose_name="value",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "message",
                    models.TextField(blank=True, null=True, verbose_name="message"),
                ),
                (
                    "application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="flags",
                        to="apps.application",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flags",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Flag",
                "verbose_name_plural": "Flags",
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
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
                ("object_type", models.CharField(max_length=25)),
                ("object_id", models.CharField(max_length=25)),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bookmarks",
                        to="apps.application",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
