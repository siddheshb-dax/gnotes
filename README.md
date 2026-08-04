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


### LICENSE
This project is licensed under the Boost Software License (BSL 1). Check the [LICENSE](./LICENSE) file or visit the official [Boost Software License](https://www.boost.org/LICENSE_1_0.txt) page.
