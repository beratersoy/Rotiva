# 🔒 Security Policy

## Supported Versions

We currently support the following versions of Rotiva AI with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🛡️ Security Features

### Data Protection
- **API Keys**: All sensitive API keys are stored in environment variables and excluded from version control
- **User Data**: Personal information is handled according to our Privacy Policy
- **Google Sheets**: OAuth2 authentication with service accounts for secure data access
- **Input Sanitization**: All user inputs are sanitized before processing

### Infrastructure Security
- **Streamlit Cloud**: Deployed on secure cloud infrastructure
- **HTTPS**: All communications are encrypted in transit
- **Environment Isolation**: Production and development environments are separated

### AI/ML Security
- **Prompt Injection Protection**: Input validation to prevent malicious prompt injection
- **Content Filtering**: Response filtering to prevent inappropriate content
- **Rate Limiting**: Protection against abuse through usage monitoring

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 📧 Contact Information
- **Primary**: Create a private issue on GitHub or email us directly
- **Response Time**: We aim to acknowledge reports within 24 hours
- **Resolution Time**: Critical vulnerabilities will be addressed within 7 days

### 📝 What to Include
When reporting a vulnerability, please provide:

1. **Description**: Clear description of the vulnerability
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Impact Assessment**: Potential impact and affected components
4. **Proof of Concept**: Code or screenshots demonstrating the issue
5. **Suggested Fix**: If you have ideas for fixing the vulnerability

### 🔍 Vulnerability Categories

#### Critical (Immediate Action Required)
- Remote code execution
- SQL injection or similar database attacks
- Authentication bypass
- Exposure of sensitive API keys or credentials

#### High Priority
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Privilege escalation
- Data exposure vulnerabilities

#### Medium Priority
- Information disclosure
- Denial of service vulnerabilities
- Session management issues

#### Low Priority
- Minor information leaks
- Non-exploitable security misconfigurations

## 🛠️ Security Best Practices for Contributors

### Code Security
```python
# ✅ Good: Use environment variables for secrets
api_key = os.getenv('GEMINI_API_KEY')

# ❌ Bad: Hard-code sensitive data
api_key = "AIzaSyBKe8kUhQIV6kOYZxtW6Bfc9KVoUVIdAsc"
```

### Input Validation
```python
# ✅ Good: Validate and sanitize user input
def sanitize_input(user_input):
    # Remove potentially harmful characters
    return re.sub(r'[<>"\']', '', user_input.strip())

# ❌ Bad: Use raw user input directly
response = f"User said: {raw_user_input}"
```

### Dependency Management
- Keep dependencies updated to latest stable versions
- Regularly scan for known vulnerabilities using tools like `pip-audit`
- Review new dependencies before adding them

## 🔐 Environment Variables & Secrets

### Required Secrets
- `GEMINI_API_KEY`: Google Gemini AI API key
- `GOOGLE_SHEETS_CREDENTIALS`: Google Sheets service account credentials (JSON)

### Security Guidelines
1. **Never commit** `.env` files or any files containing secrets
2. **Use different keys** for development and production
3. **Rotate keys regularly** (every 90 days recommended)
4. **Monitor usage** for unusual activity

## 📊 Security Monitoring

### What We Monitor
- API usage patterns and anomalies
- Failed authentication attempts
- Unusual user behavior patterns
- System resource usage

### Incident Response
1. **Detection**: Automated monitoring and user reports
2. **Assessment**: Evaluate severity and impact
3. **Containment**: Immediate steps to limit damage
4. **Resolution**: Fix the underlying issue
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Post-incident review and improvements

## 🔒 Data Privacy & GDPR Compliance

### Data We Collect
- **Optional**: User name and email (if provided)
- **Automatic**: Usage patterns and error logs
- **No Storage**: Chat conversations are not permanently stored

### User Rights
- **Access**: Users can request their data
- **Deletion**: Users can request data deletion
- **Portability**: Data export available upon request

### Data Retention
- User registration data: Retained until deletion requested
- Usage logs: 90 days retention for security monitoring
- Error logs: 30 days retention for debugging

## 🚫 Prohibited Activities

### Usage Restrictions
- Do not attempt to reverse engineer the AI models
- Do not use the service for illegal activities
- Do not attempt to extract or scrape user data
- Do not perform load testing without permission

### Consequences
Violations may result in:
- Service access suspension
- IP address blocking
- Legal action if applicable

## 📜 Security Updates

### Notification Process
- Critical security updates will be announced immediately
- Non-critical updates included in regular release notes
- Security advisories published on GitHub Security tab

### Update Recommendations
- **Immediate**: Apply critical security updates
- **Weekly**: Check for security advisories
- **Monthly**: Review access logs and usage patterns

## 🤝 Responsible Disclosure

We believe in responsible disclosure and will:

1. **Acknowledge** your report within 24 hours
2. **Investigate** thoroughly and keep you updated
3. **Credit** you in our security advisories (if desired)
4. **Coordinate** public disclosure timing with you

### Hall of Fame
We maintain a security researcher hall of fame to recognize contributions:
- Currently no reports received
- First reporter will be listed here with gratitude

## 📞 Emergency Contact

For critical security issues requiring immediate attention:

- **GitHub Issues**: Mark as "security" label
- **Email**: Contact repository maintainer
- **Response SLA**: Critical issues acknowledged within 2 hours

## 🔍 Security Audits

### Internal Reviews
- Monthly security checklist review
- Quarterly dependency vulnerability scans
- Annual security policy review

### External Audits
- Open to security researcher reviews
- Penetration testing welcome (with prior notice)
- Bug bounty program under consideration

## 📚 Additional Resources

### Security Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Streamlit Security Best Practices](https://docs.streamlit.io/knowledge-base/deploy/security)
- [Google AI Security Guidelines](https://ai.google.dev/docs/safety_guidance)

### Security Tools We Use
- **Static Analysis**: GitHub CodeQL
- **Dependency Scanning**: GitHub Dependabot
- **Secret Scanning**: GitHub Secret Scanning
- **Container Scanning**: Built into deployment pipeline

---

**Last Updated**: October 21, 2025  
**Next Review**: January 21, 2026

Thank you for helping keep Rotiva AI secure! 🛡️