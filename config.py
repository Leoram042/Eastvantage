# Define the SQLALCHEMY_DATABASE_URL variable, which specifies the database URL.
# This URL points to a SQLite database file named "address_book.db" in the current directory.

SQLALCHEMY_DATABASE_URL = "sqlite:///./address_book.db"

# In this context, "sqlite://" indicates that you're using SQLite as the database engine,
# and "./address_book.db" specifies the relative path to the SQLite database file.
# If you were using a different database system (e.g., PostgreSQL, MySQL), the URL format
# would be different, indicating the appropriate database server and credentials.
