
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# --- 1. Load Environment Variables ---
print("--- Loading .env file ---")
# Construct the path to the .env file relative to this script
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
    print(".env file loaded successfully.")
else:
    print(f"Warning: .env file not found at {dotenv_path}. Using system environment variables.")

# --- 2. Read Connection Parameters ---
print("\n--- Reading Database Configuration ---")
sql_server_host = os.getenv("SQL_SERVER_HOST")
sql_server_port = os.getenv("SQL_SERVER_PORT", 1433)
sql_server_user = os.getenv("SQL_SERVER_USER")
sql_server_password = os.getenv("SQL_SERVER_PASSWORD")
sql_server_database = os.getenv("SQL_SERVER_DATABASE")
sql_server_encrypt = os.getenv("SQL_SERVER_ENCRYPT", 'false').lower() == 'true'
sql_server_trust_cert = os.getenv("SQL_SERVER_TRUST_SERVER_CERTIFICATE", 'true').lower() == 'true'

# --- Print loaded values for verification ---
print(f"Host: {sql_server_host}")
print(f"Port: {sql_server_port}")
print(f"User: {sql_server_user}")
print(f"Database: {sql_server_database}")
print(f"Encrypt: {sql_server_encrypt}")
print(f"Trust Server Certificate: {sql_server_trust_cert}")

# --- 3. Construct Connection String ---
print("\n--- Constructing Connection String ---")
if not all([sql_server_host, sql_server_user, sql_server_password, sql_server_database]):
    print("Error: One or more required database environment variables are missing.")
    exit()

encoded_password = quote_plus(sql_server_password)
driver = "ODBC Driver 18 for SQL Server".replace(' ', '+')
encrypt_param = 'yes' if sql_server_encrypt else 'no'
trust_cert_param = 'yes' if sql_server_trust_cert else 'no'

database_url = (
    f"mssql+pyodbc://{sql_server_user}:{encoded_password}@"
    f"{sql_server_host}:{sql_server_port}/{sql_server_database}?"
    f"driver={driver}&Encrypt={encrypt_param}&TrustServerCertificate={trust_cert_param}"
)

# Do not print the full URL to avoid exposing the password in logs
print("Connection string constructed (password hidden).")


# --- 4. Attempt Connection ---
print("\n--- Attempting to Connect to Database ---")
try:
    engine = create_engine(database_url, connect_args={"timeout": 5})
    with engine.connect() as connection:
        print("Successfully created a connection.")
        
        # --- 5. Execute a Simple Query ---
        print("--- Executing a simple query (SELECT 1) ---")
        result = connection.execute(text("SELECT 1"))
        for row in result:
            print(f"Query result: {row[0]}")
            if row[0] == 1:
                print("\n*** SUCCESS: Database connection and query execution were successful! ***")
            else:
                print("\n*** WARNING: Query executed but result was not as expected. ***")

except Exception as e:
    print(f"\n*** FAILURE: An error occurred while connecting or querying the database. ***")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Details: {e}")

