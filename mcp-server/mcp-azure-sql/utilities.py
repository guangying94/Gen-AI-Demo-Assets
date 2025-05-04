import pyodbc, struct
import json
from dotenv import load_dotenv
import datetime
from decimal import Decimal
from azure.identity import DefaultAzureCredential

load_dotenv()

def fetch_data_from_azure_sql(query, server, database):

    # Use DefaultAzureCredential to get the token
    credential = DefaultAzureCredential()

    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256

    # Create the connection string
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch the data
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    # Convert rows to list of dicts and handle datetime objects
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if isinstance(value, datetime.datetime):
                row_dict[key] = value.isoformat()
        data.append(row_dict)

    # Convert to JSON array
    json_data = json.dumps(data, default=lambda x: float(x) if isinstance(x, Decimal) else x)

    # Close the connection
    cursor.close()
    conn.close()

    return json_data