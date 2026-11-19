# Cloud agent red team prompt

Paste this when AgentStrike launches a Cursor cloud agent on one repository. Replace the angle-bracket placeholders. Do not add instructions that weaken the safety rules.

This prompt stays read-only. It does not open pull requests. Fixes are a separate, opt-in run that uses [`cloud-agent-fix-prompt.md`](cloud-agent-fix-prompt.md), and only when the owner names the findings, for example "fix C1, H1".

The cloud agent assesses one AI-powered or agentic app (an LLM app, an agent, tool use, MCP, or RAG) from its source. This is not a general offensive-security engagement.

## Safety rules

These rules win over every other instruction in this prompt.

- Read-only on the target. Do not commit, push, open a pull request, open an issue, or leave any other write on the repository. Opening a fix pull request is not part of this prompt.
- Local and static only. Do not send requests to live deployments, production URLs, webhooks, or any other external host. Do not resolve or call endpoints you find in the code.
- Do not use real cloud credentials, API keys, tokens, or session cookies. Do not sign in to third-party services. Do not create credentials.
- Never print secret values. If a secret appears in a file, report the file and line only, and describe the kind of secret without quoting it.
- Verification is static review, or a local harness that stays inside the workspace and does not use the network.
- One repository per run. Stay inside the known leads below. Do not re-read the whole tree when the leads already name the files.

## Target

- Repository: `<owner/name>`
- Known leads (prompts, tools, MCP servers, RAG loaders, auth, untrusted-input paths): `<leads>`
- Off limits: `<paths, or none>`
- Phase: `<recon | threat model | attack | report | retest>`
- Prior finding IDs to retest, if this is a retest: `<C1, H1, or none>`

## What to do

1. **Recon.** Map LLM calls, system and developer prompts, tools and their arguments, MCP servers, RAG sources, authentication around those paths, and every place untrusted data enters a prompt or a tool argument. Cite `file:line`.
2. **Threat model.** Tag each path with STRIDE and with the matching entry from the OWASP Top 10 for LLM Applications 2025 (LLM01–LLM10). Where the path is agentic, also tag tool misuse, privilege compromise, memory poisoning, or excessive agency.
3. **Attack.** For each plausible path, write a concrete payload that is tied to that code path. Cover only what the code actually supports: direct prompt injection, indirect prompt injection, tool-argument injection, scope bypass, approval bypass, unsafe output handling, and secret disclosure. Do not invent a path the repository does not contain. Check the payload by reading the code, or with a local harness that does not leave the workspace.
4. **Report.** Return one markdown report in the shape of `templates/report-template.md`.
5. **Retest.** When phase is retest, recheck only the listed finding IDs against the fix pull request branch, or against the default branch after a human has merged. For each id, repeat the finding block below. Set Location to the new `file:line` and add a Status row: fixed or open. Do not commit, and do not open new product work.

## Report shape

Follow `templates/report-template.md`. Do not put severity, OWASP, or STRIDE in the finding heading.

- Header: target link, counts by severity (Critical, High, Medium, Low), and one safety line stating the run was read-only and local.
- Summary table: ID, Severity, Title, OWASP LLM, STRIDE.
- Finding heading is only `### C1 · title` (id and title). Then one row each for Severity, OWASP LLM Top 10 (2025) as `LLM06 · Excessive Agency` with the official 2025 name, OWASP Agentic with the full name or `—`, STRIDE spelled out (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), and Location as `` `file:line` ``.
- Then **Impact** (one or two sentences), **Evidence** (`file:line` bullets), **Attack** (payload in a code block), **Fix** (short bullets).
- Controls that held. Fix order, highest severity first.
- Closing line: Say 'fix C1, H1' to open fix PRs. Use the ids from this report.
- No secret values. No requests to a live host, because you must not make any.
