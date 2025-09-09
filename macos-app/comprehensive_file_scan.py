#!/usr/bin/env python3
"""
Comprehensive file-based malware scan for Reno Warriors WordPress site
"""

import subprocess
import datetime

class ComprehensiveFileScan:
    def __init__(self):
        self.ssh_host = "170.64.179.157"
        self.ssh_user = "master_ntuqvnephb"
        self.ssh_pass = "56tbztc2cRZ8"
        self.wp_path = "/home/1283775.cloudwaysapps.com/cfhbaxywhg/public_html"
        
        self.malware_patterns = [
            "CMW-URL-28773",
            "eval(base64_decode",
            "eval(gzinflate",
            "eval(str_rot13",
            "preg_replace.*\/e",
            "assert.*base64",
            "FilesMan",
            "c99sh",
            "r57shell",
            "Magento Themes",
            "MAGENTO_ROOT",
            "<script>eval(",
            "document.write(unescape",
            "function_exists.*curl_init",
            "wp_set_auth_cookie.*false",
            "add_action.*wp_loaded.*create_function"
        ]
    
    def execute_ssh_command(self, command):
        """Execute command via SSH"""
        full_command = f'sshpass -p "{self.ssh_pass}" ssh -o StrictHostKeyChecking=no {self.ssh_user}@{self.ssh_host} "{command}"'
        try:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)
    
    def check_file_integrity(self):
        """Check WordPress core file integrity"""
        print("🔍 Checking WordPress core file integrity...")
        
        # Check if any core files have been modified recently
        stdout, stderr = self.execute_ssh_command(f"find {self.wp_path}/wp-admin {self.wp_path}/wp-includes -name '*.php' -mtime -7 -ls 2>/dev/null | wc -l")
        print(f"   Recent core file modifications: {stdout}")
        
        # Check for files with unusual permissions
        stdout, stderr = self.execute_ssh_command(f"find {self.wp_path} -name '*.php' -perm 777 2>/dev/null")
        if stdout:
            print(f"   ⚠️ Files with 777 permissions: {stdout}")
        else:
            print("   ✅ No files with dangerous 777 permissions")
    
    def scan_for_malware_in_files(self):
        """Scan files for malware patterns"""
        print("🦠 Scanning files for malware patterns...")
        
        found_infections = []
        
        for pattern in self.malware_patterns:
            print(f"   Checking for: {pattern}")
            
            # Escape special characters for grep
            escaped_pattern = pattern.replace("(", "\\(").replace(")", "\\)").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]")
            
            # Search in PHP files
            stdout, stderr = self.execute_ssh_command(f"grep -r '{escaped_pattern}' {self.wp_path}/ --include='*.php' 2>/dev/null | head -3")
            
            if stdout and len(stdout) > 10:  # Found something substantial
                print(f"      ⚠️ FOUND: {pattern}")
                found_infections.append({
                    'pattern': pattern,
                    'matches': stdout.split('\n')[:3]  # First 3 matches
                })
            
        return found_infections
    
    def check_suspicious_files(self):
        """Check for suspicious files and directories"""
        print("📂 Checking for suspicious files...")
        
        suspicious_files = []
        
        # Check for common malware file names
        malware_files = [
            "wp-config-backup.php",
            "wp-admin.php", 
            "adminer.php",
            "phpMyAdmin.php",
            "shell.php",
            "c99.php",
            "r57.php",
            "wso.php",
            "b374k.php",
            "symlink.php",
            "bypass.php"
        ]
        
        for filename in malware_files:
            stdout, stderr = self.execute_ssh_command(f"find {self.wp_path} -name '{filename}' 2>/dev/null")
            if stdout:
                suspicious_files.append(f"Malware file found: {stdout}")
        
        # Check for files in uploads directory with PHP extension
        stdout, stderr = self.execute_ssh_command(f"find {self.wp_path}/wp-content/uploads -name '*.php' 2>/dev/null")
        if stdout:
            suspicious_files.append(f"PHP files in uploads: {stdout}")
        
        # Check for hidden files starting with dot
        stdout, stderr = self.execute_ssh_command(f"find {self.wp_path} -name '.*' -type f -name '*.php' 2>/dev/null")
        if stdout:
            suspicious_files.append(f"Hidden PHP files: {stdout}")
        
        return suspicious_files
    
    def check_wp_config_security(self):
        """Check wp-config.php for security issues"""
        print("⚙️ Checking wp-config.php security...")
        
        # Check if wp-config.php is readable by web
        stdout, stderr = self.execute_ssh_command(f"ls -la {self.wp_path}/wp-config.php")
        print(f"   wp-config.php permissions: {stdout}")
        
        # Check for suspicious additions to wp-config
        stdout, stderr = self.execute_ssh_command(f"grep -n 'eval\\|base64\\|exec\\|system\\|shell_exec' {self.wp_path}/wp-config.php 2>/dev/null")
        if stdout:
            print(f"   ⚠️ Suspicious code in wp-config: {stdout}")
        else:
            print("   ✅ wp-config.php appears clean")
    
    def check_htaccess_security(self):
        """Check .htaccess for malicious redirects"""
        print("🔒 Checking .htaccess for malicious redirects...")
        
        stdout, stderr = self.execute_ssh_command(f"cat {self.wp_path}/.htaccess 2>/dev/null")
        if "RewriteRule" in stdout:
            print("   Found rewrite rules - checking for suspicious patterns...")
            
            suspicious_patterns = ["base64", "eval", "php://input", "auto_prepend_file"]
            for pattern in suspicious_patterns:
                if pattern in stdout:
                    print(f"      ⚠️ Suspicious pattern in .htaccess: {pattern}")
        
        print("   .htaccess contents:")
        print(f"   {stdout[:500]}...")  # First 500 chars
    
    def run_comprehensive_scan(self):
        """Run complete file-based security scan"""
        print("🚨 COMPREHENSIVE FILE SCAN - RENO WARRIORS")
        print("=" * 60)
        print(f"Scanning path: {self.wp_path}")
        print(f"Timestamp: {datetime.datetime.now()}")
        print("=" * 60)
        
        # Run all checks
        self.check_file_integrity()
        print()
        
        infections = self.scan_for_malware_in_files()
        print()
        
        suspicious = self.check_suspicious_files()
        print()
        
        self.check_wp_config_security()
        print()
        
        self.check_htaccess_security()
        print()
        
        # Summary
        print("=" * 60)
        print("📊 COMPREHENSIVE SCAN SUMMARY")
        print("=" * 60)
        
        if infections:
            print(f"⚠️ MALWARE PATTERNS FOUND: {len(infections)}")
            for infection in infections:
                print(f"   Pattern: {infection['pattern']}")
                for match in infection['matches']:
                    print(f"     {match}")
        else:
            print("✅ NO MALWARE PATTERNS DETECTED IN FILES")
        
        if suspicious:
            print(f"\n⚠️ SUSPICIOUS FILES: {len(suspicious)}")
            for item in suspicious:
                print(f"   {item}")
        else:
            print("\n✅ NO SUSPICIOUS FILES DETECTED")
        
        print(f"\n🎯 FINAL STATUS:")
        if not infections and not suspicious:
            print("   ✅ SITE APPEARS CLEAN - No file-based malware detected")
        else:
            print("   ⚠️ ISSUES FOUND - Review findings above")
        
        print("\n📋 RECOMMENDATIONS:")
        print("   🔒 Change all WordPress passwords")
        print("   🔄 Update WordPress core and plugins")
        print("   🛡️ Install security plugin (Wordfence/Sucuri)")
        print("   📊 Enable file integrity monitoring")
        print("   🔍 Schedule regular malware scans")

if __name__ == "__main__":
    scanner = ComprehensiveFileScan()
    scanner.run_comprehensive_scan()