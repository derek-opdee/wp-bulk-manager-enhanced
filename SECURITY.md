# Security Guidelines 🔐

This document outlines security best practices for the WP Bulk Manager Enhanced project.

## 🚨 API Key Security

### ⚠️ NEVER commit API keys to the repository

API keys are sensitive credentials that should never be stored in version control. This project has been configured to prevent accidental exposure.

### 🔧 Configuration Setup

1. **Use the template configuration:**
   ```bash
   cp config.example.json config.json
   ```

2. **Set environment variables:**
   ```bash
   # In your shell profile (.bashrc, .zshrc, etc.)
   export OPDEE_WORDPRESS_API_KEY="your_actual_api_key_here"
   
   # Or create a local .env file (ignored by git)
   echo "OPDEE_WORDPRESS_API_KEY=your_actual_api_key_here" > .env
   ```

3. **Update config.json with your actual keys:**
   ```json
   {
     "sites": [
       {
         "name": "Your Site",
         "url": "https://yoursite.com",
         "api_key": "${OPDEE_WORDPRESS_API_KEY}",
         "added": "2025-01-15T10:00:00Z"
       }
     ]
   }
   ```

### 🛡️ What's Protected

The following files are automatically ignored by git to prevent credential leaks:

- `config.json` (your personal configuration)
- `.env*` (environment files)
- `*api_key*` (any files containing "api_key")
- `*secret*` (any files containing "secret")
- `*token*` (any files containing "token")
- `*_secrets.py` (Python secret files)
- `*_keys.py` (Python key files)

### 🔍 GitGuardian Alert Resolution

If you received a GitGuardian security alert:

1. **Rotate your API keys immediately**
   - Go to your WordPress admin → WP Bulk Manager → Generate new API key
   - Update your environment variables with the new key

2. **Clean up the repository history** (if needed):
   ```bash
   # Remove sensitive data from git history (use with caution)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch config.json" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push the cleaned history:**
   ```bash
   git push origin --force --all
   git push origin --force --tags
   ```

### 🔐 WordPress API Key Management

#### Generating API Keys
1. Go to WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords"
3. Create a new application password for "WP Bulk Manager"
4. Copy the generated password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
5. Store securely in environment variables

#### API Key Permissions
WordPress application passwords inherit the user's capabilities. For security:
- Create a dedicated user for API access
- Assign minimal required permissions
- Use role-based access control

### 🌐 Network Security

#### HTTPS Only
- All API requests must use HTTPS
- Never send API keys over unencrypted connections
- Verify SSL certificates in production

#### IP Whitelisting (Optional)
Configure WordPress to restrict API access by IP:
```php
// In wp-config.php
define('WPBM_ALLOWED_IPS', ['192.168.1.100', '10.0.0.50']);
```

#### Rate Limiting
The plugin includes built-in rate limiting:
- 100 requests per hour per API key (default)
- Configurable in wp-config.php: `define('WPBM_RATE_LIMIT', 200);`

### 📋 Security Checklist

- [ ] API keys stored in environment variables only
- [ ] `config.json` contains variable references, not actual keys  
- [ ] No hardcoded credentials in any code files
- [ ] WordPress uses application passwords, not admin passwords
- [ ] HTTPS enforced for all API communication
- [ ] Rate limiting configured appropriately
- [ ] Regular API key rotation schedule established
- [ ] Monitoring enabled for suspicious API activity

### 🚨 Incident Response

If you suspect API key compromise:

1. **Immediate Actions:**
   - Rotate all affected API keys
   - Review access logs for suspicious activity
   - Check for unauthorized content changes

2. **Investigation:**
   - Identify the source of the compromise
   - Assess the scope of potential damage
   - Document the incident for future prevention

3. **Recovery:**
   - Update all systems with new credentials
   - Notify team members of the security update
   - Review and improve security practices

### 📚 Additional Resources

- [WordPress Application Passwords](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)
- [GitGuardian Best Practices](https://docs.gitguardian.com/secrets-detection/detectors)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

**Remember: Security is everyone's responsibility. When in doubt, ask for a security review!** 🛡️

**🔗 Generated with [Claude Code](https://claude.ai/code)**