from utils.random_numbers import random_from_list, random_decimal_number, random_int
from faker import Faker
from . import models
import factory

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n:  f"{fake.user_name()}{n}")
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.lazy_attribute
    def email(self):
        return f"{self.username}@{fake.free_email_domain()}"


class CategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Categories

    name = fake.paragraph(nb_sentences=1)


class SubCategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SubCategories

    name = fake.paragraph(nb_sentences=1)
    category = factory.SubFactory(CategoriesFactory)


class CoursesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Courses

    course_name = fake.paragraph(nb_sentences=2)
    subcategory = factory.SubFactory(SubCategoriesFactory)
    level = random_from_list(models.Courses.LEVEL_CHOICES)
    user = factory.SubFactory(UserFactory)
    real_price = random_decimal_number()
    price = random_decimal_number()
    discount = random_int()
    course_score = random_decimal_number(max_number=5)
    users = random_int(max_number=10000)
