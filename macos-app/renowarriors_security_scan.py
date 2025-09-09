#!/usr/bin/env python3
"""
Comprehensive security scan and cleanup script for Reno Warriors WordPress site
Cloudways server: 170.64.179.157
"""

import subprocess
import datetime
import json

class RenoWarriorsSecurityScan:
    def __init__(self):
        self.ssh_host = "170.64.179.157"
        self.ssh_user = "master_ntuqvnephb"
        self.ssh_pass = "56tbztc2cRZ8"
        self.db_host = "localhost"
        self.db_port = "3307"
        self.db_name = "cfhbaxywhg"
        self.db_user = "cfhbaxywhg"
        self.db_pass = "7Sy28jzV25"
        self.wp_path = "applications/cfhbaxywhg/public_html"
        self.wp_prefix = "wpjk_"
        
        self.scan_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'malware_found': [],
            'suspicious_files': [],
            'database_issues': [],
            'recommendations': []
        }
    
    def execute_ssh_command(self, command):
        """Execute command via SSH"""
        full_command = f'sshpass -p "{self.ssh_pass}" ssh -o StrictHostKeyChecking=no {self.ssh_user}@{self.ssh_host} "{command}"'
        try:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)
    
    def execute_mysql_query(self, query):
        """Execute MySQL query via SSH tunnel"""
        mysql_cmd = f"mysql -h {self.db_host} -P {self.db_port} -u {self.db_user} -p{self.db_pass} {self.db_name} -e '{query}'"
        return self.execute_ssh_command(mysql_cmd)
    
    def scan_for_malware_patterns(self):
        """Scan database for various malware patterns"""
        print("🔍 Scanning for malware patterns in database...")
        
        malware_patterns = [
            "CMW-URL-28773",
            "<script",
            "eval(",
            "base64_decode",
            "gzinflate",
            "str_rot13",
            "javascript:",
            "vbscript:",
            "onload=",
            "onerror=",
            "document.write",
            "iframe",
            "fromCharCode"
        ]
        
        for pattern in malware_patterns:
            print(f"   Checking for: {pattern}")
            
            # Check posts content
            query = f"SELECT COUNT(*) as count FROM {self.wp_prefix}posts WHERE post_content LIKE '%{pattern}%'"
            stdout, stderr = self.execute_mysql_query(query)
            if stdout and "count" in stdout:
                count = stdout.split('\n')[1] if len(stdout.split('\n')) > 1 else "0"
                if count and count != "0":
                    self.scan_results['malware_found'].append({
                        'pattern': pattern,
                        'location': 'posts.post_content',
                        'count': count
                    })
                    print(f"      ⚠️ Found {count} instances in post_content")
            
            # Check postmeta
            query = f"SELECT COUNT(*) as count FROM {self.wp_prefix}postmeta WHERE meta_value LIKE '%{pattern}%'"
            stdout, stderr = self.execute_mysql_query(query)
            if stdout and "count" in stdout:
                count = stdout.split('\n')[1] if len(stdout.split('\n')) > 1 else "0"
                if count and count != "0":
                    self.scan_results['malware_found'].append({
                        'pattern': pattern,
                        'location': 'postmeta.meta_value',
                        'count': count
                    })
                    print(f"      ⚠️ Found {count} instances in postmeta")
            
            # Check options
            query = f"SELECT COUNT(*) as count FROM {self.wp_prefix}options WHERE option_value LIKE '%{pattern}%'"
            stdout, stderr = self.execute_mysql_query(query)
            if stdout and "count" in stdout:
                count = stdout.split('\n')[1] if len(stdout.split('\n')) > 1 else "0"
                if count and count != "0":
                    self.scan_results['malware_found'].append({
                        'pattern': pattern,
                        'location': 'options.option_value',
                        'count': count
                    })
                    print(f"      ⚠️ Found {count} instances in options")
    
    def check_suspicious_files(self):
        """Check for suspicious files in WordPress directory"""
        print("📂 Checking for suspicious files...")
        
        # Check for recently modified files
        stdout, stderr = self.execute_ssh_command(f"find {self.wp_path} -type f -mtime -7 -name '*.php' | head -20")
        if stdout:
            recent_files = stdout.split('\n')
            for file in recent_files:
                if file:
                    self.scan_results['suspicious_files'].append({
                        'file': file,
                        'reason': 'Recently modified PHP file'
                    })
        
        # Check for files with suspicious names
        suspicious_names = ['wp-config-backup.php', 'wp-admin.php', 'wp-login-backup.php', 'index2.php']
        for name in suspicious_names:
            stdout, stderr = self.execute_ssh_command(f"find {self.wp_path} -name '{name}'")
            if stdout:
                self.scan_results['suspicious_files'].append({
                    'file': stdout,
                    'reason': f'Suspicious filename: {name}'
                })
    
    def check_recent_pages(self):
        """Check our recently created accessibility pages for integrity"""
        print("📄 Checking recently created pages...")
        
        page_ids = [7556, 7557, 7558, 7559, 7560]
        for page_id in page_ids:
            query = f"SELECT ID, post_title, post_status, LENGTH(post_content) as content_length FROM {self.wp_prefix}posts WHERE ID = {page_id}"
            stdout, stderr = self.execute_mysql_query(query)
            print(f"   Page {page_id}: {stdout}")
    
    def check_admin_users(self):
        """Check for suspicious admin users"""
        print("👤 Checking admin users...")
        
        query = f"""
        SELECT u.ID, u.user_login, u.user_email, u.user_registered 
        FROM {self.wp_prefix}users u 
        JOIN {self.wp_prefix}usermeta um ON u.ID = um.user_id 
        WHERE um.meta_key = '{self.wp_prefix}capabilities' 
        AND um.meta_value LIKE '%administrator%'
        """
        stdout, stderr = self.execute_mysql_query(query)
        print(f"   Admin users: {stdout}")
    
    def check_plugins_and_themes(self):
        """Check active plugins and themes"""
        print("🔌 Checking active plugins and themes...")
        
        # Active plugins
        query = f"SELECT option_value FROM {self.wp_prefix}options WHERE option_name = 'active_plugins'"
        stdout, stderr = self.execute_mysql_query(query)
        print(f"   Active plugins: {stdout}")
        
        # Current theme
        query = f"SELECT option_value FROM {self.wp_prefix}options WHERE option_name = 'template'"
        stdout, stderr = self.execute_mysql_query(query)
        print(f"   Current theme: {stdout}")
    
    def backup_database(self):
        """Create database backup before any cleanup"""
        print("💾 Creating database backup...")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"renowarriors_backup_{timestamp}.sql"
        
        cmd = f"mysqldump -h {self.db_host} -P {self.db_port} -u {self.db_user} -p{self.db_pass} {self.db_name} > {backup_file}"
        stdout, stderr = self.execute_ssh_command(cmd)
        
        if stderr:
            print(f"   ⚠️ Backup warning: {stderr}")
        else:
            print(f"   ✅ Backup created: {backup_file}")
            return backup_file
        return None
    
    def generate_cleanup_script(self):
        """Generate SQL cleanup script based on findings"""
        cleanup_sql = f"""
-- Reno Warriors Malware Cleanup Script
-- Generated: {datetime.datetime.now()}
-- IMPORTANT: Run backup first!

-- Remove any remaining CMW-URL-28773 references
DELETE FROM {self.wp_prefix}posts WHERE post_content LIKE '%CMW-URL-28773%';
DELETE FROM {self.wp_prefix}postmeta WHERE meta_value LIKE '%CMW-URL-28773%';
DELETE FROM {self.wp_prefix}options WHERE option_value LIKE '%CMW-URL-28773%';

-- Remove common malware patterns (BE CAREFUL - review before running)
-- DELETE FROM {self.wp_prefix}posts WHERE post_content LIKE '%<script%eval(%';
-- DELETE FROM {self.wp_prefix}postmeta WHERE meta_value LIKE '%base64_decode%';

-- Check for suspicious options
SELECT * FROM {self.wp_prefix}options WHERE option_name LIKE '%_transient_%' AND option_value LIKE '%<script%';

-- Verify accessibility pages are clean
SELECT ID, post_title, post_status FROM {self.wp_prefix}posts WHERE ID IN (7556, 7557, 7558, 7559, 7560);

-- Update WordPress salts (optional - will log out all users)
-- UPDATE {self.wp_prefix}options SET option_value = 'NEW_SALT_HERE' WHERE option_name = 'auth_key';
"""
        
        with open('renowarriors_cleanup.sql', 'w') as f:
            f.write(cleanup_sql)
        
        print("📝 Cleanup script generated: renowarriors_cleanup.sql")
        return cleanup_sql
    
    def run_full_scan(self):
        """Run comprehensive security scan"""
        print("🚨 RENO WARRIORS SECURITY SCAN STARTING")
        print("=" * 60)
        
        self.backup_database()
        self.scan_for_malware_patterns()
        self.check_suspicious_files()
        self.check_recent_pages()
        self.check_admin_users()
        self.check_plugins_and_themes()
        
        # Generate recommendations
        if not self.scan_results['malware_found']:
            self.scan_results['recommendations'].append("✅ No active malware patterns detected")
        
        self.scan_results['recommendations'].extend([
            "🔒 Change all WordPress admin passwords",
            "🔄 Update WordPress core and all plugins",
            "🛡️ Install security plugin (Wordfence/Sucuri)",
            "📊 Enable security monitoring",
            "🔍 Schedule regular malware scans"
        ])
        
        self.generate_cleanup_script()
        
        # Save scan results
        with open('renowarriors_scan_results.json', 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS SUMMARY")
        print("=" * 60)
        print(f"Malware patterns found: {len(self.scan_results['malware_found'])}")
        print(f"Suspicious files found: {len(self.scan_results['suspicious_files'])}")
        print(f"Database issues: {len(self.scan_results['database_issues'])}")
        
        if self.scan_results['malware_found']:
            print("\n⚠️ MALWARE DETECTED:")
            for malware in self.scan_results['malware_found']:
                print(f"  {malware['pattern']} in {malware['location']}: {malware['count']} instances")
        
        print("\n📋 RECOMMENDATIONS:")
        for rec in self.scan_results['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📄 Scan results saved to: renowarriors_scan_results.json")
        print(f"🧹 Cleanup script saved to: renowarriors_cleanup.sql")

if __name__ == "__main__":
    scanner = RenoWarriorsSecurityScan()
    scanner.run_full_scan()