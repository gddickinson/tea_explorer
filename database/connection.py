"""
Database Connection Management
Handles SQLite connections with proper resource management
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call


class DatabaseConnection(LoggerMixin):
    """Manages database connections with context manager support"""
    
    def __init__(self, db_path: Path, timeout: int = 30):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
            timeout: Connection timeout in seconds
        """
        self.db_path = Path(db_path)
        self.timeout = timeout
        self._connection: Optional[sqlite3.Connection] = None
        self.logger.info(f"Database manager initialized for: {self.db_path}")
    
    @log_method_call
    def connect(self) -> sqlite3.Connection:
        """
        Get database connection
        
        Returns:
            SQLite connection object
        """
        if self._connection is None:
            self.logger.debug(f"Opening database connection: {self.db_path}")
            self._connection = sqlite3.connect(
                str(self.db_path),
                timeout=self.timeout
            )
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def get_connection(self) -> sqlite3.Connection:
        """Get connection (alias for connect)"""
        return self.connect()
    
    @log_method_call
    def close(self):
        """Close database connection"""
        if self._connection:
            self.logger.debug(f"Closing database connection: {self.db_path}")
            self._connection.close()
            self._connection = None
    
    def __enter__(self):
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            self.logger.error(f"Database error: {exc_val}", exc_info=True)
            if self._connection:
                self._connection.rollback()
        self.close()
        return False
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions
        
        Usage:
            with db.transaction() as conn:
                conn.execute(...)
        """
        conn = self.connect()
        try:
            yield conn
            conn.commit()
            self.logger.debug("Transaction committed")
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Transaction rolled back: {e}", exc_info=True)
            raise
    
    def execute(self, query: str, parameters=None):
        """
        Execute a query
        
        Args:
            query: SQL query
            parameters: Query parameters
            
        Returns:
            Cursor object
        """
        conn = self.connect()
        if parameters:
            return conn.execute(query, parameters)
        return conn.execute(query)
    
    def execute_many(self, query: str, parameters_list):
        """
        Execute query with multiple parameter sets
        
        Args:
            query: SQL query
            parameters_list: List of parameter tuples
        """
        conn = self.connect()
        conn.executemany(query, parameters_list)
        conn.commit()
    
    def fetch_one(self, query: str, parameters=None):
        """Fetch single row"""
        cursor = self.execute(query, parameters)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, parameters=None):
        """Fetch all rows"""
        cursor = self.execute(query, parameters)
        return cursor.fetchall()
    
    def commit(self):
        """Commit current transaction"""
        if self._connection:
            self._connection.commit()
