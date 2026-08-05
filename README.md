## Notes++ V2

> WIP

Simple CRUD note taking app with Django, GraphQL and Postgres.

### Usage

#### In different terminals:
- Start the Redis Server
```bash
redis-server
```

- Start the backend
```bash
uv run python manage.py runserver
```

- Start the Celery workers
```bash
uv run celery -A config worker --loglevel=info
```

### Running Imports 

> NOTE: The CSV file used to run imports must have fieldnames as title and content

- Launch Insomnia
- Create a new `POST` request to `http://localhost:8000/graphql`
- Navigate to the body tab below the address bar and hit the dropdown to select 'Form Data' to select multipart form.
- Set the first name as `operations` and fill in the value:
```json
{  "query": "mutation ($file: Upload!) { importNotes(file: $file) { importedCount skippedCount } }",  "variables": {    "file": null  }}
```

- Hit on the Add button and create a new name as `map` and fill the value as:
```json
{  "0": ["variables.file"]}
```
- Hit the Add button again and create a new name as '0' and change its type to file from the dropdown and select the CSV file to import. 
- Make sure that the `redis-server` and `celery` workers are running to avoid duplicate values in the DB. 
- Hit Send.


### LICENSE
This project is licensed under the Boost Software License (BSL 1). Check the [LICENSE](./LICENSE) file or visit the official [Boost Software License](https://www.boost.org/LICENSE_1_0.txt) page.
