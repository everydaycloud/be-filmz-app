import json
import psycopg2

with open('../data/test-data/films.json', 'r') as json_file:
    film_data = json.load(json_file)

with open('../data/test-data/users.json', 'r') as json_file:
    user_data = json.load(json_file)

print(user_data)

user_values = []
user_list = user_data['users'] # iterates through the array
for user in user_list:
    user_values.append(( 
        user["username"],
        user["password"],
        user["email"]
    ))
    #append fulfils same role as push in js

drop_users_table = """
    DROP TABLE IF EXISTS users;
"""

create_users_table = """
    CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255)
    );
"""

insert_user_data = """
    INSERT INTO users 
    (username, password, email)
    VALUES 
    (%s, %s, %s)
"""

film_values = []
film_list = film_data['results']
for film in film_list: 
    film_values.append((
        film["adult"],
        film["backdrop_path"],
        film["genre_ids"],
        film["id"],        
        film["original_language"],        
        film["original_title"],
        film["overview"],
        film["popularity"],
        film["poster_path"],
        film["release_date"],
        film["title"],        
        film["video"],
        film["vote_average"],
        film["vote_count"],
    ))

drop_films_table = """
DROP TABLE IF EXISTS films;
"""

create_films_table = """
    CREATE TABLE films (
        adult BOOLEAN,
        backdrop_path VARCHAR(255),
        genre_ids INT ARRAY,        
        id SERIAL PRIMARY KEY,
        original_language VARCHAR(255),
        original_title VARCHAR(255),
        overview TEXT, 
        popularity NUMERIC, 
        poster_path VARCHAR(255),
        release_date DATE,
        title VARCHAR (255),
        video BOOLEAN,
        vote_average NUMERIC, 
        vote_count INT
    );
"""

insert_film_data = """
    INSERT INTO films 
    (adult, backdrop_path, genre_ids, id, original_language, original_title, overview, popularity, poster_path, release_date, title, video, vote_average, vote_count)
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    connection = psycopg2.connect("dbname=filmz_app_test")
    cursor = connection.cursor()

    # Delete the films table
    cursor.execute(drop_films_table)
    connection.commit()

     # Delete the users table
    cursor.execute(drop_users_table)
    connection.commit()

    # Create the films table
    cursor.execute(create_films_table)
    connection.commit()

    # Create the users table
    cursor.execute(create_users_table)
    connection.commit()

    # Insert data into the films table
    cursor.executemany(insert_film_data, film_values)
    connection.commit()

    # Insert data into the users table
    cursor.executemany(insert_user_data, user_values)
    connection.commit()

    print("Data seeded successfully!")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()