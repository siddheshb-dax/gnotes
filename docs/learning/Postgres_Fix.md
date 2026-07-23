
### Issue
---
Running `python manage.py migrate` resulted in a `permission denied with public schema`. 

Verified:
- Django connected as `note_admin`
- Database was `note_db`
- Current schema was `public`
- `search_path` was `"$user", public`

Initially, the database role lacked the necessary permissions on the `public` schema.

### Fix
---
Grant privileges to the application user:

```sql
postgres=> GRANT ALL PRIVILEGES ON DATABASE note_db TO note_admin;
GRANT
postgres=> \c note_db
note_db=> GRANT ALL ON SCHEMA public TO note_admin;
GRANT
```

Now, `python manage.py` ran successfully: 

```bash
$ poetry run python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```


### Advice for the future
---
- Create a user.
```sql
CREATE ROLE project_db_admin LOGIN PASSWORD '<password>';
```

- Have the user own the DB
```sql
CREATE DATABASE project_db OWNER project_db_admin;
```
