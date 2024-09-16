# config.py

# Database configuration
DB_CONFIG = {
    'username': 'bridgeadmin',
    'password': '',
    'server': 'bridge-hackathon.database.windows.net',
    'database': 'Hackathon',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# Function to create the connection string
def get_db_connection_string():
    return f"mssql+pyodbc://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['server']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}"


API_Secret = ""
