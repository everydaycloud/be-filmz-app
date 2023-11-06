import json
import psycopg2

with open('../data/test-data/films.json', 'r') as json_file:
    loaded_films = json.load(json_file)

sample_data = loaded_films['results'][0]
print(sample_data)

drop_table_sql = """
DROP TABLE IF EXISTS films;
"""

create_table_sql = """
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

insert_data_sql = """
    INSERT INTO films 
    (adult, backdrop_path, genre_ids, id, original_language, original_title, overview, popularity, poster_path, release_date, title, video, vote_average, vote_count)
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    connection = psycopg2.connect("dbname=filmz_app_test")
    cursor = connection.cursor()

    # Delete the users table
    cursor.execute(drop_table_sql)
    connection.commit()

    # Create the users table
    cursor.execute(create_table_sql)
    connection.commit()

    # Insert data into the users table
    cursor.executemany(insert_data_sql, sample_data)
    connection.commit()

    print("Data seeded successfully!")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()