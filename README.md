# User Data Processing Application

This application processes user data from a CSV file and stores it in a PostgreSQL database using SQLAlchemy. It includes data validation, error handling, and database migrations using Alembic.

## Project Structure

```
.
├── alembic/
│   ├── versions/
│   └── env.py
├── queries/
│   ├── query1.sql
│   ├── query2.sql
│   ├── query3.sql
│   ├── query4.sql
│   └── query5.sql
├── data.csv
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── init_migrations.sh
├── main.py
├── README.md
└── requirements.txt
```

## Prerequisites

- Docker
- Docker Compose
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Anthonyfracky/user-etl-pipeline
cd user-etl-pipeline
```

2. The repository includes a sample data.csv file generated using the Faker library. You can use this file for testing or replace it with your own data following the same structure:
```csv
user_id,name,email,signup_date
1,John Doe,john@example.com,2024-01-01 10:00:00
```

## Running the Application

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Initialize the database and run migrations (first time only):
```bash
docker-compose run migrations
```

3. The application will automatically:
   - Run database migrations
   - Process the data.csv file
   - Import the data into PostgreSQL

## Accessing the Database

You can access the PostgreSQL database in several ways:

### Using psql in the container:
```bash
docker-compose exec db psql -U postgres users_db
```

### Running SQL queries from files:
```bash
# Run a specific query
docker-compose exec db psql -U postgres users_db -f /queries/query1.sql
```

## Included SQL Queries

The project includes several SQL queries in the `queries/` directory:

1. `query1.sql`: Daily user signup statistics
   ```sql
   -- Retrieves the count of users who signed up on each day
   SELECT signup_date, COUNT(*) AS users_count
   FROM users
   GROUP BY signup_date
   ORDER BY signup_date;
   ```

2. `query2.sql`: Unique email domains
   ```sql
   -- Lists all unique email domains in the database
   SELECT DISTINCT domain
   FROM public.users
   ORDER BY domain;
   ```

3. `query3.sql`: Recent signups
   ```sql
   -- Retrieves users who signed up in the last 7 days
   SELECT *
   FROM public.users
   WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days'
   ORDER BY signup_date;
   ```

4. `query4.sql`: Users with the most common email domain
   ```sql
   -- Finds user(s) with the most common email domain
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
   ```

5. `query5.sql`: Domain filtering (CAUTION: Modifies data)
   ```sql
   -- Deletes records where email domain is not in the specified list
   DELETE FROM users
   WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'ukr.net');
   ```

## Development

### Adding New Migrations

To create a new migration:
```bash
docker-compose run app alembic revision --autogenerate -m "Description of changes"
```

### Running Migrations

To apply migrations:
```bash
docker-compose run app alembic upgrade head
```