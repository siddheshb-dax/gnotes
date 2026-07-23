import graphene
from graphene_django import DjangoObjectType # This tells Graphene that 'this is based on a Django model'

from .models import Note

class NoteType(DjangoObjectType):
    class Meta:
        model = Note # This connects the object to the ORM

        # This defines what the GraphQL API exposes
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "udpated_at",
        )

class Query(graphene.ObjectType):
    notes = graphene.List(NoteType)

    def resolve_notes(self, info):
        return Note.objects.all()

schema = graphene.Schema(query=Query)