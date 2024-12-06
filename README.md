# User Data Import Project

This application processes user data from a CSV file and stores it in a PostgreSQL database using SQLAlchemy. It includes data validation, error handling, and database migrations using Alembic.

## Project Structure
```
project-root/
│
├── data.csv               # Input CSV file with user data
├── main.py                # Main application script for data processing
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Instructions to build the application Docker image
├── requirements.txt       # Python dependencies
├── start.sh               # Startup script for database initialization
│
├── alembic/               # Database migration configuration
│   ├── env.py
│   └── versions/
│
├── queries/               # Predefined SQL query files
│   ├── query1.sql
│   ├── query2.sql
│   ├── query3.sql
│   ├── query4.sql
│   └── query5.sql
│
└── README.md              # Project documentation
```

## Prerequisites
- Docker
- Docker Compose
- Python 3.8+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Anthonyfracky/user-etl-pipeline
cd user-etl-pipeline
```

2. Ensure you have Docker and Docker Compose installed on your system.

## Running the Application

1. Build and start the application:
```bash
docker-compose up --build
```

This command will:
- Build the Docker containers
- Wait for the PostgreSQL database to be ready
- Run database migrations
- Import user data from `data.csv` into the database

## Accessing the Database

### Database Connection Details
- **Host:** localhost
- **Port:** 5432
- **Database Name:** users_db
- **Username:** postgres
- **Password:** password

### Connecting to the Database
You can connect to the database using:

```bash
docker-compose exec db psql -U postgres -d users_db
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

To run these queries, connect to the database and use standard PostgreSQL query execution.

## Data Processing Details

### Input Data
- Expects a CSV file (`data.csv`) with columns:
  - `user_id`
  - `name`
  - `email`
  - `signup_date`

### Data Validation
- Email addresses are validated using a regex pattern
- Signup dates are parsed and standardized
- Invalid entries are logged and skipped

## Logging
Application logs are output to the console, providing information about:
- Data processing
- Database operations
- Any errors encountered during import

## Notes
- Ensure `data.csv` is in the correct format before running
- The application will skip entries with invalid email formats