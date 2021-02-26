from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=255)
    sub_categories_count = models.IntegerField(default=0)  # Number of times used in subcategories


class SubCategories(models.Model):
    name = models.CharField(max_length=255)
    courses_count = models.IntegerField(default=0)  # Number of times used at courses
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


@receiver(post_save, sender=SubCategories, dispatch_uid="update_sub_categories_count")
def update_sub_categories_count(sender, instance, **kwargs):
    instance.category.sub_categories_count += 1
    instance.category.save()


@receiver(post_delete, sender=SubCategories, dispatch_uid="update_sub_categories_count")
def update_sub_categories_count(sender, instance, **kwargs):
    instance.category.sub_categories_count -= 1
    instance.category.save()


class Courses(models.Model):
    LEVEL_CHOICES = [
        (1, "Avanzado"),
        (2, "Introductorio"),
        (3, "Completo"),
        (4, "Intermedio")
    ]
    course_name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    real_price = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.IntegerField(null=True, blank=True)
    course_score = models.DecimalField(max_digits=5, decimal_places=2)
    # users field could be automatically update by post_save and post_delete too, but I don't have enough information
    users = models.IntegerField(default=0)

    @property
    def subcategory_name(self):
        return self.subcategory.name

    @property
    def category_name(self):
        return self.subcategory.category.name

    @property
    def username(self):
        return self.user.username


@receiver(post_save, sender=Courses, dispatch_uid="update_courses_count")
def update_courses_count(sender, instance, **kwargs):
    instance.subcategory.courses_count += 1
    instance.subcategory.save()


@receiver(post_delete, sender=Courses, dispatch_uid="update_courses_count")
def update_courses_count(sender, instance, **kwargs):
    instance.subcategory.courses_count -= 1
    instance.subcategory.save()
