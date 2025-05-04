# Azure SQL MCP Server

This project implements a Model Context Protocol (MCP) server for Azure SQL using FastMCP. It provides tools to:

- Retrieve all tables and their schema from an Azure SQL database
- Execute arbitrary T-SQL queries and return results in JSON format

## Key Files
- `main.py`: Defines the MCP server and tools
- `utilities.py`: Handles Azure SQL authentication and data fetching

## Requirements
- Python 3.8+
- Azure credentials - Service Principal (uses `DefaultAzureCredential`)
- ODBC Driver 18 for SQL Server - Installation instructions can be found [here](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline)
- Required Python packages (see `requirements.txt`)

## Usage
1. Set environment variables for your Azure SQL server and database in a `.env` file:
   ```env
   AZURE_SQL_SERVER=your_server_name
   AZURE_SQL_DATABASE=your_database_name
   AZURE_CLIENT_ID=your_service_principal_id
   AZURE_CLIENT_SECRET=your_service_principal_secret
    AZURE_TENANT_ID=your_tenant_id
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python main.py
   ```

The server exposes tools for schema inspection and query execution, making it easy to integrate with MCP-compatible clients.
