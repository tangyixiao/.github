# Security policy

## Report privately

Do not publish a suspected vulnerability, exploit details, credentials or private data in an issue, discussion or pull request.

1. Open the affected repository's **Security → Advisories → Report a vulnerability** page. The direct URL follows `https://github.com/OWNER/REPOSITORY/security/advisories/new`.
2. If private reporting is unavailable there, use [the private security report for tangyixiao/.github](https://github.com/tangyixiao/.github/security/advisories/new) and clearly identify the affected repository. If GitHub refuses access, check the affected repository's own security policy for another private channel. Do not fall back to a public vulnerability report.

Include the affected repository and version or commit, a concise description, potential impact, and the smallest safe reproduction. Replace secrets with placeholders. Do not access other people's data or disrupt a deployed service to prove a report.

If you exposed a credential, revoke or rotate it through its provider promptly. Deleting a public message or Git commit alone does not invalidate a secret.

## Scope and response

This is the shared baseline for repositories owned by tangyixiao. An affected repository's own security policy defines its supported versions and takes precedence. Do not assume every historical version is supported. For the shared standards repository itself, reports concern the current default branch and its published tooling or site.

The maintainer will assess reports as availability permits. There is no guaranteed response deadline, paid bounty or service-level agreement. Coordinate public disclosure privately so users can receive a fix or mitigation when possible. Neither a local fix nor a merged pull request proves a deployed service or installed release has been updated.
