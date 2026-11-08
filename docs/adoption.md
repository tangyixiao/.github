# Adopt and maintain the defaults

[Standard](standard.md) · [Agent rules](../AGENTS.md) · [Policy](../.github/toss.json)

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
locally before changing the publishing source. Site document links intentionally
target the sample review branch; switch them to the accepted revision/default
branch when preparing a production deployment.

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

The checker reads source only, installs nothing, calls no network service, and
deletes nothing. `.yml` forms are written in JSON syntax, which is valid YAML;
this makes local structural validation possible with Python's standard library.
It checks local links and fragment targets, form structure, the policy budgets,
source size, static site asset links, and fixed Action commit references.

It does **not** certify external link availability, browser behavior, legal
compatibility, current GitHub settings, downstream inheritance, or a deployed site.
Those require the corresponding review or live check, with evidence in the PR.
