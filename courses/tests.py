from django.test import TestCase
from .factories import CategoriesFactory, SubCategoriesFactory


class CategoriesTest(TestCase):

    def test_attributes(self):
        category = CategoriesFactory(name="new category")
        self.assertEqual(category.name, "new category")

    def test_signal_counts_up_when_sub_category_is_created(self):
        category = CategoriesFactory()
        sub_category_one = SubCategoriesFactory(category=category)
        self.assertEqual(category.sub_categories_count, 1)

        sub_category_two = SubCategoriesFactory(category=category)
        self.assertEqual(category.sub_categories_count, 2)

        sub_category_three = SubCategoriesFactory(category=category)
        self.assertEqual(category.sub_categories_count, 3)

    def test_signal_counts_down_when_sub_category_is_created(self):
        category = CategoriesFactory()
        sub_category_one = SubCategoriesFactory(category=category)
        sub_category_two = SubCategoriesFactory(category=category)
        sub_category_three = SubCategoriesFactory(category=category)
        self.assertEqual(category.sub_categories_count, 3)

        sub_category_one.delete()
        self.assertEqual(category.sub_categories_count, 2)

        sub_category_two.delete()
        self.assertEqual(category.sub_categories_count, 1)

        sub_category_three.delete()
        self.assertEqual(category.sub_categories_count, 0)
