# Contributing

Contributions in English or Chinese are welcome. This is a personal project collection, maintained as time permits. There is no guaranteed response or review deadline.

This shared guide is provided by [tangyixiao/.github](https://github.com/tangyixiao/.github). A repository's own contribution guide, build instructions and supported-version policy take precedence for that project.

## Choose the right place

- Report a project bug or propose a change in that project's Issues. Check existing issues and its contribution guide first.
- Use that project's Discussions for questions and early ideas, when available. Follow [the support guide](https://github.com/tangyixiao/.github/blob/main/SUPPORT.md) if it has no Discussions.
- Report a problem with these shared standards in [tangyixiao/.github Issues](https://github.com/tangyixiao/.github/issues).
- Follow [the security policy](https://github.com/tangyixiao/.github/blob/main/SECURITY.md) for vulnerabilities. Never put secrets or exploit details in a public issue.

## Propose and make a change

For a large change, discuss the intended result and scope before investing heavily. Small fixes can go straight to a pull request. Keep each pull request focused on one reviewable outcome; avoid unrelated formatting, dependency updates or generated files.

Start with the target repository's current instructions and Git state. Preserve work that belongs to other people or tasks. Prefer reusing a suitable checkout; create an isolated worktree only when there is a concrete need. Record any new worktree so it can be handled at the end.

Follow the project's existing style and build process. Add or update meaningful tests when behavior changes, and update documentation when users need to act differently. A documentation-only fix does not require a new test suite. Do not install a toolchain or generate a full build just to make a lightweight check when an appropriate existing tool is available.

## Show what was verified

Explain the problem, the resulting behavior and the validation relevant to the change. Name checks that were actually run and report their results. Keep local checks, CI, deployment, repository settings and real use separate: one does not prove another. If a check was unavailable, say what remains unverified.

For screenshots, logs or reproduction files, remove credentials, private paths where sensitive, and unrelated personal data. Prefer a small reproduction over uploading an entire environment or dataset.

## Use resources responsibly

Disk space is the main resource concern. Avoid repeated clones, downloads, dependency trees, full backups and abandoned build outputs. Consider peak disk use when an archive, its extracted contents and a build may coexist. Keep scratch files in the task's designated working area and only retain useful deliverables.

Before finishing, check resources created for the task: temporary data, environments, worktrees and background processes. Remove or archive only content whose ownership and safe recovery are established. Protect uncommitted work, unique commits and anything another task still uses. State the purpose of substantial retained artifacts. Moving a directory on the same disk or placing it in the Recycle Bin does not prove disk space was released.

Use reasonable build and test concurrency. Reduce load if the machine becomes unresponsive or memory is under pressure, and stop task-owned services when no longer needed.

## AI assistance and contribution terms

AI-assisted contributions are accepted under [the AI policy](https://github.com/tangyixiao/.github/blob/main/AI_POLICY.md). The contributor remains responsible for understanding, correctness, provenance and verification.

Submit only material you have permission to contribute. Identify substantial third-party material and preserve applicable notices. Contributions must be compatible with the target repository's stated license; if that repository has no license, ask about terms before contributing material intended for redistribution. This guide introduces no separate CLA and does not change existing project licenses.

Please follow [the code of conduct](https://github.com/tangyixiao/.github/blob/main/CODE_OF_CONDUCT.md). The maintainer may request changes, defer work or decline a proposal that does not fit the project.
