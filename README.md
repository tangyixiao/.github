# Project website and community template

A reusable multilingual project website, community defaults, and practical maintenance
rules. The website introduces a project's purpose, shows its experience, and helps
visitors start using it or participate.

[简体中文](README.zh-CN.md) · [Use the template](docs/adoption.md) · [Project standard](docs/standard.md) · [Contribute](CONTRIBUTING.md)

## Make it your project's website

The website uses **OJ NEXUS** as example content across Home, Features, Get started
and Community pages. Shared identity, copyright notice, license label, releases,
URLs and locale registration come from [`project.json`](project.json); complete Chinese and English content comes from
`locales/`. Visitors can choose light, dark or system appearance. The example does not include the OJ NEXUS application
source or an installer. Its drawn interface is explicitly labelled as an illustration.
Platform names appear as text with an original generic external-link icon; the
current template does not bundle official platform artwork. The original SVG
interface illustrations remain included.

1. After the sample is merged and template mode is enabled, create a repository
   from it; during review, use the PR branch or copy its website files into an existing project.
2. Edit `project.json` with your project's identity, `copyright_notice`,
   `license_label` and URLs, and `locales/*.json`
   with its translated content. Replace the
   illustration with a real screenshot when available; provide meaningful alternative text.
3. Render and check the site:

   ```sh
   python scripts/render_site.py
   python scripts/check.py
   python -m http.server 8765 --directory site --bind 127.0.0.1
   ```

Open `http://127.0.0.1:8765`, then stop the server when finished. Generated HTML is
committed, readable without JavaScript, and can also be opened directly. Editing
the configuration or translations and rerendering is the normal content-update path.
Language switching keeps the corresponding page; theme preferences persist across
pages and languages when browser storage is available. Add a complete locale
dictionary and register its directory to extend the site without copying its styles.

The renderer and checks use Python's standard library. There is no package install,
frontend build, remote font or analytics service. Read the [adoption guide](docs/adoption.md)
for copying only the website, adjusting community contacts, and configuring publishing.

## Included

| Part | Purpose |
| --- | --- |
| Project website | Four pages in Chinese and English, extensible locale dictionaries, three appearance modes and responsive product illustrations |
| Community files | Contribution, conduct, support, security and accessibility guidance; issue/discussion forms and PR template |
| Maintenance standard | Licensing and origin, releases, recovery, upgrades and evidence of completion |
| AI working agreements | Contributor responsibility, workspace reuse, disk budgets and task cleanup |
| Offline checks | Configuration/render consistency, renderer tests, local links, forms, Action pins and source-size budgets |

English and Chinese contributions are welcome. Use the affected project's own
issue tracker for its bugs and feature requests. This repository's tracker covers
the shared template and defaults; private reports follow [SECURITY.md](SECURITY.md).

**Review status:** supported account defaults activate only after merge to the
default branch. The current Pages site still comes from `project-pages`; this PR
proposes `site/` as its replacement without changing that existing publishing source.

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

This repository provides account defaults and a reusable website/community starter.
It does not rewrite existing projects or supply their application code. When adopting,
review project-specific contacts, provenance and licenses rather than copying them blindly.

Original material in this repository is licensed under [Apache-2.0](LICENSE). See [NOTICE](NOTICE). Other projects retain their own licenses, copyright, and upstream obligations.
