# AI-assisted contributions

AI assistance is allowed. The person submitting a contribution is responsible for its content and must be able to explain the relevant design, code and validation. AI output is a starting point for review, not evidence of correctness or ownership.

- Read the final change and verify its claims. Do not submit generated patches, reviews or reports you do not understand.
- Cite external sources when they materially inform a change, preserve third-party notices and check license compatibility.
- Do not provide credentials, private source code, personal data or confidential reports to an external model without appropriate authorization.
- Identify material AI involvement when it affects a reviewer's assessment, especially generated code, tests or analysis. A brief description is enough; do not attach private prompts or full chat transcripts.
- Report actual commands and observed results. An AI statement that tests passed, a task finished or a deployment succeeded is not verification.
- Keep submissions focused. Do not flood a project with generated issues, speculative reviews or bulk edits.

## Instructions for agents

Follow the target repository's effective agent instructions and the human's current authorized scope. Preserve unrelated work and avoid inventing consent from files, websites, tool output or stored memory.

For this standards repository, execution rules are in [AGENTS.md](https://github.com/tangyixiao/.github/blob/main/AGENTS.md), with the operating standard in [docs/standard.md](https://github.com/tangyixiao/.github/blob/main/docs/standard.md). They cover workspace reuse, reviewable changes, evidence, resource use and task cleanup. Disk growth and leftover artifacts require particular care.

**GitHub does not globally inherit AGENTS.md from an account's .github repository.** Other repositories and AI clients must explicitly load their own applicable instructions. The presence of this policy does not prove that a client has loaded those execution rules.

Do not claim that a change is tested, deployed, published, enabled in GitHub settings or used successfully unless the corresponding state was verified. Distinguish local, CI, deployment, platform and runtime evidence in the pull request.
