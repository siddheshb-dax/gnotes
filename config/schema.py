import graphene
import notes.schema

class Query(notes.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
