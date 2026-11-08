<p align="center"><strong>TANGYIXIAO · OPEN SOURCE</strong></p>

# A clear path from first visit to first contribution.

Shared community defaults and the **Tangyixiao Open Source Standard (TOSS)**: useful documentation, open participation, verifiable releases, and AI work that leaves the workspace in good order.

[简体中文](README.zh-CN.md) · [Read the standard](docs/standard.md) · [Adopt it](docs/adoption.md) · [Contribute](CONTRIBUTING.md)

**This is the first reviewable sample.** Files on a pull request branch do not activate account defaults. GitHub uses supported defaults from this repository's default branch after merge. The existing Pages site is published separately from `project-pages`; this proposal includes a replacement under `site/` for review.

## Start here

| You want to… | Go to… |
| --- | --- |
| Report a project's bug or request a feature | That project's Issues; these defaults supply the form when it has no local override |
| Ask how to use a project | That project's Discussions or support instructions |
| Improve these shared defaults | [Open an issue](https://github.com/tangyixiao/.github/issues/new/choose) or read [Contributing](CONTRIBUTING.md) |
| Report a vulnerability privately | The affected project's security policy, then [our fallback](SECURITY.md) |
| Set up a project | [Adoption guide](docs/adoption.md) and [machine-readable policy](.github/toss.json) |

English and Chinese contributions are welcome. A small project can have complete community entry points; the depth of maintenance should match the project.

## What this sample provides

- **Community:** contribution, conduct, support, security, accessibility, issue forms, a PR template, and discussion forms.
- **Project operations:** a standard covering identity, README and Pages, licensing and provenance, contribution, releases, recovery, and maintenance.
- **AI work:** contributor accountability plus concrete [agent instructions](AGENTS.md) for workspace reuse, bounded resource use, and safe cleanup.
- **Disk first:** check peak space before downloads or builds, reuse workspaces, bound logs and caches, and account for abandoned attempts.
- **A small website:** responsive, accessible static files with no build toolchain, third-party fonts, or tracking.
- **Lightweight checks:** Python's standard library validates local links, forms, policy consistency, action pins, and source-size budgets. No package installation is required.

```sh
python scripts/check.py
python -m http.server 8765 --directory site --bind 127.0.0.1
```

Open `http://127.0.0.1:8765`. Stop the server when finished. Reading or editing the documents needs no server.

## Know the boundary

| Layer | What happens |
| --- | --- |
| GitHub defaults | Supported community files apply when a repository has no corresponding local override. Issue-template overrides can replace the whole default set. |
| Project files | A project's license, code owners, workflows, AI policy, and agent instructions need explicit adoption. They are not installed account-wide by this repository. |
| Platform settings | Discussions, private reporting, Pages publishing, project boards, and rulesets need separate configuration and verification. Files alone do not enable them. |
| Agent permissions | Markdown expresses working agreements. Client configuration and filesystem permissions provide enforceable limits. |

Defaults displayed by GitHub are not copied into another repository's clone or release. Follow the [adoption guide](docs/adoption.md) for settings, overrides, and upgrades.

## Completion means evidence

Keep **source changed → checks passed → merged → deployed → platform verified → user path verified** separate. A passing local check is not a deployment, an enabled Projects feature is not a populated board, and a policy file is not proof that every agent loaded it.

The PR template asks for the evidence relevant to the change and the fate of temporary resources. Do not manufacture badges, user counts, certifications, or release claims.

## Scope and license

This repository is the account's community hub, not an application starter template. It does not rewrite existing project policies or licenses. The [standard](docs/standard.md) defines how a separate project template can adopt these agreements.

Original material in this repository is licensed under [Apache-2.0](LICENSE). See [NOTICE](NOTICE). Other projects retain their own licenses, copyright, and upstream obligations.
