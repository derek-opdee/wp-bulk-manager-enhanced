#!/usr/bin/env python3
"""
Create stored procedures for WP Bulk Manager
"""

import mysql.connector
from mysql.connector import Error
import json
from pathlib import Path

# Load database configuration
config_path = Path(__file__).parent.parent / 'config' / 'database.json'
with open(config_path, 'r') as f:
    DB_CONFIG = json.load(f)['database']

def create_procedures():
    """Create stored procedures"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Creating stored procedures...")
        
        # Drop existing procedures first
        procedures = ['sp_add_site_with_key', 'sp_log_access', 'sp_log_change']
        for proc in procedures:
            try:
                cursor.execute(f"DROP PROCEDURE IF EXISTS {proc}")
            except:
                pass
        
        # Create sp_add_site_with_key
        cursor.execute("""
        CREATE PROCEDURE sp_add_site_with_key(
            IN p_name VARCHAR(100),
            IN p_url VARCHAR(255),
            IN p_api_key VARCHAR(255),
            IN p_description TEXT,
            IN p_ip_whitelist TEXT
        )
        BEGIN
            DECLARE v_site_id INT;
            
            START TRANSACTION;
            
            INSERT INTO sites (name, url, description) 
            VALUES (p_name, p_url, p_description);
            
            SET v_site_id = LAST_INSERT_ID();
            
            INSERT INTO api_keys (site_id, api_key, key_name, ip_whitelist)
            VALUES (v_site_id, p_api_key, CONCAT(p_name, ' - Primary Key'), p_ip_whitelist);
            
            COMMIT;
            
            SELECT v_site_id as site_id;
        END
        """)
        print("✅ Created sp_add_site_with_key")
        
        # Create sp_log_access
        cursor.execute("""
        CREATE PROCEDURE sp_log_access(
            IN p_site_id INT,
            IN p_api_key VARCHAR(255),
            IN p_endpoint VARCHAR(255),
            IN p_method VARCHAR(10),
            IN p_ip_address VARCHAR(45),
            IN p_response_code INT,
            IN p_response_time_ms INT
        )
        BEGIN
            DECLARE v_api_key_id INT;
            
            SELECT id INTO v_api_key_id
            FROM api_keys
            WHERE site_id = p_site_id AND api_key = p_api_key AND is_active = TRUE
            LIMIT 1;
            
            INSERT INTO access_logs (
                site_id, api_key_id, endpoint, method, 
                ip_address, response_code, response_time_ms
            ) VALUES (
                p_site_id, v_api_key_id, p_endpoint, p_method,
                p_ip_address, p_response_code, p_response_time_ms
            );
            
            IF v_api_key_id IS NOT NULL THEN
                UPDATE api_keys 
                SET last_used_at = CURRENT_TIMESTAMP 
                WHERE id = v_api_key_id;
            END IF;
        END
        """)
        print("✅ Created sp_log_access")
        
        # Create sp_log_change
        cursor.execute("""
        CREATE PROCEDURE sp_log_change(
            IN p_site_id INT,
            IN p_content_type VARCHAR(50),
            IN p_content_id INT,
            IN p_action VARCHAR(50),
            IN p_field_name VARCHAR(100),
            IN p_old_value LONGTEXT,
            IN p_new_value LONGTEXT,
            IN p_summary TEXT,
            IN p_api_key_id INT,
            IN p_batch_id VARCHAR(36)
        )
        BEGIN
            INSERT INTO changes (
                site_id, content_type, content_id, action,
                field_name, old_value, new_value, change_summary,
                api_key_id, batch_id
            ) VALUES (
                p_site_id, p_content_type, p_content_id, p_action,
                p_field_name, p_old_value, p_new_value, p_summary,
                p_api_key_id, p_batch_id
            );
        END
        """)
        print("✅ Created sp_log_change")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ All stored procedures created successfully!")
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_procedures()