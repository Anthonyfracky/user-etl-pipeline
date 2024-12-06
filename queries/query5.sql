-- Query 5: Delete records where email domain is not in the specified list
-- CAUTION: This query will permanently delete records
DELETE FROM users
WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'ukr.net');