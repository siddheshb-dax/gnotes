import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as django_login
from graphene_django import DjangoObjectType # This tells Graphene that 'this is based on a Django model'

from .models import Note, Activity

from django.contrib.auth import get_user_model

User = get_user_model()

from .services import log

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
        queryset = Note.objects.filter(owner=info.context.user)
        if title:
            queryset = queryset.filter(title__icontains=title)

        if content:
            queryset = queryset.filter(content__icontains=content)

        return queryset

    def resolve_note(self, info, id):
        try:
            return Note.objects.get(pk=id, owner=info.context.user)
        except Note.DoesNotExist:
            return None

class CreateNote(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=False)
        content = graphene.String(required=True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls, root, info, title='', content=''):
        if not info.context.user.is_authenticated:
            raise Exception("User must be authenticated")

        note = Note.objects.create(
            owner=info.context.user,
            title=title,
            content=content
        )     

        log(
            user=info.context.user,
            action=Activity.Action.CREATE,
            note=note,
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
        if not info.context.user.is_authenticated:
            raise Exception("User must be authenticated")

        try:
            note = Note.objects.get(pk=id, owner=info.context.user)
        except Note.DoesNotExist:
            return UpdateNote(note=None)

        if title is not None:
            note.title = title

        if content is not None:
            note.content = content
        
        note.save()

        log(
            user=info.context.user,
            action=Activity.Action.UDPATE,
            note=note
        )

        return UpdateNote(note=note)

class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise Exception("User must be authenticated")

        try:
            note = Note.objects.get(pk=id, owner=info.context.user)
        except Note.DoesNotExist:
            return DeleteNote(success=False)

        log(
            user=info.context.user,
            action=Activity.Action.DELETE,
            note=note,
        )

        note.delete()
        return DeleteNote(success=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = User.objects.create_user(
            username=username,
            password=password
        )

        return CreateUser(user=user)

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    user = graphene.Field(UserType)

    @classmethod 
    def mutate(cls, root, info, username, password):
        user = authenticate(request=info.context, username=username, password=password)

        if user is None:
            return LoginUser(success=False, user=None)

        django_login(info.context, user)

        Activity.objects.create(
            user=user,
            action=Activity.Action.LOGIN,
        )

        return LoginUser(success=True, user=user)

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()

    create_user = CreateUser.Field()
    login = LoginUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)