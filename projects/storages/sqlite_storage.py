import sqlite3
import logging

logger = logging.getLogger("storage")

class SQLiteStorage:
    def __init__(self, path:str):
        self.path = path
    
    def create_table(self, table_name: str, columns: dict[str, str] ):
        """ Create a new table dynamically.

        Args:
            table_name (str): Name of the table
            columns (dict[str, str]): Mapping of column names to their SQL definitions
                Example:
                {
                    "id": "TEXT PRIMARY KEY",
                    "name": "TEXT",
                    "age": "INTEGER"
                }
            
        """
        try:
            col_defs = ", ".join(
                f"{col} {col_type}" for col, col_type in columns.items() 
            )
            sql_query = f"""CREATE TABLE IF NOT EXISTS {table_name} 
                            ({col_defs})
                        """
            
            with self._connect() as conn:
                conn.execute(sql_query)
                
            logger.info("Table '%s' created successfully", table_name)
            
        except Exception:
            logger.exception("Cannot create table '%s'", {table_name})
            
    def _connect(self):
        # Return the connection, used with 'with' to automatically commit/rollback.
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn
    
            
    def append(
        self,
        table_name,
        columns:list[str],
        values: list | tuple):
        """Insert a row into the specified table

        Args:
            table_name (str): Target table name
            columns (list[str]): List of column names
            values (list | tuple): Values corresponding to the columns
        """
        if len(columns) != len(values):
            raise ValueError("Column and values length mismatch")
        
        columns_str = ", ".join(columns)
        placeholder = ", ".join(["?"]*len(columns))
        
        query = f"""INSERT OR IGNORE INTO {table_name} 
                    ({columns_str})
                    VALUES({placeholder})
                """
        try:
            
            with self._connect() as conn:
                conn.execute(query, values)
            
        
        except Exception:
            logger.exception("Error when append data into '%s' table", table_name)
            
            
    def select(
        self,
        table_name,
        columns: list[str] | None=None,
        where: str | None=None
        ):
        """Retrieve rows from a table with optional column selection and filtering.

        Args:
            table_name (str): Target table name
            columns (list[str]): Columns to retrieve, If None, all columns are selected.
        """
        if columns is not None:
            columns_str = ", ".join(columns)
        else:
            columns_str = "*"
        
        where_str = f"WHERE {where}" if where else ""
        
        query = f"""
            SELECT {columns_str}
            FROM {table_name}
            {where_str}
        """
        try:
            with self._connect() as conn:
                rows = conn.execute(query).fetchall()
            
            values = [dict(row) for row in rows]
            logger.info("Data retrieved successfully from the table '%s'",table_name)
            return values
            
        except Exception:
            logger.exception("Error retrieving data from table '%s'", table_name)
            raise
    
    def update(
        self,
        table_name,
        column,
        value,
        where):
        """Update values for the column of a table

        Args:
            table_name (str): Target table name
            column (str): Column is updated
            value: New value of column
            where (str): Condition of row are updated
                Example:
                table_name = "Jobs",
                column = "job_name",
                value = "Python",
                where = "id = '123' " 
        """
        query = f"""
                    UPDATE {table_name}
                    SET {column} = ?
                    WHERE {where}
                """
        try:
            with self._connect() as conn:
                conn.execute(query, (value,))
                
            logger.info("Data updated successfully!")
            
        except Exception:
            logger.exception("Error updating for '%s' of '%s'",column, table_name)
            
    def delete(self,
               table_name,
               where,
               ):
        """Delete rows in a table have 'where'

        Args:
            table_name (str): Target table name
            where (str): Condition rows need delete
                Example:
                    table_name = "Jobs",
                    where = "job_name = 'Backend Engineer' "
        """
        
        query = f"""
                    DELETE FROM {table_name}
                    WHERE {where}
                """
        try:
            with self._connect() as conn:
                conn.execute(query)
            
            logger.info("Successfully deleted rows from table '%s' where '%s'", table_name, where)
        except Exception:
            logger.exception("Error deleting rows of '%s'", table_name)
            