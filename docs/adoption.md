# Use the website and community template

[Standard](standard.md) · [Agent rules](../AGENTS.md) · [Policy](../.github/toss.json)

## Create a project website

After this sample is merged and template mode is enabled, start from the repository's
**Use this template** entry. During review, use the PR branch or copy its website
into an existing project. The public page should describe the receiving project itself.
The default OJ NEXUS content demonstrates the layout; it is not the identity of
every project that adopts the template.

For a website-only adoption, copy `project.json`, `locales/`, `templates/project-homepage.html`,
`scripts/render_site.py`, and `site/`. No application source, dependency tree or
package installation is required. Keep the source template and configuration so
the next content update can be rendered consistently.

Schema 2 separates shared data from translations. Edit `project.json` with actual
identity, URLs, release information, default theme and locale registration. Set
`copyright_notice` to the receiving project's actual copyright notice. This visible
credit is separate from the license: edit `license_label` and `links.license`
together to describe the project's actual license. These fields do not replace
its license text. Edit
`locales/<code>.json` for page titles, descriptions, features, navigation, captions
and accessible control labels. `{project}`, `{release}` and `{copyright}` in text
insert the shared name, release and copyright notice; asset paths and icon names
are never expanded. The default footer is `{copyright} · {project}` in both languages.
The sample's OJ NEXUS release links are
real, but belong to OJ NEXUS; update them before publishing another project.

Four pages are generated for each registered locale: `index.html`, `features.html`,
`download.html` and `community.html`. The default Chinese locale uses the site root;
English uses `en/`. Navigation and language links use relative paths, including when
hosted under a GitHub Pages repository path. Changing language keeps the same page.

To add a language, create a complete `locales/<code>.json` with the same keys and
array lengths as the default dictionary, translate its text and image descriptions,
and add `{code, label, directory}` to `locales` in `project.json`. Use a unique language
tag and safe single directory name; the default locale alone uses `directory: ""`.
Only registered languages with valid dictionaries appear. The renderer rejects
missing keys and shape differences instead of publishing partly translated pages.
Localized illustrations may share files or point to accurately translated variants.

The default appearance is light. Visitors can choose light, dark or system from
every page. `theme` in `project.json` controls the fallback before a saved preference.
The small synchronous `theme-init.js` applies a saved choice before the stylesheet
paints; one site-root-scoped preference is shared by all pages and languages. System
mode reacts to system changes. Storage denial leaves the current-page controls usable;
cross-file `file://` persistence depends on the browser. No-JavaScript navigation,
language switching and reading remain available, with the configured theme fallback.

To use a captured product image, set `preview.image: {src}` in `project.json` and
`preview.image: {alt, caption}` in each dictionary. Replace the native illustrative
tabs/items in that dictionary with these image descriptions if no longer needed.
Place the capture beneath `site/` and identify it accurately.

The optional `platforms` array defaults to entries containing only `{name, href}`.
Each entry displays the service name with an original generic external-link icon;
no official brand image download is needed. Remove the array for a project that
does not connect external platforms. Optional local `logo` paths remain supported;
use them only for artwork you own or have clear permission to use, and record its
source and applicable terms. Set `wordmark: true` when permitted artwork already
contains the full name; otherwise the platform name appears beside it.

Each translated feature group can use `image: {src, dark_src, alt, caption}` instead of its small
`preview` rows. Image paths must be local to `site/`; place a real capture or
original illustration in `site/assets/`. The sample's warm and green SVG panels
are labeled demonstrations, not application screenshots. Replace or remove the
OJ-specific platform entries and illustrations when adopting this for another product.
Keep captions accurate. `dark_src` is optional; when provided, both the displayed
image and full-size link follow the selected theme.

The source-size limits in `.github/toss.json` are budgets for this small starter.
Review them when adding a real screenshot or application source; choose an explicit
reasonable budget for that project rather than silently disabling the checks.
Keep large release assets in the project's release/distribution channel.
This starter's site budget is 256 KiB for eight HTML pages, shared scripts/styles
and eight small localized light/dark SVGs. The complete source
budget remains 512 KiB. Neither budget includes release binaries or dependencies.

```sh
python scripts/render_site.py
python scripts/render_site.py --check
python scripts/check.py
python -m http.server 8765 --directory site --bind 127.0.0.1
```

Review the desktop and mobile page. The generated HTML contains the content,
works without JavaScript and does not depend on fetching its configuration at
runtime. Commit configuration, dictionaries, templates and every rendered HTML page.
The read-only render check fails if any expected page is missing or stale. Use
`--output-dir <directory>` for a different output folder. Rendering does not delete
unrelated files or retired locale directories. Its marker identifies retired
generated HTML, which `--check` reports as needing review instead of silently
publishing a removed language. Remove a retired generated directory
only after reviewing its ownership and any manual content. The repository
checker and renderer tests apply to the complete starter; a website-only copy can
still run the renderer's `--check` command independently.

Earlier single-page PR snapshots used schema 1. Move their shared values into the
schema 2 structure and their visible text into locale dictionaries before rendering;
the renderer reports the unsupported schema rather than silently discarding content.
The old single-file `--output` option is replaced by `--output-dir`.

When copying community files, adapt contacts, source attribution and contribution
instructions to the receiving project. Never replace an existing application's
license merely because this starter is Apache-2.0.

## Activate the sample

1. Review the PR, its exact changed files, checks, and local site preview.
2. Merge only after review. Supported defaults become eligible on the default branch.
3. Verify the target project's community links and new-issue form in the GitHub UI.
   A local Issue template/configuration can replace the entire inherited set.
4. Treat other repositories separately: do not overwrite their existing community
   files, licenses, or settings just to make this sample look complete.

Inherited files are displayed by GitHub but are not added to downstream clones,
archives, or packages. Include required notices and licensing in each project.
Do not claim global inheritance for `AGENTS.md`, `AI_POLICY.md`, workflows,
`LICENSE`, CODEOWNERS, or this repository's configuration.

## Configure the platform explicitly

The intended switches are in `.github/toss.json`. Read actual settings before
changing them, apply only this task's scope, and read them back afterward. A
repeat run should repair differences without duplicating content.

| Capability | Verification |
| --- | --- |
| Issues / Wiki / Discussions | Read repository settings, then open the relevant entry point |
| Template repository | Confirm the Use this template entry; creating a copy does not keep it synchronized |
| Discussion forms | Confirm categories have matching `ideas` and `q-a` slugs and open their forms |
| Projects | Verify the feature and an actual board separately; link populated work when it exists |
| Private vulnerability reporting | Verify enablement and the private report entry, without submitting a test vulnerability |
| Pages | Read publishing source and the deployed revision; test the actual URL |
| Actions | Verify permissions and a successful run for the expected commit |
| Releases | Publish a real version when ready; no placeholder installer/assets |
| Rulesets | Inspect current rules, confirm the maintainer can complete the workflow, then test them |

Do not create sponsor destinations, sample community posts, or empty boards to
inflate a completion score. Establish real content when its purpose is defined.
No test submission to Issues/Discussions is needed to prove a form can open.

### Existing Pages site

At initial inspection on 2026-11-08, Pages used the `project-pages` branch at `/`.
That branch is outside this PR. The new `site/` is a proposed source. Preview it
locally before changing the publishing source. Configure all public project links
for the receiving project before publishing it.

The included `pages.yml` is manual and restricted to `main`. After this PR is
merged and replacing the current site is authorized, select GitHub Actions as
the Pages source, then run it. The workflow does not automatically replace a
legacy branch-based site. If the new site fails, restore the previous publishing
source or deploy the previous accepted revision and verify the URL again.

## Load agent instructions

1. Read the AI client's supported global/project instruction mechanism.
2. Merge the applicable rules from `AGENTS.md` into that entry point, preserving
   other instructions. Set local scratch/output locations to the host's conventions.
3. Ask the client to identify loaded instruction sources and summarize its disk
   budget and cleanup obligations. Check for project/skill rules that conflict.
4. Use client filesystem restrictions or OS quotas if hard enforcement is required.
   A policy document alone cannot stop arbitrary filesystem writes.

This sample does not modify machine-global rules. Never turn a repository task
into an unrequested installation of scheduled cleaners, watchers, or startup jobs.

## Override and upgrade safely

- Leave supported defaults inherited when no project customization is needed.
- When copying a default into a project, record that it is now project-owned;
  future changes to this hub will no longer replace it automatically.
- Put project-specific build/installation instructions and licenses in the project.
- Before upgrading, compare the old shared version, the new shared version, and
  local customizations. Open a small PR; never replace the project tree blindly.
- Keep the prior revision and a revert path. Validate an application/plugin/library
  as appropriate before wider adoption. Start with one representative existing project.
- Verify English/Chinese navigation, user commands, forms, and official links after
  upgrades. Different repository types have different real user paths.

## Run the checks

```sh
python scripts/check.py
```

The checker reads source and runs bounded renderer tests without installing
dependencies or calling network services. It does not modify or delete project
sources; tests create and clean their own bounded scratch under `work/`.
`.yml` forms use JSON syntax, which is valid YAML;
this makes local structural validation possible with Python's standard library.
It checks rendering consistency, local links and fragment targets, form structure,
policy budgets, source size, static site asset links and fixed Action commit references.

It does **not** certify external link availability, browser behavior, legal
compatibility, current GitHub settings, downstream inheritance, or a deployed site.
Those require the corresponding review or live check, with evidence in the PR.
