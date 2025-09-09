"""
MySQL Database Manager for WP Bulk Manager
"""

import os
import json
import mysql.connector
from mysql.connector import Error, pooling
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import uuid
from contextlib import contextmanager

from ..utils.logger import get_logger

logger = get_logger(__name__)


class MySQLManager:
    """MySQL database manager with connection pooling"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize database manager"""
        self.config = self._load_config(config_path)
        self.pool = self._create_pool()
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load database configuration"""
        if config_path:
            with open(config_path, 'r') as f:
                return json.load(f)['database']
        
        # Try to load from default location
        default_path = Path(__file__).parent.parent.parent / 'config' / 'database.json'
        if default_path.exists():
            with open(default_path, 'r') as f:
                return json.load(f)['database']
        
        # Fall back to environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'database': os.getenv('DB_DATABASE', 'opdee-bulk-manager'),
            'user': os.getenv('DB_USERNAME', 'root'),
            'password': os.getenv('DB_PASSWORD', 'VXG4qwm2zqz0ydr-jxz')
        }
    
    def _create_pool(self) -> pooling.MySQLConnectionPool:
        """Create connection pool"""
        try:
            return pooling.MySQLConnectionPool(
                pool_name="wpbm_pool",
                pool_size=5,
                pool_reset_session=True,
                **self.config
            )
        except Error as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool"""
        connection = None
        try:
            connection = self.pool.get_connection()
            yield connection
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    # Site Management Methods
    
    def add_site(self, name: str, url: str, api_key: str, 
                 description: Optional[str] = None,
                 ip_whitelist: Optional[str] = None) -> Optional[int]:
        """Add a new site with API key"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if site already exists
                cursor.execute("SELECT id FROM sites WHERE name = %s", (name,))
                if cursor.fetchone():
                    logger.warning(f"Site '{name}' already exists")
                    return None
                
                # Use stored procedure
                cursor.callproc('sp_add_site_with_key', 
                               [name, url, api_key, description, ip_whitelist])
                
                # Get the site ID from the result
                for result in cursor.stored_results():
                    site_id = result.fetchone()[0]
                    
                conn.commit()
                logger.info(f"Added site '{name}' with ID {site_id}")
                return site_id
                
        except Error as e:
            logger.error(f"Error adding site: {e}")
            return None
    
    def get_site(self, name: str) -> Optional[Dict]:
        """Get site by name"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT s.*, ak.api_key, ak.ip_whitelist
                    FROM sites s
                    LEFT JOIN api_keys ak ON s.id = ak.site_id AND ak.is_active = TRUE
                    WHERE s.name = %s
                    LIMIT 1
                """, (name,))
                return cursor.fetchone()
        except Error as e:
            logger.error(f"Error getting site: {e}")
            return None
    
    def list_sites(self, status: Optional[str] = None) -> List[Dict]:
        """List all sites"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                if status:
                    cursor.execute("""
                        SELECT * FROM v_active_sites WHERE status = %s
                    """, (status,))
                else:
                    cursor.execute("SELECT * FROM v_active_sites")
                
                return cursor.fetchall()
        except Error as e:
            logger.error(f"Error listing sites: {e}")
            return []
    
    def update_site(self, site_id: int, **kwargs) -> bool:
        """Update site information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build update query
                updates = []
                values = []
                for key, value in kwargs.items():
                    if key in ['name', 'url', 'description', 'status']:
                        updates.append(f"{key} = %s")
                        values.append(value)
                
                if not updates:
                    return False
                
                values.append(site_id)
                query = f"UPDATE sites SET {', '.join(updates)} WHERE id = %s"
                
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Error as e:
            logger.error(f"Error updating site: {e}")
            return False
    
    def delete_site(self, name: str) -> bool:
        """Delete a site (cascades to related records)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sites WHERE name = %s", (name,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error deleting site: {e}")
            return False
    
    # API Key Management
    
    def add_api_key(self, site_id: int, api_key: str, 
                    key_name: Optional[str] = None,
                    ip_whitelist: Optional[str] = None) -> Optional[int]:
        """Add API key for a site"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO api_keys (site_id, api_key, key_name, ip_whitelist)
                    VALUES (%s, %s, %s, %s)
                """, (site_id, api_key, key_name, ip_whitelist))
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            logger.error(f"Error adding API key: {e}")
            return None
    
    def update_api_key(self, key_id: int, **kwargs) -> bool:
        """Update API key"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                updates = []
                values = []
                for key, value in kwargs.items():
                    if key in ['api_key', 'key_name', 'ip_whitelist', 'is_active', 'expires_at']:
                        updates.append(f"{key} = %s")
                        values.append(value)
                
                if not updates:
                    return False
                
                values.append(key_id)
                query = f"UPDATE api_keys SET {', '.join(updates)} WHERE id = %s"
                
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Error as e:
            logger.error(f"Error updating API key: {e}")
            return False
    
    def get_api_keys(self, site_id: int) -> List[Dict]:
        """Get all API keys for a site"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT * FROM api_keys 
                    WHERE site_id = %s 
                    ORDER BY created_at DESC
                """, (site_id,))
                return cursor.fetchall()
        except Error as e:
            logger.error(f"Error getting API keys: {e}")
            return []
    
    # Access Logging
    
    def log_access(self, site_id: int, api_key: str, endpoint: str,
                   method: str, ip_address: Optional[str] = None,
                   response_code: Optional[int] = None,
                   response_time_ms: Optional[int] = None,
                   error_message: Optional[str] = None) -> None:
        """Log API access"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if response_code and response_time_ms and not error_message:
                    # Use stored procedure for successful requests
                    cursor.callproc('sp_log_access',
                                   [site_id, api_key, endpoint, method,
                                    ip_address, response_code, response_time_ms])
                else:
                    # Direct insert for errors or incomplete data
                    cursor.execute("""
                        INSERT INTO access_logs 
                        (site_id, endpoint, method, ip_address, 
                         response_code, response_time_ms, error_message)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (site_id, endpoint, method, ip_address,
                          response_code, response_time_ms, error_message))
                
                conn.commit()
                
        except Error as e:
            logger.error(f"Error logging access: {e}")
    
    def get_access_logs(self, site_id: int, limit: int = 100,
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> List[Dict]:
        """Get access logs for a site"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                    SELECT * FROM access_logs 
                    WHERE site_id = %s
                """
                params = [site_id]
                
                if start_date:
                    query += " AND created_at >= %s"
                    params.append(start_date)
                
                if end_date:
                    query += " AND created_at <= %s"
                    params.append(end_date)
                
                query += " ORDER BY created_at DESC LIMIT %s"
                params.append(limit)
                
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Error as e:
            logger.error(f"Error getting access logs: {e}")
            return []
    
    # Change Tracking
    
    def log_change(self, site_id: int, content_type: str, content_id: int,
                   action: str, field_name: Optional[str] = None,
                   old_value: Optional[str] = None, new_value: Optional[str] = None,
                   summary: Optional[str] = None, api_key_id: Optional[int] = None,
                   batch_id: Optional[str] = None) -> None:
        """Log a content change"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                batch_id = batch_id or str(uuid.uuid4())
                
                cursor.callproc('sp_log_change',
                               [site_id, content_type, content_id, action,
                                field_name, old_value, new_value, summary,
                                api_key_id, batch_id])
                
                conn.commit()
                
        except Error as e:
            logger.error(f"Error logging change: {e}")
    
    def get_changes(self, site_id: int, content_type: Optional[str] = None,
                    limit: int = 100) -> List[Dict]:
        """Get change history"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = "SELECT * FROM changes WHERE site_id = %s"
                params = [site_id]
                
                if content_type:
                    query += " AND content_type = %s"
                    params.append(content_type)
                
                query += " ORDER BY created_at DESC LIMIT %s"
                params.append(limit)
                
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Error as e:
            logger.error(f"Error getting changes: {e}")
            return []
    
    # Plugin Operations
    
    def log_plugin_operation(self, site_id: int, plugin_slug: str,
                            plugin_name: str, operation: str,
                            version_from: Optional[str] = None,
                            version_to: Optional[str] = None,
                            status: str = 'pending',
                            error_message: Optional[str] = None,
                            api_key_id: Optional[int] = None) -> Optional[int]:
        """Log plugin operation"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO plugin_operations 
                    (site_id, plugin_slug, plugin_name, operation,
                     version_from, version_to, status, error_message, api_key_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (site_id, plugin_slug, plugin_name, operation,
                      version_from, version_to, status, error_message, api_key_id))
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            logger.error(f"Error logging plugin operation: {e}")
            return None
    
    def update_plugin_operation(self, operation_id: int, status: str,
                               error_message: Optional[str] = None) -> bool:
        """Update plugin operation status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE plugin_operations 
                    SET status = %s, error_message = %s
                    WHERE id = %s
                """, (status, error_message, operation_id))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error updating plugin operation: {e}")
            return False
    
    # SEO Changes
    
    def log_seo_change(self, site_id: int, page_id: int, page_url: str,
                       field_type: str, old_value: Optional[str] = None,
                       new_value: Optional[str] = None,
                       api_key_id: Optional[int] = None) -> None:
        """Log SEO change"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO seo_changes 
                    (site_id, page_id, page_url, field_type,
                     old_value, new_value, api_key_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (site_id, page_id, page_url, field_type,
                      old_value, new_value, api_key_id))
                conn.commit()
        except Error as e:
            logger.error(f"Error logging SEO change: {e}")
    
    # Statistics and Reports
    
    def get_site_statistics(self, site_id: int) -> Dict:
        """Get site statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT * FROM v_site_statistics WHERE id = %s
                """, (site_id,))
                return cursor.fetchone() or {}
        except Error as e:
            logger.error(f"Error getting site statistics: {e}")
            return {}
    
    def get_recent_activity(self, limit: int = 100) -> List[Dict]:
        """Get recent activity across all sites"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(f"""
                    SELECT * FROM v_recent_activity LIMIT %s
                """, (limit,))
                return cursor.fetchall()
        except Error as e:
            logger.error(f"Error getting recent activity: {e}")
            return []
    
    # Backup Management
    
    def create_backup_record(self, site_id: int, backup_type: str,
                            backup_location: str, backup_size: int,
                            items_count: int) -> Optional[int]:
        """Create backup record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO backup_history 
                    (site_id, backup_type, backup_location, backup_size,
                     items_count, status, started_at)
                    VALUES (%s, %s, %s, %s, %s, 'in_progress', NOW())
                """, (site_id, backup_type, backup_location, 
                      backup_size, items_count))
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            logger.error(f"Error creating backup record: {e}")
            return None
    
    def update_backup_status(self, backup_id: int, status: str,
                            error_message: Optional[str] = None) -> bool:
        """Update backup status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if status == 'completed':
                    cursor.execute("""
                        UPDATE backup_history 
                        SET status = %s, completed_at = NOW()
                        WHERE id = %s
                    """, (status, backup_id))
                else:
                    cursor.execute("""
                        UPDATE backup_history 
                        SET status = %s, error_message = %s
                        WHERE id = %s
                    """, (status, error_message, backup_id))
                
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error updating backup status: {e}")
            return False