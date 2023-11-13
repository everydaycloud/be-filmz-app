from flask import jsonify

def remove_review_by_id(review_id, connection):
    DELETE_REVIEW_BY_ID = """
    DELETE FROM reviews WHERE review_id = %s
    RETURNING *;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_REVIEW_BY_ID, (review_id,))
            deleted_review = cursor.fetchone()

            if deleted_review:
                return jsonify({'message': f'Review {deleted_review} deleted successfully'})
            else:
                return jsonify({'message': 'Review not found'})
            