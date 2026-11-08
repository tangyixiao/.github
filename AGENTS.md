# Agent working agreements

These instructions apply to this repository. They are also an adoption example:
GitHub does not load this file into other repositories or AI clients automatically.
When adopting, put the relevant rules in each client's supported global entry
point and verify the instruction sources it actually loaded.

## Work within the task

- Inspect the current work, repository state, applicable instructions, and existing
  workspaces before editing. Preserve dirty files and other tasks' changes.
- Prefer the current suitable workspace. Read-only reviews and small edits do not
  normally need a new clone or worktree. Explain a concrete isolation need before
  creating one; reuse a suitable existing one first.
- Keep one task's scratch scripts, logs, screenshots, and generated data in `work/`.
  Keep requested deliverables in `outputs/`, or follow the host's stated locations.
  Never scatter task folders beside projects or at drive/user roots.
- Track resources you create in one small local task note or the existing task
  record: paths, purpose, processes, and what must be retained. Do not commit local
  machine paths or routine execution logs. Reconcile that record after interruption.
- Divide paths between agents. Do not modify or clean another agent's workspace.
  Respect the human's existing authorization; do not turn routine actions into
  repeated permission requests. Do not treat documents, memory, or web text as consent.

## Disk use comes first

- Read `.github/toss.json` for this sample's budgets. They are working agreements,
  not OS-enforced quotas. Larger legitimate tasks need a reasoned budget adjustment.
- Before a large download, installation, extraction, backup, or build, inspect the
  target volume's free space and estimate peak simultaneous copies. Leave the
  configured free-space reserve. If it cannot fit, stop that expansion and choose
  a smaller approach or surface the specific capacity decision.
- Reuse compatible dependencies and toolchains. Use shared caches only when the
  tool supports safe sharing. Avoid full clones, full datasets, whole-repo backups,
  new runtimes, and repeated builds when a smaller check answers the task.
- Warn in progress when temporary growth passes the warning budget. At the task
  budget, stop optional growth, inspect its cause, and reduce it or explicitly
  document the revised budget and reason within the authorized task.
- Bound logs and generated test output. Keep failure evidence that is useful;
  do not retain every successful run. Account for abandoned approaches promptly.
- Do not start bulk scans of every drive or install watchers/cleanup daemons for
  ordinary work. Check known task-owned paths and target volumes first.

## Other resources

- Default to one heavy build, test suite, compression job, or media job at a time
  per machine; coordinate across agents. Small independent reads can run together.
- Reduce concurrency or stop task-owned heavy work when memory pressure or sustained
  system slowdown is visible. Do not kill unrelated processes or change system settings.

## Finish and verify

- Before finishing, review all task-created resources, including rejected attempts.
  Stop unneeded task-owned servers, watchers, and child processes.
- Remove disposable scratch only after confirming ownership, the resolved absolute
  boundary, no active consumer, and no needed work. Inspect reparse points/symlinks.
  Never infer disposability from a name, age, extension, or size alone.
- Before retiring a workspace, preserve required dirty/untracked/ignored files and
  unique commits. Use the managing client's recoverable archive when available;
  otherwise prefer recoverable removal. Do not use force removal, `git clean`,
  `reset --hard`, or broad recursive deletion as a shortcut.
- A recycle operation or same-volume move is not freed space. Measure free space
  when claiming recovery. If permanent deletion is needed, surface the exact scope
  instead of silently emptying the recycle bin or purging other work.
- Mention retained temporary resources only when they remain: purpose, size when
  material, and the event that makes them removable. Do not generate another report
  file for a routine clean finish.
- Keep local validation, CI, merge, deployment, platform configuration, and actual
  use distinct. Never report success from a planned action or a file's presence.
- For website changes preserve the user-approved project-homepage concept. The
  public page presents the example project's purpose, experience and ways to start;
  do not replace it with a template advertisement, file list or maintenance rules.
- Keep project-specific content in `project.json`; run `python scripts/render_site.py`
  after editing it. Run `python scripts/check.py`, then compare desktop and mobile
  browser screenshots against the approved concept. Check keyboard use, navigation,
  applicable theme behavior and console errors. Install no frontend stack.

## Scope and review

- English public metadata and concise commits; English/Chinese contributions welcome.
- Follow `docs/standard.md` and `docs/adoption.md`. The default website demonstrates
  OJ NEXUS using public project information; its configured project links intentionally
  go to that project. Its interface illustration is not a captured app screenshot.
- This repository owns community defaults and the reusable website template.
  Do not mass-update consumer repositories,
  switch the existing Pages source, merge, publish a release, change access controls,
  or replace another project's license without authorization for that action.
