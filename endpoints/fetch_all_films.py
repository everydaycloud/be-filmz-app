from flask import request

def fetch_all_films(connection):
    film_title = request.args.get('title')
    
    with connection: 
        with connection.cursor() as cursor:
            if film_title:
                cursor.execute('''
                    SELECT 
                        f.*,
                        COALESCE(AVG(r.rating), 0) AS average_rating
                    FROM 
                        films f
                    LEFT JOIN 
                        reviews r ON f.id = r.film_id
                    WHERE 
                        f.title ILIKE %s
                    GROUP BY 
                        f.id;
                ''', ('%' + film_title + '%',))
                
                films_and_ratings = cursor.fetchall()

                if not films_and_ratings:
                    return {"message": "We couldn't find any films with the provided title."}

                result = []
                for film in films_and_ratings:
                    result.append({
                        "id": film[3],
                        "original_title": film[5],
                        "overview": film[6],
                        "poster_path": film[8],
                        "release_date": film[9],
                        "average_rating": float(film[14]) 
                    })

                return {"films": result}
            else:
                
                cursor.execute('''
                    SELECT 
                        f.*,
                        COALESCE(AVG(r.rating), 0) AS average_rating
                    FROM 
                        films f
                    LEFT JOIN 
                        reviews r ON f.id = r.film_id
                    GROUP BY 
                        f.id;
                ''')

                films_and_ratings = cursor.fetchall()

                result = []
                for film in films_and_ratings:
                    result.append({
                        "id": film[3],
                        "original_title": film[5],
                        "overview": film[6],
                        "poster_path": film[8],
                        "release_date": film[9],
                        "average_rating": float(film[14])
                    })
                print (result)
                return {"films": result}



# from flask import request

# def fetch_all_films(connection):
#     film_title = request.args.get('title')
#     with connection: 
        
#         with connection.cursor() as cursor:
#             if film_title:
#                 cursor.execute('SELECT * FROM films WHERE title ILIKE %s;',('%' + film_title + '%',))
#                 film_by_title=cursor.fetchall()

#                 result = []
#                 for film in film_by_title:
#                         result.append({"id": film[3], "title": film[10], "overview": film[6], "poster_path": film[8],
#                                     "release_date": film[9]})
#                 if len(result) <= 0:
#                         return {"message": "We couldn't find this film."}
#                 else:     
#                         return {"films": result}

#             else:
#                 cursor.execute('SELECT * FROM films;')
#                 films=cursor.fetchall()

#                 if films:
#                     result = []
#                     for film in films:
#                         result.append({"id": film[3], "title": film[10], "overview": film[6], "poster_path": film[8],
#                                     "release_date": film[9]})
#                 return {"films": result}