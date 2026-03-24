import sqlite3
import logging
from tabulate import tabulate
import re

logger = logging.getLogger("storage")

VALID_OPERATORS = {"=", ">", "<", ">=", "<=", "!=", "LIKE", "IN", "NOT IN", "IS NULL", "IS NOT NULL"}
NAME_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

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
        
        col_defs = ", ".join(
            f"{col} {col_type}" for col, col_type in columns.items() 
        )
        sql_query = f"""CREATE TABLE IF NOT EXISTS {table_name} 
                        ({col_defs})
                    """
        try:
            with self._connect() as conn:
                conn.execute(sql_query)
                
            logger.info("Table '%s' created successfully", table_name)
            
        except Exception:
            logger.exception("Cannot create table '%s'", table_name)       
            
    def append(
        self,
        table_name,
        data: dict,
        ):
        """Insert a row into the specified table

        Args:
            table_name (str): Target table name
            data (dict): 
        """
        
        
        columns_str = ", ".join(data.keys())
        placeholder = ", ".join(["?"]*len(data))
        
        query = f"""INSERT OR IGNORE INTO {table_name} 
                    ({columns_str})
                    VALUES({placeholder})
                """
        try:
            
            with self._connect() as conn:
                conn.execute(query, tuple(data.values()))
            
        except Exception:
            logger.exception("Error when append data into '%s' table", table_name)
    
    def insert_many(self, table_name:str, data_list: list[dict]):
        """Insert many data into table

        Args:
            table_name (str): The target table name
            data_list (list[dict]): List of data dictionaries
        """
        if not data_list:
            return
        columns = ", ".join(data_list[0].keys())
        placeholders = ", ".join(['?']*len(data_list[0]))
        
        query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Covert list[dict] to list[tupple] for use with executemany
        params = [tuple(d.values()) for d in data_list]
        
        try:
            with self._connect() as conn:
                conn.executemany(query, params)
            
            logger.info("Inserted %d rows into %s", len(data_list), table_name)
        
        except Exception:
            logger.exception("Error inserting many into %s", table_name)
            
        
    def upsert(self, table_name: str, data:dict, conflict: str):
        """ Insert a row into the table, update it  if a conflict occurs
        
        Args:
            table_name (str): Target table name.
            data (dict): Column-value mapping for the row.
            conflict (str): Column name used as the conflict target
                (usually a PRIMARY KEY or UNIQUE column)
        """
                
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"]*len(data))
        
        update_sql = ", ".join(
            f"{col} = excluded.{col}" for col in data.keys() if col != conflict
        )
        
        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT({conflict})
            DO UPDATE SET ({update_sql})
        """
        
        try:
            with self._connect() as conn:
                conn.execute(query, tuple(data.values()))
        
        except Exception:
            logger.exception("Error upserting into '%s'", table_name)
    
    def upsert_many(self, table_name: str, data_list:list[dict], conflict: str):
        """Update or insert many rows

        Args:
            table_name (str): The target table name
            data_list (list[dict]): List of data dictionaries
            conflict (str): Column name used as the conflict target
                (usually a PRIMARY KEY or UNIQUE column)
        """
        if not data_list:
            return
        
        columns = ", ".join(data_list[0].keys())
        placeholders = ", ".join(["?"] * len(data_list[0]))
        
        update_sql = ", ".join(
            f"{col} = execlude{col}" for col in data_list[0].keys if col != conflict
        )
        
        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT ({conflict})
            DO UPDATE SET ({update_sql})            
        """
        
        params = [tuple(d.values()) for d in data_list]
        try:
            with self._connect() as conn:
                conn.executemany(query, params)
            logger.info("Upserted %d rows into %s", len(data_list), table_name)
        except Exception:
            logger.exception("Error upserting many into '%s'", table_name)
          
    def select(
        self,
        table_name: str,
        columns:list[str] | None = None,
        filters:dict |None = None,
        order_by: str| None = None,
        order: str = "ASC",
        limit: int| None = None,
        ):
        """Select data of columns from the table 
        
        Args:
            table_name (str): Target table name,
            columns (list[str]): List columns to retrieve data,
            filters (dict): Conditions to retrieve data,
            order_by (str): Column name to order
            order (str): DESC or ASC, default ASC 
            limit (int): Number of rows to retrieve,
            offset (int): Number of rows to skip
        """    
        
        if not self._is_valid_name(table_name):
            raise ValueError("The table name is incorrect")
        
        columns_str = ""
        if columns is not None:
            for col in columns:  
                if not self._is_valid_name(col):
                    raise ValueError("The column name is incorrect")
            columns_str = ", ".join(columns)
        else:
            columns_str = "*"
        
        query = f"SELECT {columns_str} FROM {table_name}"
        params = []
        
        if filters:
            where_sql, where_param = self._parse_logic(filters)
            query += f" WHERE {where_sql}"
            params.extend(where_param)
        
        if order_by:
            query += f" ORDER BY {order_by}"
            if order.upper() in ["ASC", "DESC"]:
                query += f" {order.upper()}" 
            
        if limit:
            query += " LIMIT ?"
            params.append(limit)           
        
        try:
            with self._connect() as conn:
                rows = conn.execute(query, params).fetchall()

                return self._format_rows(rows)    
            
        except Exception:
            logger.exception("Error retrieving data from table '%s'", table_name)
            raise

    
    def update(
        self,
        table_name: str,
        data: dict,
        filters: dict,
        ):
        """Update values for the column of a table

        Args:
            table_name (str): Target table name
            data (dict): key is column and value is new value of that column
            filters (dict): Key is column and value is conditions of that column
                Example:
                table_name = "Employee"
                data = {
                    "department": "Data Engineer",
                    "salary": 1500,
                }
                filters = {
                    "first_name": "David",
                    "last_name": "Cameroon",
                }
            query = {
                UPDATE {table_name}
                SET department = "Data Engineer", salary = 1500
                WHERE first_name = ? AND last_name = ?, (David, Cameroon)
            }
        """
        query = f"UPDATE {table_name}"
        set_sql = []
        params = []
        if isinstance(data, dict):
            for col, val in data.items():
                set_sql.append(f"{col} = ?")
                params.append(val)

            query += " SET " + ", ".join(set_sql)
            
        if filters:
            where_sql, where_param = self._parse_logic(filters)
            query += f" WHERE {where_sql}"
            params.extend(where_param)        
        try:
            with self._connect() as conn:
                conn.execute(query, tuple(params))
                
            logger.info("Data updated successfully!")
            
        except Exception:
            logger.exception("Error updating for '%s'", table_name)
             
    def delete(self,
               table_name,
               filters: dict,
               ):
        """Delete rows in a table

        Args:
            table_name (str): Target table name
            filter (dict): Filter is a dict containing conditions to delete rows in the table
                Example:
                    table_name = "Employee",
                    filter = {
                        "first_name": "David",
                        "salary": ("<=", 1000),
                    }
        """
        
        query = f"DELETE FROM {table_name}"
        
        if not isinstance(filters, dict):
            raise ValueError(f"Filter is a dict")
        
        where_sql, where_param = self._parse_logic(filters)
        query += f" WHERE {where_sql}"    

        
        try:
            with self._connect() as conn:
                conn.execute(query, tuple(where_param))
            
            logger.info("Successfully deleted rows from table '%s' where '%s'", table_name, filters)
        except Exception:
            logger.exception("Error deleting rows of '%s'", table_name)  
                
    def count(
        self,
        table_name:str,
        columns:list[str] | None=None,
        filters:dict|None = None,
        order_by: str| None = None,
        order: str | None = None,
        limit: int | None = None):
        """Count rows optionally grouped by columns.

        Args:
            table_name (str): Target table name
            columns (list[str]): List columns name
            filter (dict): Where to count
        """
        if not self._is_valid_name(table_name):
            raise ValueError("The table name is incorrect")
        
        col_str = ""
        one = True
        if columns is not None:
            
            for col in columns:
                if not self._is_valid_name(col):
                    raise ValueError("The columns name is incorrect")
            
            col_str = ", ".join(columns)
            
        query = f"SELECT {col_str + ', ' if col_str else ''}COUNT(*) FROM {table_name}"
        
        params = []
        if filters:
            where_sql, where_params = self._parse_logic(filters)
            query += f" WHERE {where_sql}"
            params.extend(where_params)
        
        if col_str:
            one = False
            query += f" GROUP BY {col_str}"
            
        if order_by:
            query += f" ORDER BY {order_by}"
            if order.upper() in ["ASC", "DESC"]:
                query += f" {order.upper()}"
            
        if limit:
            query += f" LIMIT {limit}"
      
        try:
            with self._connect() as conn:
                rows = conn.execute(query, params).fetchall()
                return self._format_rows(rows, one=one)
        
        except Exception:
            logger.exception("Error when count '%s' of '%s' ", columns, table_name)
    
    def first(self, table_name:str, columns:list[str] | None = None, filters:dict | None = None):
        """ Get the first of required data

        Args:
            table_name (str): Target table name
            columns (list[str] | None, optional): List columns name is required.Defaults to None.
            filters (dict {key: (operator, value)}): Conditions to retrieve data. Defaults to None.
        """
        rows = self.select(table_name, columns, filters, limit=1)
        return self._format_rows(rows=rows, one=True)
    
    def exists(self, table_name: str, filters:dict):
        """Check exists of data

        Args:
            table_name (str): Target table name
            filters (dict {key: (operator, value)}): filter for where
        """
        where_sql, where_params = self._parse_logic(filters)
        
        sql =f"""
            SELECT 1
            FROM {table_name}
            WHERE {where_sql}
            LIMIT 1
        """
        
        try:
            with self._connect() as conn:
                cur = conn.execute(sql, where_params)
                return cur.fetchone() is not None
            
        except Exception:
            logger.exception("Error get data with where '%s'", filters)
    
    def tables(self):
        """ Get list all tables in database
        """
        try:
            with self._connect() as conn:
                tables = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                return self._format_rows(rows=tables)
        except Exception:
            logger.exception("Error when get list all tables")
    
    def schema(self, table_name):
        "Get schema of a table"
        with self._connect() as conn:
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            rows = cursor.fetchall()
            
            schema = {}
            for row in rows:
                name = row[1]
                schema[name] = {
                    "type": row[2],
                    "notnull": row[3],
                    "default": row[4],
                    "pk": bool(row[5])
                }
            
            return schema
    
    def safe_query(self, query:str, show=False):
        conn = None
        try:
            conn = sqlite3.connect("file:data/scraper.db?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row 
            
            cursor = conn.cursor()
            cursor.execute(query)
            
            rows = cursor.fetchall()
                        
            result = [dict(r) for r in rows]
                        
            if show:
                result = self._format_numbers(result)
                print(tabulate(result, headers="keys", tablefmt="grid"))
            else:
                return result
        
        except sqlite3.OperationalError as e:
            logger.error("SQL error: %s", e)
            return None
        
        except Exception:
            logger.exception("Error when retrieving '%s'", query)
            return None
        
        finally:
            if conn:
                conn.close()
    
    def _format_numbers(self, rows):
        formatted = []
        
        for row in rows:
            row = dict(row)
            
            new_row = {}
            for k,v in row.items():
                if isinstance(v, int):
                    new_row[k] = f"{v:,}"
                else:
                    new_row[k] = v
            formatted.append(new_row)
        
        return formatted
    
    
    def _connect(self):
        # Return the connection, used with 'with' to automatically commit/rollback.
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _parse_logic(self, filters:dict):
    
        """Parse a nested filter dictionary into a SQL WHERE clause.

            The filter structure is a logical expression tree where each
            dictionary contains exactly one key:

            - column_name → ("operator", value)
            - "AND" / "OR" → list of sub-filter dictionaries

            Example:
                filters = {
                    "AND": [
                        {"age": (">", 18)},
                        {"role": ("=", "admin")}
                    ]
                }

            Returns:
                tuple[str, list]: SQL clause and parameters.
        """
        
        params = []
        for key, value in filters.items():
            if key in ["AND", "OR"]:
                
                operator = key
                sub_clauses = []
                
                for items in value:
                    clause, sub_param = self._parse_logic(items)
                    
                    sub_clauses.append(clause)
                    params.extend(sub_param)
                
                joined = f" {operator} ".join(sub_clauses)
                
                return f"({joined})", params
                    
                    
            else:
                return self._parse_compare({key: value})
                
    
    def _parse_compare(self, filter:dict):
        """
        Parse a single column condition into a SQL fragment.

        Args:
            filter (dict): Exactly one key-value pair where value is a tuple (operator, operand).
                Supported operators:
                    - ("=", value), ("!=", value), (">", value), ...
                    - ("IN", [v1, v2])        → "col IN (?, ?)"
                    - ("NOT IN", [v1, v2])    → "col NOT IN (?, ?)"
                    - ("BETWEEN", (v1, v2))   → "col BETWEEN ? AND ?"
                    - ("IS NULL", None)       → "col IS NULL"
                    - ("IS NOT NULL", None)   → "col IS NOT NULL"

        Returns:
            tuple[str, list]: SQL fragment string and list of bound parameters.

        Raises:
            ValueError: If filter has != 1 key, value is not a tuple,
                        operator is invalid, or operands are malformed.
        """

        if len(filter) != 1:
            raise ValueError("Filter must contain exactly one condition")
        col, val = next(iter(filter.items()))
        
        if not self._is_valid_name(col):
            raise ValueError("The column name is incorrect")
        
        if not isinstance(val, tuple):
            raise ValueError("Value must be a tuple, (operator, value)")
        
        op, value = val
        op = op.upper()
        if op not in VALID_OPERATORS:
            raise ValueError(f"Invalid operator. Allowed: {VALID_OPERATORS}")
        
        if op in ["IN", "NOT IN"]:
            if not value:
                raise ValueError("Value for IN must be a non-empty list or tuple")
            placeholder = ", ".join(["?"]* len(value))
            query = f"{col} {op} ({placeholder})"
            return query, list(value)
        
        elif op in ["IS NULL", "IS NOT NULL"]:
            query = f"{col} {op}"
            return query, []
        
        elif op == "BETWEEN":
            if not value or len(value) != 2:
                raise ValueError("BETWEEN requires exactly two values")
            query = f"{col} BETWEEN ? AND ?"
            return query, list(value)
            
        else:
            query = f"{col} {op} ?"
            return query, [value]
    
    def _format_rows(self, rows, col_names = None, one=False):
        if not rows:
            return None if one else []
        
        if col_names:
            result = [dict(zip(col_names,row)) for row in rows]
        else:
            result = [dict(row) for row in rows]
        return result[0] if one else result
        
    def _is_valid_name(self, name):
        return bool(NAME_PATTERN.fullmatch(name))
        
    