from django.contrib.auth.models import User as UserModel
from graphene_django import DjangoObjectType
import graphene


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class UserQuery(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return UserModel.objects.all()
