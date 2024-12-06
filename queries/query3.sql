-- Query 3: Retrieve users who signed up in the last 7 days
SELECT *
FROM users
WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY signup_date;