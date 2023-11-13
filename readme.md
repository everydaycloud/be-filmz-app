***Welcome to the Filmz API!***

This API serves up information about films, user reviews and user comments, allows the users to add friends, reviews and films to their watchlist and more. It's a base for an app for films lovers who would like to keep track of what they have watched, review it and comment on their friends' reviews and share their passion for film with others. 

The live API can be accessed here: https://be-filmz-app.onrender.com

***Setup instructions (fork and clone the repo first):***

1. Make sure that you have Python3 and python3-flask installed on your machine.
2. Run the command "pip install -r requirements.txt" to install all dependencies listed in the requirements.txt file. If you experience any trouble with this go to your Python interpreter and make sure that the version matches the project (python 3.11.4).
3. Create a 'database.ini' file inside the 'db' folder. Paste the following contents inside 
    [postgresql]
    host=localhost
    database=filmz_app_test
4. Run the command "psql -f ./db/setup.sql" to set up the database.
5. Run the seed.py file to seed the database. One way you can do this is by right-clicking and selecting 'Run Python'.
6. You're good to go!
7. EXTRA - If you'd like to deploy the project yourself you will need to add a '.env' file at the top of the directory and paste the following inside DATABASE_URL="<url to your own postgres instance>".
