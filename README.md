# <img src="assets/icon.svg" alt="" width="40"> AgentStrike

**AI agent red team, read-only and local only.**

AgentStrike is a Grok Bot (an AI assistant built on the Grok Bot app, by Cursor) that red teams AI-powered and agentic applications from their GitHub repositories. It covers LLM apps, agents, tool use, MCP, and RAG, and it scores what it finds against STRIDE, the OWASP Top 10 for LLM Applications 2025, and OWASP Agentic threats (tool misuse, privilege compromise, memory poisoning, excessive agency).

It does not do general offensive security. A run never commits, opens a pull request, or opens an issue on the target. It never calls a live deployment or any other external host, never uses real cloud credentials, and never prints a secret value. When a check needs a concrete payload, that payload is tied to a code path and checked by reading the code or with a local harness that stays inside the workspace.

The bot launches one Cursor cloud agent on the repository you pick, opens that run in its box browser so you can watch the commands on the Computer tab, and returns a severity-ranked markdown report. Findings use ids such as C1, H1, M1, and L1, with STRIDE and OWASP tags, `file:line` evidence, the payload in a code block, and a one-line fix. The report also lists controls that held and a fix order.

This repository is the public template: the bot profile, four memories, two skills, the cloud-agent prompt, and an empty report skeleton. Import it, or recreate it by hand from the files below.

## Key features

- **AI and agent scope only.** LLM apps, agents, tool use, MCP, and RAG. Other kinds of security work are out of scope.
- **Six phases.** Inventory, recon, threat model, attack, verify and report, then retest after you fix the code.
- **Read-only on the target.** No commits, pull requests, or issues. You merge your own fixes.
- **Local only.** No live hosts, no real cloud credentials, and secret values are never printed. The report names the file and line.
- **One target at a time.** The cloud agent gets the known leads, so it does not re-read the whole tree.
- **Live view.** The run opens in the box browser. You watch commands on the Computer tab.
- **One report shape.** Severity sections, tags, evidence, payloads, one-line fixes, controls that held, and a fix order.
- **A public template.** Profile, memories, skills, and a getting-started skill. No routines and no plugins.

## System architecture

<p align="center">
  <img src="assets/architecture.png" alt="How AgentStrike works" width="900">
</p>
<p align="center"><b>Figure 1. How AgentStrike works</b></p>

You ask AgentStrike. The bot launches a Cursor cloud agent, which is the central step and uses the Cursor logo in the figure. That agent reads the GitHub repository. A live view branches off the cloud agent into the box browser. The report flows back to you.

1. **You** tell AgentStrike which GitHub owner to look at, or you name one AI or agent app.
2. **AgentStrike**, the Grok Bot, keeps the work inside the AI-only scope, saves your answers, and launches a single read-only run with the known leads.
3. **Cursor Cloud Agent** is the central step. It receives the prompt in [`prompts/cloud-agent-redteam-prompt.md`](prompts/cloud-agent-redteam-prompt.md), stays read-only, and does recon, the threat model, and the checks.
4. **GitHub** is the target repository. The agent reads it. It does not push, open a pull request, or open an issue.
5. **Box browser** is the live-view branch. As soon as the run exists, the bot opens it so you can watch the Computer tab. The branch is only a window onto the same run.
6. **Report** flows back. You get severity counts, tagged findings, evidence, payloads, fixes, controls that held, and a fix order. After you change the code, the same loop retests each id.

## Tech stack

- **Grok Bot app.** The bot profile, memories, skills, the getting-started skill, and the box browser.
- **Cursor cloud agents.** One read-only run per target. The prompt they receive is in this repo.
- **GitHub.** The inventory of your repositories, and the source the cloud agent reads.
- **Box desktop browser.** The live run, with commands on the Computer tab.
- **STRIDE.** Spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- **OWASP Top 10 for LLM Applications 2025.** LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption.
- **OWASP Agentic threats used here.** Tool misuse, privilege compromise, memory poisoning, and excessive agency.
- **Markdown.** The report skeleton in [`templates/report-template.md`](templates/report-template.md), and the report the bot writes back.

## Setup instructions

You need a Grok Bot account, a GitHub account, and access to Cursor cloud agents. The bot launches those agents. There is no separate CLI to install for the assessment itself.

### 1. Clone the template

```bash
git clone https://github.com/ritvikindupuri/AgentStrike.git
cd AgentStrike
```

### 2. Create the bot from the template

The recipe is [`template/agentstrike-template.json`](template/agentstrike-template.json). It sets the profile name and description, the four memories, both skills, and `gettingStarted` to `agentstrike-getting-started`. Routines and plugins are empty.

If your Grok Bot app offers a template import, import that file.

If it does not, create a bot by hand and match the file:

1. Name the bot **AgentStrike**.
2. Paste the profile description from the JSON.
3. Add the four memories, using each `title` and `text`: AI-only scope, red-teamer report format, auto-open live runs in the box browser, and keep usage lean.
4. Add the two skills from the files below. The getting-started skill must be the one that runs on the first conversation.
   - [`skills/ai-agent-red-team/SKILL.md`](skills/ai-agent-red-team/SKILL.md)
   - [`skills/agentstrike-getting-started/SKILL.md`](skills/agentstrike-getting-started/SKILL.md)
5. Leave routines and plugins empty.

### 3. Connect GitHub

Open the new bot’s chat and let the getting-started skill ask its first question, or ask it to connect GitHub. Approve the connection card when it appears, and grant access to the repositories you want inventoried. Read access is enough. The bot does not push to those repositories.

### 4. Confirm cloud agents

Cursor cloud agents have to be available on the same account. You do not start one yourself for the first run. AgentStrike launches a single read-only agent and opens it in the box browser.

### Files in this repo

| Path | What it is |
|------|------------|
| `template/agentstrike-template.json` | Bot profile, memories, skills, getting-started skill. No routines or plugins. |
| `skills/ai-agent-red-team/SKILL.md` | The six-phase workflow and the report rules. |
| `skills/agentstrike-getting-started/SKILL.md` | The first conversation. |
| `prompts/cloud-agent-redteam-prompt.md` | The prompt the cloud agent runs under. |
| `templates/report-template.md` | Empty report shape. Every finding in it is an example placeholder. |
| `assets/icon.svg` | Shield and crosshair mark. |
| `assets/architecture.svg` and `assets/architecture.png` | The figure above. |
| `scripts/build_architecture.py` | Rebuilds the figure. |

## Usage guide

The interaction is the chat, plus two places you look: the GitHub connection card, and the Computer tab of the live run. The steps below are the whole loop, from the first question to sharing the template.

### 1. First conversation

Open AgentStrike. The getting-started skill introduces itself in one line: it red teams AI-powered and agentic apps against STRIDE and the OWASP LLM and Agentic standards, read-only and local only.

It then asks **one question at a time**. Answer each one before the next appears.

1. **GitHub owner.** It asks for your GitHub username or org, and whether it should connect GitHub now.
   - Example: `My GitHub username is octocat. Yes, connect GitHub now.`
   - When the connection card appears, approve it. If you are already connected, say so and it will move on.
2. **Where to start.** It asks whether you have a specific app, or whether it should inventory your repos and pick the riskiest AI or agent app.
   - Inventory: `Inventory my repos and pick the riskiest AI app.`
   - One app: `Start with octocat/example-agent. It is an MCP agent.`
3. **Live view.** It asks whether you want to watch runs in its browser. The default is yes.
   - Example: `Yes, open each run so I can watch.`
4. **Off limits.** It asks which repos or paths it must not enter.
   - Example: `Leave octocat/personal-notes alone. Everywhere else in that account is fine.`
   - Or: `Nothing is off limits.`

### 2. What it saves

After the fourth answer it stores three memories of its own, separate from the four template memories:

- The GitHub owner.
- The off-limits list.
- Whether you want the live view.

You can change any of them later in the same chat. Example: `Add octocat/archive to the off-limits list.`

### 3. Phase 0, inventory

If you asked for an inventory, the bot lists repositories for that owner and flags the ones that look like LLM apps, agents, tool use, MCP, or RAG. It ranks them by risk: autonomous actions, cloud write access, and tool execution. It skips anything you marked off limits.

Read the list. Each candidate should say why it was flagged. Repos that are not AI or agent apps are not targets.

If the account has no AI or agent app, it says so and stops. It does not switch to a general security review.

### 4. Pick a target

Either accept the top candidate or name another repo from the list.

- `Use the top one.`
- `Use the second one instead.`
- `Skip that repo. It is a demo with no real tool use.`

The bot keeps a single target. If a run is already open, it finishes or you tell it to stop before it starts another. Example: `Stop the current run. The next target is octocat/example-rag.`

Before the cloud agent starts, the bot should be able to tell you the leads it will pass in: prompt files, tools, MCP servers, RAG loaders, and where untrusted input enters. If it is about to scan the whole tree with no leads, correct it. Example: `The leads are src/agent/ and src/rag/. Do not read the rest.`

### 5. The cloud agent starts

The bot launches one Cursor cloud agent with the prompt in [`prompts/cloud-agent-redteam-prompt.md`](prompts/cloud-agent-redteam-prompt.md). That prompt repeats the safety rules: no commits, pull requests, or issues; no live hosts; no real cloud credentials; never print a secret value.

Phases on that run:

1. **Recon.** Map LLM calls, prompts, tools, MCP servers, RAG sources, auth, and untrusted input. Cite `file:line`.
2. **Threat model.** STRIDE, OWASP LLM01–LLM10 (2025), and the agentic tags where the path is an agent.
3. **Attack.** Payloads tied to those code paths. Checked by reading the code, or with a local harness that does not use the network.
4. **Report.** The markdown shape in [`templates/report-template.md`](templates/report-template.md).
5. **Retest.** Only when you ask, and only for the ids you name.

### 6. Watch the Computer tab

When the run starts, the bot opens it in the box browser. That is the live-view branch in the figure.

1. Bring the box browser forward. The page is the cloud agent run the bot just opened.
2. Open the **Computer** tab on that run.
3. Watch the commands as they run. You should see reads of the target repo, not pushes, and not requests to a deployed URL.
4. If a command is heading at a live host, an external service, or a write to the repo, stop the run in that cloud-agent page and tell the bot: `Stop. That run tried to leave the repo. Start it again read-only.`

You can say `No live view` on a later run if you do not want the browser opened. The assessment still returns the report.

### 7. Read the report

The bot posts the report in chat when the run finishes. Ask for the file if you want a copy you can keep: `Write the report to a markdown file in this chat.`

Read it in this order:

1. **Header.** Target link, counts for Critical, High, Medium, and Low, and a safety line. The safety line should say the run was read-only and local, and that no secret values are included.
2. **Critical, then High, Medium, and Low.** Ids look like `C1`, `H1`, `M1`, `L1`.
3. **Each finding.** Title, STRIDE tag, OWASP tag, `file:line` evidence, a payload in a fenced code block, and one fix line. Open the cited file at that line and confirm the payload matches that path. If the payload is not tied to the code, reject the finding.
4. **Controls that held.** Checks the agent expected to fail that did not. Leave these in place when you fix other items.
5. **Fix order.** Highest severity first. Follow this order unless two fixes touch the same lines, in which case do those together.
6. **Secrets.** A finding may name a file that contains a secret. It must not include the value. If a value appears, treat the report as wrong and tell the bot: `Redact that. Tell me the path only.`

The file [`templates/report-template.md`](templates/report-template.md) shows the shape with placeholder findings only. Those placeholders are not results.

### 8. Fix, then retest

AgentStrike does not edit the target. You change the code, review it, and merge it yourself.

When the fixes are on the branch you want checked:

`Retest C1, H1, and M1 on octocat/example-agent at the current default branch.`

Phase 5 rechecks those ids only and marks each one **fixed** or **open**. It should not start a new hunt unless you ask. An open item keeps its id. A fixed item says what changed, with a new `file:line`.

To retest everything from the last report: `Retest every open finding from the last report.`

### 9. Another target

`Inventory again and pick the next AI app, skipping anything we already reported.`

The off-limits list still applies. Live view still follows the preference you saved.

### 10. Share the template

The public copy of AgentStrike is this repository. To hand it to someone else, send:

`https://github.com/ritvikindupuri/AgentStrike`

They clone it and follow the setup above. The file they import, if their app accepts a template file, is `template/agentstrike-template.json`.

If your Grok Bot app shows a share or export action for a bot, you can use that too. The repository stays the copy that includes the prompt, the report skeleton, and the skills as separate files. Do not put real findings, secret values, or personal data into the template when you share it.
