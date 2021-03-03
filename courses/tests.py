from django.test import TestCase
import json
from .factories import UserFactory, CategoriesFactory, SubCategoriesFactory, CoursesFactory
from graphene_django.utils.testing import GraphQLTestCase


class CategoriesTest(TestCase):
    def setUp(self):
        self.category = CategoriesFactory()

    def test_attributes(self):
        category = CategoriesFactory(name="new category")
        self.assertEqual(category.name, "new category")

    def test_signal_counts_up_when_sub_category_is_created(self):
        sub_category_one = SubCategoriesFactory(category=self.category)
        self.assertEqual(self.category.sub_categories_count, 1)

        sub_category_two = SubCategoriesFactory(category=self.category)
        self.assertEqual(self.category.sub_categories_count, 2)

        sub_category_three = SubCategoriesFactory(category=self.category)
        self.assertEqual(self.category.sub_categories_count, 3)

    def test_signal_counts_down_when_sub_category_is_deleted(self):
        sub_category_one = SubCategoriesFactory(category=self.category)
        sub_category_two = SubCategoriesFactory(category=self.category)
        sub_category_three = SubCategoriesFactory(category=self.category)
        self.assertEqual(self.category.sub_categories_count, 3)

        sub_category_one.delete()
        self.assertEqual(self.category.sub_categories_count, 2)

        sub_category_two.delete()
        self.assertEqual(self.category.sub_categories_count, 1)

        sub_category_three.delete()
        self.assertEqual(self.category.sub_categories_count, 0)


class SubCategoriesTest(TestCase):
    def setUp(self):
        self.subcategory = SubCategoriesFactory()

    def test_attributes(self):
        category = CategoriesFactory()
        subcategory = SubCategoriesFactory(name="new subcategory", category=category)
        self.assertEqual(subcategory.name, "new subcategory")
        self.assertEqual(subcategory.courses_count, 0)
        self.assertEqual(subcategory.category, category)

    def test_signal_counts_up_when_course_is_created(self):
        course_one = CoursesFactory(subcategory=self.subcategory)
        self.assertEqual(self.subcategory.courses_count, 1)

        course_two = CoursesFactory(subcategory=self.subcategory)
        self.assertEqual(self.subcategory.courses_count, 2)

        course_three = CoursesFactory(subcategory=self.subcategory)
        self.assertEqual(self.subcategory.courses_count, 3)

    def test_signal_counts_down_when_course_is_deleted(self):
        course_one = CoursesFactory(subcategory=self.subcategory)
        course_two = CoursesFactory(subcategory=self.subcategory)
        course_three = CoursesFactory(subcategory=self.subcategory)
        self.assertEqual(self.subcategory.courses_count, 3)

        course_one.delete()
        self.assertEqual(self.subcategory.courses_count, 2)

        course_two.delete()
        self.assertEqual(self.subcategory.courses_count, 1)

        course_three.delete()
        self.assertEqual(self.subcategory.courses_count, 0)


class CoursesTest(TestCase):
    def setUp(self):
        self.subcategory = SubCategoriesFactory()
        self.user = UserFactory()
        self.courses = CoursesFactory(
            course_name="Course 1",
            subcategory=self.subcategory,
            level=1,
            user=self.user,
            real_price=12.2,
            price=11.1,
            discount=70,
            course_score=13.3,
            users=20,
        )

    def test_attributes(self):
        self.assertEqual(self.courses.course_name, "Course 1")
        self.assertEqual(self.courses.subcategory, self.subcategory)
        self.assertEqual(self.courses.level, 1)
        self.assertEqual(self.courses.user, self.user)
        self.assertEqual(self.courses.real_price, 12.2)
        self.assertEqual(self.courses.price, 11.1)
        self.assertEqual(self.courses.discount, 70)
        self.assertEqual(self.courses.course_score, 13.3)
        self.assertEqual(self.courses.users, 20)

    def test_properties(self):
        self.assertEqual(self.courses.subcategory_name, self.subcategory.name)
        self.assertEqual(self.courses.category_name, self.subcategory.category.name)
        self.assertEqual(self.courses.username, self.user.username)


class UserGraphQLTest(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_one = UserFactory()
        cls.user_two = UserFactory()

    def setUp(self):
        self.user_three = UserFactory()
        self.user_four = UserFactory()

    def test_user_query(self):
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


class CategoriesGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.category_one = CategoriesFactory()
        self.category_two = CategoriesFactory()

    def test_categories_query(self):
        response = self.query(
            '''
             {
                categories {
                    name
                    subCategoriesCount
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)


class SubCategoriesGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.subcategory_one = SubCategoriesFactory()
        self.subcategory_two = SubCategoriesFactory()

    def test_subcategories_query(self):
        response = self.query(
            '''
             {
                subCategories{
                  name
                  coursesCount
                  category {
                    id
                    name
                  }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)


class CoursesGraphQLTest(GraphQLTestCase):
    def setUp(self):
        self.courses_one = CoursesFactory()
        self.courses_two = CoursesFactory()

    def test_courses_query(self):
        response = self.query(
            '''
             {
                courses {
                courseName
                subcategory {
                  id
                  name
                }
                level
                user {
                  username
                }
                realPrice
                price
                discount
                courseScore
                users
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
