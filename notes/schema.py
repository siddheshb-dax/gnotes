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
            "updated_at",
        )

class Query(graphene.ObjectType):
    notes = graphene.List(NoteType)
    note = graphene.Field(NoteType, id=graphene.ID(required=True))

    def resolve_notes(self, info):
        return Note.objects.all()

    def resolve_note(self, info, id):
        try:
            return Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return None

class CreateNote(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=False)
        content = graphene.String(required=True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls, root, info, title='', content=''):
        note = Note.objects.create(
            title=title,
            content=content,
        )

        return CreateNote(note=note)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

schema = graphene.Schema(query=Query)