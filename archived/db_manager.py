import pyodbc
from db_config import DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD

def connect_db():
    """Connect to the Azure SQL database using credentials from db_config.py."""
    conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={DB_SERVER};Database={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}"
    return pyodbc.connect(conn_str)

def create_tables(conn):
    """Create the consultants and consultant_slides tables if they do not exist."""
    cursor = conn.cursor()
    
    # Create consultants table
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='consultants' AND xtype='U')
        BEGIN
            CREATE TABLE consultants (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255),
                title NVARCHAR(255),
                mobile NVARCHAR(255),
                location NVARCHAR(255),
                email NVARCHAR(255)
            )
        END
    ''')
    
    # Create consultant_slides table
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='consultant_slides' AND xtype='U')
        BEGIN
            CREATE TABLE consultant_slides (
                id INT IDENTITY(1,1) PRIMARY KEY,
                consultant_id INT FOREIGN KEY REFERENCES consultants(id),
                slide_id NVARCHAR(255),
                data NVARCHAR(MAX)
            )
        END
    ''')
    
    conn.commit()

def store_consultant_info(conn, consultant_info):
    """Store consultant information in the database and return the new consultant ID."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consultants (name, title, mobile, location, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        consultant_info.get('name', ''),
        consultant_info.get('title', ''),
        consultant_info.get('mobile', ''),
        consultant_info.get('location', ''),
        consultant_info.get('email', '')
    ))
    
    # Fetch the last inserted ID using SCOPE_IDENTITY()
    cursor.execute('SELECT SCOPE_IDENTITY()')
    consultant_id = cursor.fetchone()[0]
    
    conn.commit()
    return consultant_id

def store_slide_data(conn, consultant_id, slides_data):
    """Store slide data linked to a consultant ID in the database."""
    cursor = conn.cursor()
    for slide in slides_data:
        cursor.execute('''
            INSERT INTO consultant_slides (consultant_id, slide_id, data)
            VALUES (?, ?, ?)
        ''', (
            consultant_id,
            slide.get('slide_id', ''),
            slide.get('data', '')
        ))
    conn.commit()

def get_consultant_by_name(conn, name):
    """Retrieve consultant information by name."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM consultants WHERE name = ?', (name,))
    return cursor.fetchone()

def get_slides_by_consultant_id(conn, consultant_id):
    """Retrieve all slides linked to a consultant ID."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM consultant_slides WHERE consultant_id = ?', (consultant_id,))
    return cursor.fetchall()
