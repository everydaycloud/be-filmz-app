\c filmz_app_test

-- SELECT * FROM watchlist
-- JOIN films ON watchlist.film_id = films.id 
-- WHERE watchlist.film_id = 671;

-- SELECT * FROM watchlist
-- JOIN users ON watchlist.user_id = users.user_id 
-- WHERE watchlist.user_id = 1;

-- SELECT * FROM users; 

-- SELECT * FROM friendships WHERE user_id = 2;

-- SELECT f.user_id, f.friend_id, f.created_at
--     FROM friendships AS f
--     -- WHERE f.user_id = 2
--     -- COUNT(c.article_id) AS comment_count
--     LEFT JOIN users AS u ON f.friend_id = u.user_id 
--     WHERE f.user_id = 2
--     GROUP BY f.user_id;

-- SELECT u.username AS username, f.user_id AS user_id, uf.username AS friend_name, f.created_at AS friends_since, f.friend_id AS friend_id
-- FROM friendships f
-- JOIN users u ON f.user_id = u.user_id
-- JOIN users uf ON f.friend_id = uf.user_id
-- -- WHERE u.user_id = 2;

SELECT * FROM reviews;

    -- SELECT
    --     f.*,
    --     r.original_title,
    --     AVG(r.rating) AS average_rating
    -- FROM
    --     films f
    -- JOIN
    --     reviews r ON f.id = r.film_id
    -- WHERE
    --     f.id = 672
    -- GROUP BY
    --     f.id, r.original_title;

                    SELECT 
                        f.*,
                        COALESCE(AVG(r.rating), 0) AS average_rating
                    FROM 
                        films f
                    LEFT JOIN 
                        reviews r ON f.id = r.film_id
                    GROUP BY 
                        f.id;