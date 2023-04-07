from django.db import models


class ReactionableModel(models.Model):
    reaction = models.JSONField(
        editable=False,
        verbose_name=_("reaction"),
        help_text=_('JSON fields contains {"like": 1, "love":2, "flap":3}'),
    )

    reactions = GenericRelation(Reaction)

    class Meta:
        abstract = True

    def get_reactions(self, reaction=None):
        extra_filter = {}
        if reaction:
            extra_filter.update({"value": reaction})
            reactions = self.reactions.filter(**extra_filter)
        else:
            reactions = self.reactions.all()
        return reactions

    def calculate_reaction(self):
        reactions = (
            self.get_reactions().values("value").annotate(total=models.Count("id"))
        )
        self.reaction = {obj["value"]: obj["total"] for obj in reactions}

    def save(self, *args, **kwargs):
        self.calculate_reaction()
        return super().save(*args, **kwargs)

    def add_reaction(self, user, value):
        """add reaction to object"""
        content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
        try:
            reaction = Reaction.objects.get(
                content_type=content_type, object_id=self.id, user=user
            )
            reaction.value = value
            reaction.save()
        except Reaction.DoesNotExist:
            reaction = Reaction(
                content_type=content_type, object_id=self.id, user=user, value=value
            )
            # TODO: Add notification
            reaction.save()
        return reaction

    def user_reaction(self, user):
        reaction = self.get_user_reaction(user)
        if reaction:
            return reaction
        else:
            return None

    def get_user_reaction(self, user):
        return self.reactions.filter(user=user.id).first()


class BookmarkableModel(models.Model):
    bookmarked = models.PositiveIntegerField(
        default=0,
        verbose_name=_("bookmarked"),
        help_text=_("Total bookmarked"),
    )

    bookmarks = GenericRelation(Bookmark)

    class Meta:
        abstract = True

    def add_bookmark(self, user):
        """add bookmark to object"""
        content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
        bookmark = self.bookmarks.filter(
            content_type=content_type, object_id=self.id, user=user
        ).first()
        if bookmark is None:
            bookmark = Bookmark(content_type=content_type, object_id=self.id, user=user)
            bookmark.save()
            self.save()

    def remove_bookmark(self, user):
        """remove bookmark to object"""
        content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
        bookmark = self.bookmarks.filter(
            content_type=content_type, object_id=self.id, user=user
        ).first()
        if bookmark is not None:
            bookmark.delete()
            self.save()

    def calculate_bookmark(self):
        self.bookmarked = (
            self.bookmarks.aggregate(total=models.Count("id"))["total"] or 0
        )

    def save(self, *args, **kwargs):
        self.calculate_bookmark()
        return super().save(*args, **kwargs)


class ReviewableModel(models.Model):
    RATING_STRING = {
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
        "10": "ten",
    }
    rating = models.DecimalField(
        max_digits=4,
        default=Decimal("0.00"),
        decimal_places=2,
        editable=False,
        verbose_name=_("rating"),
    )
    review_count = models.IntegerField(
        default=0,
        verbose_name=_("review count"),
    )
    reviews = GenericRelation(
        Review,
        content_type_field="object_type",
        object_id_field="object_id",
    )
    review = models.JSONField(
        editable=False,
        verbose_name=_("review"),
        help_text=_('JSON fields contains {"one": 1, "two":1, "three":1}'),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

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

    def get_reviews(self, rating=None):
        extra_filter = {}
        if rating:
            extra_filter.update({"rating": rating})
            reviews = self.reviews.filter(**extra_filter)
        else:
            reviews = self.reviews.all()
        return reviews

    def calculate_review(self):
        reviews = self.get_reviews().values("rating").annotate(total=models.Count("id"))
        self.review = {
            self.RATING_STRING.get(str(obj["rating"]), obj["rating"]): obj["total"]
            for obj in reviews
        }

    def count_rating(self):
        self.review_count = self.reviews.count()

    def calculate_rating(self):
        self.rating = self.reviews.aggregate(models.Avg("rating"))[
            "rating__avg"
        ] or Decimal("0.00")

    def add_review(self, user, rating, message=None, target_object=None):
        """add review to object"""
        object_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
        target_type = None
        target_id = None
        if target_object:
            target_type = ContentType.objects.get_for_model(
                target_object, for_concrete_model=True
            )
            target_id = target_object.id
        review = Review(
            object_type=object_type,
            object_id=self.id,
            user=user,
            target_type=target_type,
            target_id=target_id,
            rating=rating,
            message=message,
        )
        review.save()
        return review

    def save(self, *args, **kwargs):
        self.calculate_review()
        self.calculate_rating()
        self.count_rating()
        return super().save(*args, **kwargs)


class FlaggableModel(models.Model):
    flag = models.JSONField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("flag"),
        help_text=_('JSON fields contains {"spam": 1, "hoax":2, "bullying":3}'),
    )

    flags = GenericRelation(Flag)

    class Meta:
        abstract = True

    def get_flags(self, flag=None):
        extra_filter = {}
        if flag:
            extra_filter.update({"value": flag})
            flags = self.flags.filter(**extra_filter)
        else:
            flags = self.flags.all()
        return flags

    def calculate_flag(self):
        flags = self.get_flags().values("value").annotate(total=models.Count("id"))
        self.flag = {obj["value"]: obj["total"] for obj in flags}

    def save(self, *args, **kwargs):
        self.calculate_flag()
        return super().save(*args, **kwargs)

    def add_flag(self, user, value, message=None):
        """add flag to object"""
        content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
        try:
            flag = Flag.objects.get(
                content_type=content_type, object_id=self.id, user=user
            )
            flag.value = value
            flag.message = message
            flag.save()
        except Flag.DoesNotExist:
            flag = Flag(
                content_type=content_type,
                object_id=self.id,
                user=user,
                value=value,
                message=message,
            )
            flag.save()
        return flag


@receiver(post_save, sender=Flag)
def recalculate_object_flag(sender, instance, **kwargs):
    if instance.content_object is not None:
        instance.content_object.save()


@receiver(post_save, sender=Reaction)
def recalculate_object_reaction(sender, instance, **kwargs):
    if instance.content_object is not None:
        instance.content_object.save()
    # TODO send notification to user when reaction created


@receiver(post_delete, sender=Reaction)
def recalculate_object_reaction_remove(sender, instance, **kwargs):
    if instance.content_object is not None:
        instance.content_object.save()


@receiver(post_save, sender=Review)
def recalculate_object_rating(sender, instance, **kwargs):
    if instance.content_object is not None:
        instance.content_object.save()
    # TODO send notification to user when review created


@receiver(post_delete, sender=Review)
def recalculate_object_rating_remove(sender, instance, **kwargs):
    if instance.content_object is not None:
        instance.content_object.save()
    # TODO send notification to user when review created
