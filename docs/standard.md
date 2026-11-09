# Tangyixiao Open Source Standard

Version 0.1.0 · first sample · [Adoption](adoption.md) · [中文概览](../README.zh-CN.md)

Enable applicable participation features from the start. Every entry point needs
a purpose, useful content, a maintenance path, and a check that it works. Project
size changes maintenance depth, not whether people are welcome to participate.

## Project identity and documentation

A project's About description, topics, website, README, package metadata, and
release identity must agree. Give each project its own name, visual identity, real
screenshots, and useful social preview. Shared typography and navigation should
help recognition without making unrelated products look identical.

The README explains purpose, supported platforms, current limitations, installation,
one working example, and help/contribution links. Move development history and
architecture detail into navigable documents. Keep English and Chinese entry pages
consistent; do not promise that every document is translated when it is not.

The reusable website is a project homepage, with replaceable identity, copy,
product visuals, feature descriptions and working links in `project.json`.
Visitors should understand the receiving project and how to start using it.
Maintenance policies, repository file inventories and template-authoring details
belong in the relevant documentation rather than the homepage's primary content.
Use an explicitly approved visual overview before a new website or substantial
redesign, then compare the implementation at desktop and mobile sizes against it.

Pages carries the complete user path: start, configure, use, troubleshoot, update,
and contribute. Make links work under the repository subpath. Support keyboard
navigation, readable contrast, mobile layouts, dark mode, and reduced motion.
State known accessibility gaps; do not claim a certification without an audit.
Add privacy information if a product handles data; disclose telemetry and external
requests. This sample has no tracking, remote fonts, or user-data collection.

## Community and decisions

| Entry | Responsibility |
| --- | --- |
| Discussions | Questions, ideas, announcements, and user examples |
| Issues | Reproducible defects, agreed work, and actionable requests |
| Pull requests | Scoped changes with evidence and review |
| Projects / milestones | Priorities, ownership, and planned work tied to issues |
| Wiki | Community-maintained tips; link official guidance instead of duplicating it |
| Security reporting | Private handling of vulnerabilities and accidental disclosures |

Move an agreed idea into an issue and link the discussion. Keep a public roadmap
honest about current intent; avoid invented deadlines or response-time guarantees.
Use `good first issue` only for genuinely approachable, described tasks. Define
maintainer responsibilities and how decisions are recorded in issues/PRs. An
independent maintainer must not require approval by a nonexistent second maintainer.
Any emergency bypass needs a reason and a record; it must not become the default.

Enable the repository feature and create the actual useful content separately.
An enabled Projects tab does not mean a project board exists. Discussion forms
require matching categories; copying a file does not create those categories.
Sponsors, citation metadata, plugin registries, and research-specific material are
applicable only with a real destination or use case. Record specific exceptions.

## Licenses, origin, and brand

Each repository chooses its own compatible license. Preserve upstream copyright,
license text, notices, and modification obligations. Distinguish original software,
third-party code, screenshots, datasets, fonts, and trademarks. Maintain attribution
where it is required. Publishing code publicly does not establish reuse rights by
itself. This hub's Apache-2.0 license grants no new rights to other repositories.

Require contributors to have the right to submit their work. Do not silently add a
CLA, relicense a project, or copy one project's license across an account. Brand
rules should prevent implied endorsement without blocking ordinary attribution.

## Releases, safety, and recovery

Use identifiable versions and readable changes, state supported platforms and
compatibility, and distinguish stable, preview, and experimental channels when
they exist. An installer release needs correctly named assets, checksums, and
installation/update checks on the relevant supported platforms. Use provenance,
signatures, SBOMs, and dependency scanning when appropriate to what is distributed.
Do not label a source-only standard as a tested multiplatform application.

Keep contribution validation separate from privileged publishing. Use least
privilege, reviewed workflow changes, fixed Action commit SHAs, and protected
release credentials. Untrusted PR content must not execute with release secrets
or on a maintainer's general-purpose machine. Never upload sensitive logs as
public build evidence. Scorecard and security tools are evidence, not guarantees.

For a bad release, explain affected versions, mitigation, and the replacement.
For deployment/template updates, retain a known prior revision and a revert path.
Backups need a bounded retention policy and a restore check. Inventory Git/LFS,
Wiki, release assets, issues, discussions, and platform settings separately; a Git
mirror alone does not preserve the whole project. Do not make endless complete
backups or leave them scattered across the working disk.

When ending maintenance, state support status, archive or hand over deliberately,
preserve attribution, and update links. Never imply that another maintainer has
accepted responsibility without their agreement.

## AI work and disk space

[AI_POLICY.md](../AI_POLICY.md) covers contributor accountability. [AGENTS.md](../AGENTS.md)
covers execution. Adopt it explicitly in each AI client; this hub cannot enforce
another client's filesystem access or inject rules into every project.

Disk use is the primary resource concern. `.github/toss.json` sets a default 10 GiB
free-space reserve, a 1 GiB temporary-growth warning, a 2 GiB task budget, 20 MiB
per log, and one heavy job per machine. These are starting agreements for ordinary
tasks, not universal hardware limits. Explain legitimate adjustments, check peak
space, and remain within the user's authorized work. The local checker enforces
only this repository's source-size budgets; it does not monitor disks or kill jobs.

Prefer reuse before creation. Keep temporary files together. Avoid repeated clones,
toolchains, full datasets, screenshots, test output, and abandoned builds. Record
task-created paths/processes once; reconcile on resume after a crash or interruption.
Before retiring a workspace, preserve dirty files, ignored needed artifacts, and
unique commits, and check other tasks are not using it. Cleanup must be bounded by
verified ownership and resolved paths. Never guess from age, name, or size. Use a
recoverable archive/removal and verify actual free space before claiming recovery.

## Configuration, upgrades, and notifications

Use a small configuration as the intended state. Record observed platform state
with a date and evidence in the existing PR/issue, rather than turning a stale
snapshot into a permanent "passed" badge. Distinguish missing, verified, blocked,
and not-applicable items; give concrete reasons for exceptions.

Classify shared content as inherited defaults, template-managed material, or
project-owned customization. Propose template upgrades through scoped PRs, show
the diff, preserve custom sections and licenses, and test a representative project
before a rollout. Initializers must be repeatable without duplicating categories,
labels, boards, or notifications. Never overwrite all repositories in one run.

Group dependency PRs and bound their number. Audit on meaningful changes and a
reasonable cadence; notify on new actionable findings, recovery, or needed decisions.
Do not post recurring identical reports or close useful issues solely for inactivity.
Bound build caches, artifacts, and logs. Cancel obsolete checks when safe; protect
release/deployment jobs from accidental cancellation or concurrent publication.

## Acceptance

| Evidence | What it proves |
| --- | --- |
| Changed source | The proposed files exist in a specific revision |
| Local checks | The stated checks passed in the stated environment |
| CI | GitHub executed the named checks for the expected commit |
| Merge | The expected changes reached the target branch |
| Deployment | The desired revision was published successfully |
| Platform verification | Actual feature settings/categories/rules match the intended state |
| User path | A fresh visitor can find, install/use, get help, and contribute as applicable |

For each task include only relevant evidence, uncertainties, and retained resources
in the existing PR. Check real links and commands. A local file, scheduled workflow,
enabled feature, or green unrelated check is not proof of the next stage.

## Source references

- [GitHub default community files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [GitHub discussion forms](https://docs.github.com/en/discussions/managing-discussions-for-your-community/creating-discussion-category-forms)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub backups and their scope](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)
