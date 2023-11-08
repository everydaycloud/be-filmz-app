Check python interpreter is set to 'python 3.11.4 64-bit' (bottom right of window)

psql -f ./db/setup.sql

CREATE /db/database.ini
    [postgresql]
    host=localhost
    database=filmz_app_test

Run pytest to seed the database (will be amended later.)

Then, see 'requirements.txt' for install instructions.