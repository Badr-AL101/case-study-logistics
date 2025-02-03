from sqlalchemy import create_engine, text

password_file = "/run/secrets/db_password"
with open(password_file,"r") as f:
     db_password = f.readline().strip()

# Database connection URL
DATABASE_URL = f"mysql+pymysql://user:{db_password}@logistics-etl-warehouse-1/logistics"

engine = create_engine(DATABASE_URL, echo=True)

def test_connection():
    # Test the database connection
    with engine.connect() as connection:
        # Query to fetch the MySQL server version
        result = connection.execute(text("SELECT VERSION();"))
        version = result.scalar()
        print(f"Connected to MySQL Server version: {version}")

        # Simple query to check connectivity and basic functionality
        try:
            connection.execute(text("SELECT 1"))
            print("Connection to the database is stable.")
        except Exception as e:
            print(f"Error testing the database connection: {e}")

test_connection()

