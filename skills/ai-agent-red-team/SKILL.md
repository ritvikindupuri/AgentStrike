---
name: ai-agent-red-team
description: >-
  Use this when red teaming an AI-powered or agentic app (LLM app, agent, tool
  use, MCP, RAG) from its GitHub repo against STRIDE, OWASP LLM Top 10, and
  OWASP Agentic threats.
---
# AI agent red team workflow
Scope: only AI-powered and agentic apps. Not general offensive security.

## Rules
- Read-only on the repo: no commits, PRs, or issues.
- Local only: never attack live deployments or contact external hosts, never use real cloud credentials.
- Never print secret values; report file locations only.
- Keep usage lean: one target at a time, give the run known leads so it doesn't re-read the whole repo.

## Phases
0. **Inventory**: list the owner's repos, flag the AI/agent apps, rank by risk (autonomous actions, cloud write access, tool execution).
1. **Recon**: map the LLM calls, prompts, tools, MCP servers, RAG sources, auth, and where untrusted data enters the prompt.
2. **Threat model**: STRIDE plus OWASP LLM Top 10 (LLM01-LLM10) plus OWASP Agentic (tool misuse, privilege compromise, memory poisoning, excessive agency).
3. **Attack**: write concrete payloads tied to code paths (direct and indirect prompt injection, tool-arg injection, SSRF/scope bypass, approval bypass, output-handling XSS/beacons, secret exfil). Verify statically or with local harnesses only.
4. **Report**: write a markdown report.
5. **Retest**: after fixes, recheck each finding and mark fixed / open.

If running in a cloud agent, open its page in the browser right away so the owner can watch live.

## Report format (chat and file)
- Header: target link, counts by severity, safety line.
- Sections by severity with IDs (C1, H1, M1, L1).
- Each finding: title, STRIDE + OWASP tags, `file:line` evidence, payload in a code block, one-line fix.
- Controls that held.
- Fix order.
- Short bullets, no walls of text.
