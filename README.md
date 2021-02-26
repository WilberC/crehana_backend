# ERD


# Seed DB
To seed the DB you can run `python manage.py seed_courses` which will populate the DB
( source code for command `courses/management/commands/seed_courses.py` )

- It will return a response with how many courses were migrated (remember that I'm using `get_or_create` to avoid duplicity)