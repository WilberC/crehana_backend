from django.test import TestCase
import json
from .factories import UserFactory, CategoriesFactory, SubCategoriesFactory
from graphene_django.utils.testing import GraphQLTestCase


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


class UserGraphQLTest(GraphQLTestCase):
    def setUp(self):
        super().setUp()
        # user_one = UserFactory()
        user_one = UserFactory()
        user_one = UserFactory()

    def test_some_query(self):
        response = self.query(
            '''
             {
                users {
                    username
                    email
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)
