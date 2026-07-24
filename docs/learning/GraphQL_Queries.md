
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


---

### Fetching a single `Note`
---

To fetch a single note, we need to create a GraphQL field for a single note. 

```python
note = graphene.Field(NoteType, id=graphene.ID(required=True))
```

This will promises the caller that a single note exists. A single note is then resolved as:

```python
def resolve_note(self, info, id):
	try:
		return Note.object.get(pk=id)
	except Note.DoesNotExist:
		return None
```

Since to fetch a single note, we will need to pass in the ID of the note, we add `id` as an argument in the resolver. Since, the note for a given ID may or may not exist, we use a safer way to fetch it and if it does not exist, we return `None`. 


### GraphQL Queries
---
For the schema we defined, we run queries on: `localhost:8000/graphql`. 
- To fetch all notes we use the `resolve_notes` resolver.

```graphql
query {
	notes {
		id
		title
		content
	}
}
```

This returns:

```json
{
  "data": {
    "notes": [
      {
        "id": "4",
        "title": "Title 1",
        "content": "This is the first note. Hope this updates."
      },
      {
        "id": "5",
        "title": "Title 2",
        "content": "This is my second note. Hope it works!"
      },
      {
        "id": "6",
        "title": "Title 3",
        "content": "This is my third note. This seems to work well!"
      }
    ]
  }
}
```


- To fetch a single note, we use the `resolve_note` resolver. 

```graphql
query {
	note (id: 4) {
		id
		title
		content
		createdAt
		updatedAt
	}
}
```

This results in:

```json
{
  "data": {
    "note": {
      "id": "4",
      "title": "Title 1",
      "content": "This is the first note. Hope this updates.",
      "createdAt": "2026-07-23T12:57:50.605433+00:00",
      "updatedAt": "2026-07-23T18:24:05.728649+00:00"
    }
  }
}
```

An interesting thing to notice is that we defined the fields in the `note.models.Note` as `created_at` and `updated_at`, i.e., in snake case, but here, we are using camelCase. This is done by Graphene (GraphQL requires the fields in queries to be in camelCase according to its standards). 