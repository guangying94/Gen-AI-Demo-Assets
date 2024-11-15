import pyodbc
import json
from dotenv import load_dotenv
import os
import datetime
from decimal import Decimal

load_dotenv()

def fetch_data_from_azure_sql(query, server, database, username, password):

    # Connect to Azure SQL Database
    conn = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        f'Server=tcp:{server},1433;'
        f'Database={database};'
        f'UID={username};'
        f'PWD={password};'
        'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    )
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