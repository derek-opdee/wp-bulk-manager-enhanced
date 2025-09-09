# WP Bulk Manager - Folder Organization Guide

## Directory Structure

```
wp-bulk-manager/
├── macos-app/              # Main application directory
│   ├── wpbm_*.py          # Core application files
│   ├── config.json        # Site configurations
│   ├── requirements.txt   # Python dependencies
│   │
│   ├── temp/             # Temporary files and test scripts
│   │   └── test_*.py     # Connection tests, debugging scripts
│   │
│   ├── scripts/          # Utility scripts
│   │   ├── analysis/     # Analysis and verification scripts
│   │   │   ├── analyze_*.py
│   │   │   ├── check_*.py
│   │   │   └── verify_*.py
│   │   │
│   │   └── fixes/        # Fix and transformation scripts
│   │       ├── fix_*.py
│   │       └── transform_*.py
│   │
│   ├── reports/          # Generated reports
│   │   ├── *.json        # Analysis reports
│   │   └── *.log         # Operation logs
│   │
│   ├── exports/          # Exported data
│   │   ├── *.csv         # CSV exports
│   │   ├── *.html        # HTML content exports
│   │   └── *.xml         # XML exports
│   │
│   ├── backups/          # Backup files
│   │   └── *.bak         # Automatic backups
│   │
│   └── logs/             # Application logs
│       └── *.log         # Debug and error logs
│
└── wordpress-plugin/      # WordPress plugin files
    └── wp-bulk-manager-client.php
```

## Usage Guidelines

### temp/
- **Purpose**: Temporary scripts, test files, debugging code
- **Cleanup**: Can be safely deleted periodically
- **Examples**: test_connection.py, debug_auth.py

### scripts/analysis/
- **Purpose**: Reusable analysis scripts
- **Keep**: These are useful tools, don't delete
- **Examples**: analyze_h1_issues.py, check_seo_compliance.py

### scripts/fixes/
- **Purpose**: Scripts that fix specific issues
- **Keep**: Useful for recurring tasks
- **Examples**: fix_gutenberg_h1.py, transform_opdee_content.py

### reports/
- **Purpose**: Generated analysis reports
- **Cleanup**: Delete old reports after reviewing
- **Examples**: seo_analysis.json, h1_report.json

### exports/
- **Purpose**: Data exports from WordPress
- **Cleanup**: Delete after importing or processing
- **Examples**: pages_export.csv, content_backup.html

### backups/
- **Purpose**: Automatic backups before major changes
- **Cleanup**: Keep recent backups, delete old ones
- **Naming**: Uses timestamp: backup_20240607_143022.json

### logs/
- **Purpose**: Application logs for debugging
- **Cleanup**: Rotate logs weekly/monthly
- **Examples**: wpbm_debug.log, error.log

## File Naming Conventions

### Scripts:
- Analysis: `analyze_[what].py` (e.g., analyze_h1_structure.py)
- Fixes: `fix_[issue].py` (e.g., fix_missing_seo.py)
- Tests: `test_[feature].py` (e.g., test_api_connection.py)
- Transforms: `transform_[content].py` (e.g., transform_opdee_style.py)

### Reports:
- JSON: `[site]_[analysis]_report.json`
- CSV: `[site]_[content]_export.csv`
- Logs: `[operation]_[timestamp].log`

## Cleanup Commands

```bash
# Clean temporary files older than 7 days
find temp/ -type f -mtime +7 -delete

# Clean old reports (keep last 10)
ls -t reports/*.json | tail -n +11 | xargs rm -f

# Clean old exports
find exports/ -type f -mtime +30 -delete

# Archive old logs
tar -czf logs/archive_$(date +%Y%m).tar.gz logs/*.log
rm logs/*.log
```

## Best Practices

1. **Before Running Scripts**: Check if similar script exists in scripts/
2. **After Analysis**: Move reports to reports/ folder
3. **Test Scripts**: Create in temp/ first, move to scripts/ if reusable
4. **Exports**: Delete after processing to save space
5. **Backups**: Keep at least 3 recent backups

## Quick Commands

```bash
# See what's in each folder
ls -la temp/
ls -la scripts/analysis/
ls -la reports/

# Find recent files
find . -type f -mtime -1 -ls

# Check folder sizes
du -sh */

# Clean all temporary files
rm -f temp/*
```