---
name: ai-agent-red-team
description: >-
  Use this when red teaming an AI-powered or agentic app (LLM app, agent, tool
  use, MCP, RAG) from its GitHub repo against STRIDE, OWASP LLM Top 10, and
  OWASP Agentic threats, and optionally opening fix PRs on request.
---
# AI agent red team workflow
Scope: only AI-powered and agentic apps. Not general offensive security.

## Rules
- Phases 0-4 and 5 are read-only on the repo: no commits, PRs, or issues.
- Only the opt-in Fix phase writes code, and only when the owner names the findings to fix (e.g. "fix C1, H1").
- Never merge a PR yourself; a human reviews and merges.
- Local only: never attack live deployments or contact external hosts, never use real cloud credentials.
- Never print secret values; report file locations only.
- Keep usage lean: one target at a time, give the run known leads so it doesn't re-read the whole repo.

## Phases
0. **Inventory**: list the owner's repos, flag the AI/agent apps, rank by risk (autonomous actions, cloud write access, tool execution).
1. **Recon**: map the LLM calls, prompts, tools, MCP servers, RAG sources, auth, and where untrusted data enters the prompt.
2. **Threat model**: STRIDE plus OWASP LLM Top 10 (LLM01-LLM10) plus OWASP Agentic (tool misuse, privilege compromise, memory poisoning, excessive agency).
3. **Attack**: write concrete payloads tied to code paths (direct and indirect prompt injection, tool-arg injection, SSRF/scope bypass, approval bypass, output-handling XSS/beacons, secret exfil). Verify statically or with local harnesses only.
4. **Report**: write a markdown report.
4.5 **Fix (opt-in)**: only on request. A cloud agent opens a PR on a new branch per finding (or per severity group): minimal diff, a regression test or local harness showing the payload now fails, the finding ID in the title (e.g. "fix(C1): ..."), and a PR body with the finding, root cause, change, and how it was verified. No unrelated refactors. Never merge.
5. **Retest**: rerun each finding's payload against the fix PR branch (or main after merge) and mark fixed / open, with new `file:line`.

If running in a cloud agent, open its page in the browser right away so the owner can watch live.

## Report format (chat and file)
Match `templates/report-template.md`.
- Header: target link, counts by severity, safety line.
- Summary table: ID, Severity, Title, OWASP LLM, STRIDE.
- Heading is only `### C1 · title`. Severity, OWASP LLM Top 10 (2025) with the official name, OWASP Agentic, STRIDE spelled out, and Location (`file:line`) are separate table rows.
- Then Impact, Evidence, Attack (payload in a code block), and Fix.
- Controls that held. Fix order.
- Offer: "Say 'fix C1, H1' to open fix PRs."
- No secret values. Do not jam severity and tags into the heading.
