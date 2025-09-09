#!/usr/bin/env python3
"""
Database setup script for WP Bulk Manager
Creates MySQL database and tables
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
import argparse
from pathlib import Path
import json

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USERNAME', 'root'),
    'password': os.getenv('DB_PASSWORD', 'VXG4qwm2zqz0ydr-jxz'),
    'database': os.getenv('DB_DATABASE', 'opdee-bulk-manager')
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database
        config = DB_CONFIG.copy()
        config.pop('database', None)
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        db_name = DB_CONFIG['database']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        print(f"✅ Database '{db_name}' created or already exists")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def run_schema():
    """Execute the schema SQL file"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Read schema file
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema commands separately
        for statement in schema_sql.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Error as e:
                    if 'already exists' not in str(e):
                        print(f"⚠️  Warning executing statement: {e}")
        
        connection.commit()
        print("✅ Database schema created successfully")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating schema: {e}")
        return False

def test_connection():
    """Test database connection and show table info"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Get table list
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n📊 Database Tables:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} records")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error testing connection: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Check if we already have data
        cursor.execute("SELECT COUNT(*) FROM sites")
        if cursor.fetchone()[0] > 0:
            print("ℹ️  Sample data already exists, skipping...")
            return True
        
        # Insert sample site
        cursor.execute("""
            INSERT INTO sites (name, url, description) 
            VALUES (%s, %s, %s)
        """, ('opdee', 'https://opdee.com', 'Opdee main website'))
        site_id = cursor.lastrowid
        
        # Insert API key
        cursor.execute("""
            INSERT INTO api_keys (site_id, api_key, key_name, ip_whitelist)
            VALUES (%s, %s, %s, %s)
        """, (site_id, '27013065aa24d225b5ea9db967d191f3', 'Opdee Primary Key', '202.62.150.192'))
        
        connection.commit()
        print("✅ Sample data inserted successfully")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def create_config_file():
    """Create a database configuration file"""
    config = {
        'database': {
            'host': DB_CONFIG['host'],
            'port': DB_CONFIG['port'],
            'database': DB_CONFIG['database'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password']
        }
    }
    
    config_path = Path(__file__).parent.parent / 'config' / 'database.json'
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Database configuration saved to: {config_path}")

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='Setup WP Bulk Manager database')
    parser.add_argument('--no-sample-data', action='store_true', 
                       help='Skip inserting sample data')
    parser.add_argument('--drop-existing', action='store_true',
                       help='Drop existing database before creating')
    args = parser.parse_args()
    
    print("🚀 WP Bulk Manager Database Setup")
    print("=" * 50)
    
    # Drop existing if requested
    if args.drop_existing:
        try:
            config = DB_CONFIG.copy()
            config.pop('database', None)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS `{DB_CONFIG['database']}`")
            connection.close()
            print("✅ Dropped existing database")
        except Error as e:
            print(f"⚠️  Could not drop database: {e}")
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Run schema
    if not run_schema():
        sys.exit(1)
    
    # Insert sample data
    if not args.no_sample_data:
        insert_sample_data()
    
    # Test connection
    test_connection()
    
    # Create config file
    create_config_file()
    
    print("\n✅ Database setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Update your WP Bulk Manager configuration to use MySQL")
    print("2. Run 'python wpbm_manager.py' to start using the application")
    print("3. Check config/database.json for database settings")

if __name__ == "__main__":
    main()