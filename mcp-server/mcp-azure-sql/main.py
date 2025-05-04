# server.py
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
from utilities import fetch_data_from_azure_sql

load_dotenv()

AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")

# Create an MCP server
mcp = FastMCP("Azure SQL MCP Server")

@mcp.tool()
def get_table_schema() -> str:
    """
    Get all the tables and their schema from the azure sql database.
    """
    get_schema_query = """
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME,
                STRING_AGG(CONCAT(COLUMN_NAME, ' (', DATA_TYPE, ')'), ', ') AS COLUMNS
            FROM 
                INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA != 'sys'
            GROUP BY 
                TABLE_SCHEMA, TABLE_NAME
            ORDER BY 
                TABLE_SCHEMA, TABLE_NAME;
            """
    print("get_schema_query is executed") 
    return fetch_data_from_azure_sql(get_schema_query, AZURE_SQL_SERVER, AZURE_SQL_DATABASE)

@mcp.tool()
def execute_query(query: str) -> str:
    """
    Execute a T-SQL query to Azure SQL Database and return the results.
    
    Args:
        query: The SQL query to be executed
    Returns:
        A string containing the results of the query in JSON format
    """
    print("execute_query is executed with query: ", query) 
    return fetch_data_from_azure_sql(query, AZURE_SQL_SERVER, AZURE_SQL_DATABASE) 

if __name__ == "__main__":
    mcp.run(transport="sse")