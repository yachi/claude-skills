# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT open a public issue.**
2. Use [GitHub's private vulnerability reporting](https://github.com/yachi/claude-skills/security/advisories/new) to submit your report.

You will receive a response within 72 hours acknowledging your report.

## Scope

This project contains Claude Code skill definitions (markdown-based prompts). The primary security concerns are:

- **Prompt injection** — malicious instructions embedded in skill files
- **Data exfiltration** — skills that attempt to send data to external services
- **Credential exposure** — skills that attempt to access or leak API keys, tokens, or secrets

## Supported Versions

Only the latest version on the `main` branch is supported with security updates.

| Version | Supported |
|---------|-----------|
| `main` (latest) | Yes |
| Older commits | No |
