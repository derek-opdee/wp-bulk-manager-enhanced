#!/usr/bin/env python3
"""Fix database issues and set up properly"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'VXG4qwm2zqz0ydr-jxz',
    'database': 'opdee-bulk-manager'
}

def setup_database():
    try:
        # First connect without database
        config = DB_CONFIG.copy()
        db_name = config.pop('database')
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        cursor.execute(f"USE `{db_name}`")
        print(f"✅ Using database: {db_name}")
        
        # Create sites table first
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                url VARCHAR(255) NOT NULL,
                description TEXT,
                status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
                brand_voice TEXT COMMENT 'Brand voice and tonality guidelines',
                brand_guidelines JSON COMMENT 'Detailed brand guidelines',
                folder_path VARCHAR(500) COMMENT 'Local folder path for site-specific files',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created sites table")
        
        # Create API keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site_id INT NOT NULL,
                api_key VARCHAR(255) NOT NULL,
                key_name VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                ip_whitelist TEXT COMMENT 'Comma-separated IP addresses or CIDR ranges',
                permissions JSON COMMENT 'JSON array of allowed operations',
                last_used_at TIMESTAMP NULL,
                expires_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                INDEX idx_site_id (site_id),
                INDEX idx_api_key (api_key),
                INDEX idx_is_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created api_keys table")
        
        # Run the rest of schema from file
        with open('database/schema.sql', 'r') as f:
            schema = f.read()
            
        # Skip the CREATE DATABASE and USE statements
        schema_lines = schema.split('\n')
        in_table_def = False
        current_statement = []
        
        for line in schema_lines:
            line = line.strip()
            if line.startswith('CREATE DATABASE') or line.startswith('USE'):
                continue
            if line.startswith('CREATE TABLE'):
                in_table_def = True
                current_statement = [line]
            elif in_table_def:
                current_statement.append(line)
                if line.endswith(';'):
                    try:
                        statement = '\n'.join(current_statement)
                        if 'sites' not in statement and 'api_keys' not in statement:
                            cursor.execute(statement)
                            print(f"✅ Executed: {statement[:50]}...")
                    except Error as e:
                        if 'already exists' not in str(e):
                            print(f"⚠️  Warning: {e}")
                    in_table_def = False
                    current_statement = []
        
        # Now apply the updates
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site_id INT NOT NULL,
                template_name VARCHAR(200) NOT NULL,
                template_type VARCHAR(50) NOT NULL,
                template_content LONGTEXT NOT NULL,
                template_metadata JSON,
                is_active BOOLEAN DEFAULT TRUE,
                usage_count INT DEFAULT 0,
                last_used_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                INDEX idx_site_id (site_id),
                INDEX idx_template_type (template_type),
                UNIQUE KEY uk_site_template (site_id, template_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created templates table")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS branded_agent_kit (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site_id INT NOT NULL UNIQUE,
                brand_personality TEXT,
                tone_attributes JSON,
                writing_style TEXT,
                vocabulary_preferences TEXT,
                vocabulary_avoid TEXT,
                target_audience JSON,
                customer_pain_points TEXT,
                value_propositions TEXT,
                content_themes JSON,
                content_pillars JSON,
                hashtag_strategy TEXT,
                brand_colors JSON,
                typography JSON,
                logo_guidelines TEXT,
                imagery_style TEXT,
                tagline VARCHAR(500),
                elevator_pitch TEXT,
                mission_statement TEXT,
                unique_selling_points JSON,
                primary_keywords JSON,
                secondary_keywords JSON,
                local_keywords JSON,
                example_headlines JSON,
                example_descriptions JSON,
                email_templates JSON,
                compliance_requirements TEXT,
                disclaimer_text TEXT,
                copyright_notice VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                INDEX idx_site_id (site_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created branded_agent_kit table")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup completed!")
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_database()