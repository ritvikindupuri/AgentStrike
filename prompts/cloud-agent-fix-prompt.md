# Cloud agent fix prompt

Paste this when AgentStrike launches a Cursor cloud agent to fix findings the owner named. Replace the angle-bracket placeholders. Do not add instructions that weaken the safety rules.

This is the opt-in Fix phase. The red team prompt in `prompts/cloud-agent-redteam-prompt.md` stays read-only. Use this prompt only after the owner says which findings to fix, for example "fix C1, H1".

## Safety rules

These rules win over every other instruction in this prompt.

- Write code only for the findings named below. Do not fix, refactor, or restyle anything else.
- Open a pull request on a new branch. Do not merge it. A human reviews the diff and merges.
- Do not push to the default branch. Do not open an issue. Do not close or edit existing pull requests unless the owner asked you to update one you just opened.
- One pull request per finding, unless the owner asked for one pull request per severity group. Do not bundle unrelated findings.
- The diff stays minimal. No drive-by refactors, formatting sweeps, or dependency bumps.
- Add a regression test, or a local harness, that runs the original payload and shows it now fails. The check stays inside the workspace and does not use the network.
- Do not send requests to live deployments, production URLs, webhooks, or any other external host.
- Do not use real cloud credentials, API keys, tokens, or session cookies. Do not create credentials.
- Never print secret values. If a secret is in a file, name the file and line only.

## Target

- Repository: `<owner/name>`
- Findings to fix: `<C1, H1>`
- Base branch: `<branch the pull request should target>`
- How to group the pull requests: `<one PR per finding | one PR per severity group>`
- Finding notes (id, file:line, payload, one-line fix): `<paste from the report>`

## What to do

1. Read each named finding. Use its `file:line`, payload, and one-line fix. Do not invent a finding that is not in the list.
2. Create a new branch from the base branch. Name it for the finding, for example `fix/c1-short-slug`. For a severity group, name the branch for that group.
3. Make the smallest change that closes that finding.
4. Add a regression test or a local harness. Run it. The original payload must fail closed: the unsafe behavior must not happen.
5. Open a pull request into the base branch.
   - Title includes the finding id, for example `fix(C1): keep untrusted text out of the system prompt`. A group uses each id, for example `fix(C1, H1): ...`.
   - Body has four parts: **Finding** (id, what was wrong, `file:line`), **Root cause**, **Change** (what the diff does), **Verification** (the test or harness, and the result).
6. Stop. Do not merge. Return the pull request link. Phase 5 retests against this branch, and a human merges after review.
