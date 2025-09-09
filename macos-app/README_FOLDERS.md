# Folder Organization System

This project uses an organized folder structure to keep the main directory clean and maintainable.

## Quick Reference

- **temp/** - Temporary test scripts (safe to delete)
- **scripts/** - Reusable utility scripts
  - **analysis/** - Analysis and checking scripts
  - **fixes/** - Scripts that fix issues
- **reports/** - JSON reports and analysis results
- **exports/** - CSV, HTML, XML exports
- **backups/** - Automatic backups
- **logs/** - Debug and error logs

## What Goes Where?

| File Type | Folder | Example |
|-----------|---------|---------|
| Test scripts | `temp/` | `test_connection.py` |
| Analysis scripts | `scripts/analysis/` | `analyze_h1_issues.py` |
| Fix scripts | `scripts/fixes/` | `fix_missing_seo.py` |
| JSON reports | `reports/` | `seo_analysis_report.json` |
| CSV exports | `exports/` | `pages_export.csv` |
| HTML exports | `exports/` | `page_content.html` |
| Backups | `backups/` | `config.json.bak` |
| Logs | `logs/` | `debug_20240607.log` |

## Cleanup Schedule

- **temp/** - Delete files older than 7 days
- **exports/** - Delete files older than 30 days
- **reports/** - Keep last 10 reports
- **logs/** - Archive monthly

## Usage

```bash
# Check what's in each folder
ls -la temp/
ls -la scripts/analysis/

# Clean temporary files
find temp/ -mtime +7 -delete

# See folder sizes
du -sh */
```