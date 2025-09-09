#!/usr/bin/env python3
"""
Apply database updates for templates and branded agent kit
"""

import mysql.connector
from mysql.connector import Error
import json
from pathlib import Path

# Load database configuration
config_path = Path(__file__).parent.parent / 'config' / 'database.json'
with open(config_path, 'r') as f:
    DB_CONFIG = json.load(f)['database']

def apply_updates():
    """Apply schema updates"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("🚀 Applying database updates...")
        
        # Add columns to sites table
        try:
            cursor.execute("""
                ALTER TABLE sites 
                ADD COLUMN IF NOT EXISTS brand_voice TEXT COMMENT 'Brand voice and tonality guidelines',
                ADD COLUMN IF NOT EXISTS brand_guidelines JSON COMMENT 'Detailed brand guidelines including colors, fonts, messaging',
                ADD COLUMN IF NOT EXISTS folder_path VARCHAR(500) COMMENT 'Local folder path for site-specific files'
            """)
            print("✅ Updated sites table with branding columns")
        except Error as e:
            print(f"⚠️  Sites table update: {e}")
        
        # Create templates table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS templates (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    site_id INT NOT NULL,
                    template_name VARCHAR(200) NOT NULL,
                    template_type VARCHAR(50) NOT NULL COMMENT 'page, post, product, email, etc',
                    template_content LONGTEXT NOT NULL,
                    template_metadata JSON COMMENT 'Variables, placeholders, instructions',
                    is_active BOOLEAN DEFAULT TRUE,
                    usage_count INT DEFAULT 0,
                    last_used_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                    INDEX idx_site_id (site_id),
                    INDEX idx_template_type (template_type),
                    INDEX idx_is_active (is_active),
                    UNIQUE KEY uk_site_template (site_id, template_name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Created templates table")
        except Error as e:
            print(f"⚠️  Templates table: {e}")
        
        # Create branded_agent_kit table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS branded_agent_kit (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    site_id INT NOT NULL UNIQUE,
                    
                    -- Brand Voice & Tone
                    brand_personality TEXT COMMENT 'Overall brand personality description',
                    tone_attributes JSON COMMENT 'Array of tone attributes (professional, friendly, etc)',
                    writing_style TEXT COMMENT 'Detailed writing style guidelines',
                    vocabulary_preferences TEXT COMMENT 'Preferred words, phrases, terminology',
                    vocabulary_avoid TEXT COMMENT 'Words and phrases to avoid',
                    
                    -- Target Audience
                    target_audience JSON COMMENT 'Detailed target audience profiles',
                    customer_pain_points TEXT COMMENT 'Key customer pain points to address',
                    value_propositions TEXT COMMENT 'Core value propositions',
                    
                    -- Content Guidelines
                    content_themes JSON COMMENT 'Key content themes and topics',
                    content_pillars JSON COMMENT 'Content pillar categories',
                    hashtag_strategy TEXT COMMENT 'Hashtag usage guidelines',
                    
                    -- Visual Brand
                    brand_colors JSON COMMENT 'Primary, secondary, accent colors with hex codes',
                    typography JSON COMMENT 'Font families, sizes, hierarchy',
                    logo_guidelines TEXT COMMENT 'Logo usage rules',
                    imagery_style TEXT COMMENT 'Photography and illustration style guidelines',
                    
                    -- Messaging Framework
                    tagline VARCHAR(500) COMMENT 'Brand tagline',
                    elevator_pitch TEXT COMMENT '30-second elevator pitch',
                    mission_statement TEXT COMMENT 'Company mission statement',
                    unique_selling_points JSON COMMENT 'Array of USPs',
                    
                    -- SEO & Keywords
                    primary_keywords JSON COMMENT 'Primary SEO keywords',
                    secondary_keywords JSON COMMENT 'Secondary SEO keywords',
                    local_keywords JSON COMMENT 'Location-based keywords',
                    
                    -- Examples & Templates
                    example_headlines JSON COMMENT 'Example headlines in brand voice',
                    example_descriptions JSON COMMENT 'Example descriptions/paragraphs',
                    email_templates JSON COMMENT 'Email signature and template guidelines',
                    
                    -- Compliance & Legal
                    compliance_requirements TEXT COMMENT 'Industry compliance requirements',
                    disclaimer_text TEXT COMMENT 'Standard disclaimers',
                    copyright_notice VARCHAR(500) COMMENT 'Copyright notice format',
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                    INDEX idx_site_id (site_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Created branded_agent_kit table")
        except Error as e:
            print(f"⚠️  Branded agent kit table: {e}")
        
        # Create template_usage table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS template_usage (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    template_id INT NOT NULL,
                    site_id INT NOT NULL,
                    content_type VARCHAR(50) NOT NULL,
                    content_id INT,
                    variables_used JSON COMMENT 'Template variables and their values',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
                    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                    INDEX idx_template_id (template_id),
                    INDEX idx_site_id (site_id),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Created template_usage table")
        except Error as e:
            print(f"⚠️  Template usage table: {e}")
        
        # Add sample template for existing sites
        try:
            cursor.execute("""
                INSERT IGNORE INTO templates (site_id, template_name, template_type, template_content, template_metadata)
                SELECT 
                    id, 
                    'Newsletter Signup Page', 
                    'page',
                    '<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">{headline}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{introduction}</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="newsletter-form">
    {signup_form}
</div>
<!-- /wp:html -->',
                    JSON_OBJECT(
                        'variables', JSON_ARRAY('headline', 'introduction', 'signup_form'),
                        'description', 'Standard newsletter signup page template'
                    )
                FROM sites
            """)
            print("✅ Added sample templates")
        except Error as e:
            print(f"⚠️  Sample templates: {e}")
        
        # Initialize branded agent kit for existing sites
        try:
            cursor.execute("""
                INSERT IGNORE INTO branded_agent_kit (site_id, brand_personality)
                SELECT id, 'Professional and informative brand voice'
                FROM sites
            """)
            print("✅ Initialized branded agent kit for existing sites")
        except Error as e:
            print(f"⚠️  Branded agent kit initialization: {e}")
        
        connection.commit()
        print("\n✅ Database updates completed successfully!")
        
        # Show current tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\n📊 Current tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_updates()