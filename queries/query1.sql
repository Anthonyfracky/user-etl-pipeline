-- Query 1: Retrieve the count of users who signed up on each day
SELECT signup_date, COUNT(*) AS users_count
FROM users
GROUP BY signup_date
ORDER BY signup_date;