from flask import request

def fetch_all_films(connection):
    film_title = request.args.get('title')
    with connection: 
        
        with connection.cursor() as cursor:
            if film_title:
                cursor.execute('SELECT * FROM films WHERE title ILIKE %s;',('%' + film_title + '%',))
                film_by_title=cursor.fetchall()

                result = []
                for film in film_by_title:
                        result.append({"id": film[3], "title": film[10], "overview": film[6], "poster_path": film[8],
                                    "release_date": film[9], "vote_average": film[12], "vote_count": film[13]})
                if len(result) <= 0:
                        return {"message": "We couldn't find this film."}
                else:     
                        return {"films": result}

            else:
                cursor.execute('SELECT * FROM films;')
                films=cursor.fetchall()

                if films:
                    result = []
                    for film in films:
                        result.append({"id": film[3], "title": film[10], "overview": film[6], "poster_path": film[8],
                                    "release_date": film[9], "vote_average": film[12], "vote_count": film[13]})
                return {"films": result}