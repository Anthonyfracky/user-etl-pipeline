-- Query 4: Find user(s) with the most common email domain
WITH domain_counts AS (
    SELECT domain, COUNT(*) AS domain_frequency
    FROM users
    GROUP BY domain
    ORDER BY domain_frequency DESC
    LIMIT 1
)
SELECT u.*
FROM users u
JOIN domain_counts dc ON u.domain = dc.domain;