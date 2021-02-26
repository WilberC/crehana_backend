from django.core.management.base import BaseCommand, CommandError
from ...models import Categories, SubCategories, Courses, User
import pandas as pd
import numpy as np
from decimal import Decimal
from crehana.settings import BASE_DIR


def get_excel_data():
    courses_list_path = BASE_DIR / "courses_list.xlsx"
    data = pd.read_excel(courses_list_path, header=0, index_col=0, keep_default_na=True)
    # Other good option to avoid column_stack is to use zip, but let's keep being a fancy dev
    return np.column_stack((
        data["course_name"],
        data["category_name"],
        data["subcategory_name"],
        data["level"],
        data["username"],
        data["real_price"],
        data["price"],
        data["discount"],
        data["course_score"],
        data["users"],
    ))


def get_level_options():
    return {lvl_str: val for val, lvl_str in Courses.LEVEL_CHOICES}


class Command(BaseCommand):
    help = 'This command will populated bd'

    def handle(self, *args, **options):
        # -----------------------------------------------------------------
        level_options = get_level_options()
        courses_created = 0
        # -----------------------------------------------------------------
        # I can clean the list and then iterate through the clean list or
        # better take advantage of get_or_create and loop just one time
        for course_name, category_name, subcategory_name, level, username, real_price, price, discount, course_score, users in get_excel_data():
            # I should use just create for Courses, but for projects purpose I will use
            # get_or_create to avoid duplicated data when I seed the BD
            category = Categories.objects.get_or_create(name=category_name)
            subcategory = SubCategories.objects.get_or_create(name=subcategory_name, category=category[0])
            # Valid user is created
            user, user_created = User.objects.get_or_create(username=username, email=f"{username}@gmail.com")
            if user_created:
                # If user is created I set a password
                user.set_password("123456")
                user.save()
            course, course_created = Courses.objects.get_or_create(course_name=course_name,
                                                                   subcategory=subcategory[0],
                                                                   level=level_options[level],
                                                                   user=user,
                                                                   real_price=Decimal(real_price),
                                                                   price=Decimal(price),
                                                                   discount=discount,
                                                                   course_score=Decimal(course_score),
                                                                   users=users)
            if course_created:
                courses_created += 1
        self.stdout.write(f"{courses_created} Courses were created", ending='.')
        # -----------------------------------------------------------------
