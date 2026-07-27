import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType # This tells Graphene that 'this is based on a Django model'

from .models import Note

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")

class NoteType(DjangoObjectType):
    owner = graphene.Field(UserType)

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
    '''
        The fields below contain the queryable fields 
        which can be used to search for Note objects
    '''
    notes = graphene.List(
        NoteType,
        title=graphene.String(),
        content=graphene.String()
    )

    note = graphene.Field(NoteType, id=graphene.ID(required=True))

    def resolve_notes(self, info, title=None, content=None):
        queryset = Note.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)

        if content:
            queryset = queryset.filter(content__icontains=content)

        return queryset

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

class UpdateNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=False)
        title = graphene.String(required=False)
        content = graphene.String(required=False)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls, root, info, id = '', title = '', content = ''):
        # Case 1 - ID given
        if id:
            note = Note.objects.get(pk=id)
            if title is not None:
                note.title = title

            if content:
                note.content = content

        # Case 2: Title given
        if title:
            note = Note.objects.get(title=title)
            note.title = title

            if content:
                note.content = content

        note.save()
        return UpdateNote(note=note)

class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            note = Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return DeleteNote(success=False)

        note.delete()
        return DeleteNote(success=True)
    

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()

schema = graphene.Schema(query=Query)