
```python
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

    def resolve_notes(self, info):
        return Note.objects.all()

```


The `Query` class defines the entry point for reading the data in the GraphQL API. 

```python
class Query:
	notes = graphene.List(NoteType)
```

This snippet above creates GraphQL field named `notes`. It promises that, API can ask for this field and the server will return a list of `NoteType` objects. The GraphQL schema has a field named `notes`. Its return type is a list, and every item in that list follows the `NoteType` shape.

```python
def resolve_notes(self, info):
	return Note.objects.all()
```

This function above is prefixed with a `resolve_`, this means that Graphene looks for these functions (which are prefixed with `resolve_`) followed by the field name to find out how to actually fetch the data. In this case we `return Note.objects.all()` a simple ORM query returning all the `Note` objects. But we could add filters to this specific function to tell how the objects should be fetched. The `info` argument to the function provides context and other information that can be used to add more filters like:

```python
def resolve_notes(self, user):
	user = info.context.user
	return Note.objects.all(author=user) if user.is_authenticated else Note.objects.none()
```

---

In short,
- `Note`: The Django ORM model representing a DB table.
- `NoteType`: The GraphQL representation of `Note`. Graphene uses it to serialize and de-serialize the `Note` object. 
- `resolve_notes()`: The resolver which fetches the data from the DB.