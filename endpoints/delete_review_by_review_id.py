def delete_review(connection, review_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM reviews WHERE review_id = %s RETURNING *;', (review_id,))
            review = cursor.fetchone()
            return ({"message":f"Review {review_id} deleted.", "review":review})