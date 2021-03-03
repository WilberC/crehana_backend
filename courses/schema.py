from django.contrib.auth.models import User
from .models import Categories, SubCategories, Courses
from graphene_django import DjangoObjectType
import graphene


class UserGraphObject(DjangoObjectType):
    class Meta:
        model = User


class CategoriesGraphObject(DjangoObjectType):
    class Meta:
        model = Categories


class SubCategoriesGraphObject(DjangoObjectType):
    class Meta:
        model = SubCategories


class CoursesGraphObject(DjangoObjectType):
    class Meta:
        model = Courses


class CoursesQuery(graphene.ObjectType):
    users = graphene.List(UserGraphObject)
    categories = graphene.List(CategoriesGraphObject)
    sub_categories = graphene.List(SubCategoriesGraphObject)
    courses = graphene.List(CoursesGraphObject)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_categories(self, info):
        return Categories.objects.all()

    def resolve_sub_categories(self, info):
        return SubCategories.objects.all()

    def resolve_courses(self, info):
        return Courses.objects.all()
