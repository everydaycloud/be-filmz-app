import json
from db.connection import get_connection

# Function to seed database
def seed_database():

    with open('./db/data/test-data/films.json', 'r') as json_file:
        film_data = json.load(json_file)

    with open('./db/data/test-data/users.json', 'r') as json_file:
        user_data = json.load(json_file)

    with open('./db/data/test-data/watchlist.json', 'r') as json_file:
        watchlist_data = json.load(json_file)
        
    with open('./db/data/test-data/reviews.json', 'r') as json_file:
        review_data = json.load(json_file)

    with open('./db/data/test-data/review_comments.json', 'r') as json_file:
        review_comments_data = json.load(json_file)

    with open('./db/data/test-data/friendships.json', 'r') as json_file:
        friendship_data = json.load(json_file)

    friendship_values = []
    for friendship in friendship_data:
        friendship_values.append((
            friendship['user1'],
            friendship['user2']
        ))

    drop_friendships_table = """
        DROP TABLE IF EXISTS friendships;
    """

    create_friendships_table = """
        CREATE TABLE friendships (
        friendship_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        friend_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (user_id, friend_id)
        );
    """

    insert_friendships_data = """
        INSERT INTO friendships 
        (user_id, friend_id)
        VALUES 
        (%s, %s);
    """

    user_values = []
    user_list = user_data['users'] 
    for user in user_list:
        user_values.append(( 
            user["username"],
            user["password"],
            user["email"],
            user["avatar"]
        ))

    drop_users_table = """
        DROP TABLE IF EXISTS users;
    """

    create_users_table = """
        CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        avatar VARCHAR(400)
        );
    """

    insert_user_data = """
        INSERT INTO users 
        (username, password, email, avatar)
        VALUES 
        (%s, %s, %s, %s);
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
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    review_values = []
    for review in review_data:
        review_values.append(( 
            review["user_id"],
            review["film_id"],
            review["body"],
            review["rating"],
            review["votes"],
            review["created_at"],
        ))

    watchlist_values = []
    for entry in watchlist_data:
        watchlist_values.append(( 
            entry["user_id"],
            entry["film_id"]
        ))

    drop_watchlist_table = """
        DROP TABLE IF EXISTS watchlist;
    """

    create_watchlist_table = """
        CREATE TABLE watchlist (
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            film_id INT REFERENCES films(id),
            is_watched BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, film_id)
        );
    """

    insert_watchlist_data = """
        INSERT INTO watchlist 
        (user_id, film_id)
        VALUES 
        (%s, %s);
    """

    drop_reviews_table = """
        DROP TABLE IF EXISTS reviews;
    """

    create_reviews_table = """
        CREATE TABLE reviews (
            review_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            film_id INTEGER REFERENCES films(id),
            body TEXT,
            rating INTEGER,
            votes INTEGER NOT NULL,
            created_at DATE NOT NULL
        );
    """
    
    insert_review_data = """
        INSERT INTO reviews 
        (user_id, film_id, body, rating, votes, created_at)
        VALUES 
        (%s, %s, %s, %s, %s, %s);
    """

    review_comment_values = []
    for comment in review_comments_data:
        review_comment_values.append(( 
            comment["user_id"],
            comment["review_id"],
            comment["body"],
            comment["created_at"],
            comment["votes"],
        ))

    drop_review_comments_table = """
        DROP TABLE IF EXISTS review_comments;
    """

    create_review_comments_table = """
        CREATE TABLE review_comments (
            review_comment_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            review_id INTEGER REFERENCES reviews(review_id) ON DELETE CASCADE,
            body TEXT,
            created_at DATE NOT NULL,
            votes INTEGER NOT NULL
        );
    """

    insert_review_comment_data = """
        INSERT INTO review_comments 
        (user_id, review_id, body, created_at, votes)
        VALUES 
        (%s, %s, %s, %s, %s);
    """
    
    db_connection = None
    try:
        db_connection = get_connection()
        db_connection.autocommit = True

        cursor = db_connection.cursor()    

        # Delete the review_comments table
        cursor.execute(drop_review_comments_table)
        db_connection.commit() 
        
        # Delete the watchlist table
        cursor.execute(drop_watchlist_table)
        db_connection.commit()
        
        # Delete the reviews table
        cursor.execute(drop_reviews_table)
        db_connection.commit()

         # Delete the friendships table
        cursor.execute(drop_friendships_table)
        db_connection.commit()

        # Delete the films table
        cursor.execute(drop_films_table)
        db_connection.commit()

        # Delete the users tables
        cursor.execute(drop_users_table)
        db_connection.commit()

        # Create the films table
        cursor.execute(create_films_table)
        db_connection.commit()

        # Create the users table
        cursor.execute(create_users_table)
        db_connection.commit()

        # Create the friendships table
        cursor.execute(create_friendships_table)
        db_connection.commit()

        # Create the watchlist table
        cursor.execute(create_watchlist_table)
        db_connection.commit()

        # Create the reviews table
        cursor.execute(create_reviews_table)
        db_connection.commit()

        # Create the reviews table
        cursor.execute(create_review_comments_table)
        db_connection.commit()

        # Insert data into the films table
        cursor.executemany(insert_film_data, film_values)
        db_connection.commit()

        # Insert data into the users table
        cursor.executemany(insert_user_data, user_values)
        db_connection.commit()

        # Insert data into the friendships table
        cursor.executemany(insert_friendships_data, friendship_values)
        db_connection.commit()

        # Insert data into the watchlist table
        cursor.executemany(insert_watchlist_data, watchlist_values)
        db_connection.commit()
        
        # Insert data into the reviews table
        cursor.executemany(insert_review_data, review_values)
        db_connection.commit()

        # Insert data into the reviews_comment table
        cursor.executemany(insert_review_comment_data, review_comment_values)
        db_connection.commit()

        print("Data seeded successfully!")

    except Exception as e:
        print("Error:", e)
           
seed_database()