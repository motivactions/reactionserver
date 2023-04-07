from decimal import Decimal
from functools import cached_property
from logging import getLogger
from math import floor

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.models import Application

User = get_user_model()

logger = getLogger("django")


class ReactionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.hide_blocked_user = kwargs.pop("hide_blocked_user", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.hide_blocked_user:
            qs = super().get_queryset().filter(user__is_active=True)
        else:
            qs = super().get_queryset()
        return qs.select_related("user", "content_type")

    def get(self, *args, **kwargs):
        if self.hide_blocked_user:
            kwargs["user__is_active"] = True
        return super().get(*args, **kwargs)


class ReviewManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("user", "object_type")


class BookmarkManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("user", "content_type")


class Reaction(models.Model):
    LIKE = "like"
    LOVE = "love"
    PRAY = "pray"
    FLAP = "flap"
    FUNNY = "funny"
    SAD = "sad"
    ANGRY = "angry"
    REACTION_TYPES = (
        (LIKE, _("like")),
        (LOVE, _("love")),
        (PRAY, _("pray")),
        (FLAP, _("flap")),
        (FUNNY, _("funny")),
        (SAD, _("sad")),
        (ANGRY, _("angry")),
    )

    user = models.ForeignKey(
        User,
        related_name="reactions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    application = models.ForeignKey(
        Application,
        null=True,
        blank=True,
        related_name="reactions",
        on_delete=models.SET_NULL,
    )
    object_type = models.CharField(max_length=25)
    object_id = models.CharField(max_length=25)
    value = models.CharField(
        max_length=25,
        default=LIKE,
        choices=REACTION_TYPES,
        verbose_name=_("value"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    objects = ReactionManager()
    all_objects = ReactionManager(hide_blocked_user=False)

    class Meta:
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")

    def __str__(self):
        return '%s %s "%s"' % (self.user, self.get_value_display(), self.content_object)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.uid,)


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        related_name="bookmarks",
        on_delete=models.CASCADE,
        db_index=True,
    )
    application = models.ForeignKey(
        Application,
        null=True,
        blank=True,
        related_name="bookmarks",
        on_delete=models.SET_NULL,
    )
    object_type = models.CharField(max_length=25)
    object_id = models.CharField(max_length=25)
    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )
    objects = BookmarkManager()


class Review(models.Model):
    user = models.ForeignKey(
        User,
        related_name="ratings",
        on_delete=models.CASCADE,
        db_index=True,
    )
    application = models.ForeignKey(
        Application,
        null=True,
        blank=True,
        related_name="reviews",
        on_delete=models.SET_NULL,
    )
    object_type = models.CharField(max_length=25)
    object_id = models.CharField(max_length=25)
    target_type = models.CharField(max_length=25)
    target_id = models.CharField(max_length=25)
    rating = models.IntegerField(default=0, choices=[(x, f"{x}") for x in range(1, 6)])
    message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("message"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    objects = ReviewManager()

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    @cached_property
    def star_rating(self):
        rate = floor(self.rating)
        return rate

    @cached_property
    def star_rating_iterable(self):
        a = [0, 0, 0, 0, 0]
        for i, x in enumerate(range(self.star_rating)):
            a[i] = 1
        return a


class Flag(models.Model):
    SPAM = "spam"
    SEXUAL = "sexual"
    HATE = "hate"
    VIOLENCE = "violence"
    BULLYING = "bullying"
    HOAX = "hoax"
    SCAM = "scam"
    ILLEGAL = "illegal"
    OTHERS = "others"

    FLAG_TYPES = (
        (SPAM, _("spam")),
        (SEXUAL, _("sexual")),
        (HATE, _("hate")),
        (VIOLENCE, _("violence")),
        (BULLYING, _("bullying")),
        (HOAX, _("hoax")),
        (SCAM, _("scam")),
        (ILLEGAL, _("illegal")),
        (OTHERS, _("others")),
    )
    user = models.ForeignKey(
        User,
        related_name="flags",
        on_delete=models.CASCADE,
        db_index=True,
    )
    application = models.ForeignKey(
        Application,
        null=True,
        blank=True,
        related_name="flags",
        on_delete=models.SET_NULL,
    )
    object_type = models.CharField(max_length=25)
    object_id = models.CharField(max_length=25)
    value = models.CharField(
        max_length=25,
        default=SPAM,
        choices=FLAG_TYPES,
        verbose_name=_("value"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )
    objects = ReactionManager()
    message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("message"),
    )

    class Meta:
        verbose_name = _("Flag")
        verbose_name_plural = _("Flags")

    def __str__(self):
        return '%s %s "%s"' % (self.user, self.get_value_display(), self.content_object)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.uid,)
