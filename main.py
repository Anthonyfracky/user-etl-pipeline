import re
import csv
import time
import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date

# Configure logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a base class for SQLAlchemy models
Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    Represents user data with fields for ID, user ID, name, email, signup date, and domain.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    name = Column(String)
    email = Column(String)
    signup_date = Column(Date)
    domain = Column(String)


def extract_domain(email):
    """
    Validate email and extract the domain part.

    Args:
        email (str): The email address to process.

    Returns:
        str or None: Domain if the email is valid, otherwise None.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return email.split('@')[-1]
    return None


def process_dataset(file_name):
    """
    Read and process data from a CSV file.

    Args:
        file_name (str): Path to the CSV file.

    Returns:
        list: Transformed data as a list of dictionaries.
    """
    transformed_data = []
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Format date and validate email domain
                    formatted_date = datetime.strptime(
                        row['signup_date'],
                        '%Y-%m-%d %H:%M:%S'
                    ).strftime('%Y-%m-%d')

                    domain = extract_domain(row['email'])
                    if domain is None:
                        logger.warning(f"Invalid email for user {row['user_id']}")
                        continue

                    transformed_data.append({
                        'user_id': row['user_id'],
                        'name': row['name'],
                        'email': row['email'],
                        'signup_date': formatted_date,
                        'domain': domain
                    })
                except ValueError as e:
                    logger.error(f"Error processing row {row}: {str(e)}")
                    continue
    except Exception as e:
        logger.error(f"Error reading file {file_name}: {str(e)}")
        raise

    logger.info(f"Processed {len(transformed_data)} valid records")
    return transformed_data


def save_to_database(data):
    """
    Save processed data to the database with simplified error handling.

    Args:
        data (list): A list of dictionaries containing user data.
    """
    DATABASE_URL = 'postgresql://postgres:password@db:5432/users_db'

    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            for item in data:
                user = User(
                    user_id=item['user_id'],
                    name=item['name'],
                    email=item['email'],
                    signup_date=datetime.strptime(item['signup_date'], '%Y-%m-%d').date(),
                    domain=item['domain']
                )
                session.add(user)

            session.commit()
            logger.info(f"Successfully saved {len(data)} records to the database.")

        except Exception as e:
            session.rollback()
            logger.error(f"Error saving data: {e}")
            raise

        finally:
            session.close()

    except Exception as e:
        # Якщо підключення не вдалося, одразу логуємо помилку
        logger.error(f"Failed to connect to the database: {e}")
        raise Exception("Failed to connect to the database")


def main():
    """
    Main function to orchestrate the data processing and saving workflow.
    """
    try:
        input_file = 'data.csv'
        logger.info("Starting data processing")
        result = process_dataset(input_file)
        logger.info("Starting database save")
        save_to_database(result)
        logger.info("Process completed successfully")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
