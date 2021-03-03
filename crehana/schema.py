from graphene import ObjectType, Schema
from courses.schema import CoursesQuery


class Query(CoursesQuery,
            ObjectType):
    pass


schema = Schema(query=Query)

# No mutations required for this demo project
# class Mutation(ObjectType):
#     pass

# schema = Schema(query=Query, mutation=Mutation)
