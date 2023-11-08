\c filmz_app_test

SELECT * FROM watchlist
JOIN films ON watchlist.film_id = films.id 
WHERE watchlist.film_id = 671;

-- SELECT * FROM watchlist
-- JOIN users ON watchlist.user_id = users.user_id 
-- WHERE watchlist.user_id = 1;