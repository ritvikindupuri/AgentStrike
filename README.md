# <img src="assets/icon.svg" alt="" width="40"> AgentStrike

**AI agent red team. The review is read-only. Fixes open a pull request only if you ask.**

AgentStrike is a Grok Bot (an AI assistant built on the Grok Bot app, by Cursor) that red teams AI-powered and agentic applications from their GitHub repositories. It covers LLM apps, agents, tool use, MCP, and RAG, and it scores what it finds against STRIDE, the OWASP Top 10 for LLM Applications 2025, and OWASP Agentic threats (tool misuse, privilege compromise, memory poisoning, excessive agency).

It does not do general offensive security. Phases 0 through 4, and the retest, never commit, open a pull request, or open an issue. They never call a live deployment or any other external host, never use real cloud credentials, and never print a secret value. When a check needs a concrete payload, that payload is tied to a code path and checked by reading the code or with a local harness that stays inside the workspace.

After the report, you can say `fix C1, H1`. That opt-in Fix phase launches a cloud agent that opens a pull request on a new branch for each finding, or for a severity group. The diff is minimal, a regression test or local harness shows the payload now fails, and the finding id is in the pull request title. The agent never merges. You review, and Phase 5 retests against that branch.

The bot launches one Cursor cloud agent on the repository you pick. In the Grok Bot app, open AgentStrike's Computer tab. The box browser there shows the cloud agent run page with its live commands. The bot returns a severity-ranked markdown report. Findings use ids such as C1, H1, M1, and L1, with STRIDE and OWASP tags, `file:line` evidence, the payload in a code block, and a one-line fix. The report also lists controls that held and a fix order.

This repository is the recipe for that bot: the profile, four memories, two skills, the cloud-agent prompt, and an empty report skeleton. [`template/agentstrike-template.json`](template/agentstrike-template.json) is the recipe reference. Open the AgentStrike Bot template link, or create the bot by hand from these files.

## Key features

- **AI and agent scope only.** LLM apps, agents, tool use, MCP, and RAG. Other kinds of security work are out of scope.
- **Phases 0 through 5, plus an opt-in fix.** Inventory, recon, threat model, attack, report, then an optional fix, then retest.
- **Read-only until you ask for a fix.** Phases 0 through 4, and the retest, do not commit, open a pull request, or open an issue. A fix pull request is opened only when you name the findings, and you merge it yourself.
- **Opt-in fix PRs.** Say `fix C1, H1`. A cloud agent opens one pull request per finding, or per severity group, on a new branch. The title carries the finding id. The body states the finding, the root cause, the change, and how it was verified. The agent never merges.
- **Local only.** No live hosts, no real cloud credentials, and secret values are never printed. The report names the file and line.
- **One target at a time.** The cloud agent gets the known leads, so it does not re-read the whole tree.
- **Live view.** In the Grok Bot app, open AgentStrike's Computer tab. The box browser there shows the cloud agent run page with its live commands.
- **One report shape.** Severity sections, tags, evidence, payloads, one-line fixes, controls that held, and a fix order.
- **A public template.** Profile, memories, skills, and a getting-started skill. No routines and no plugins.

## System architecture

<p align="center">
  <img src="assets/architecture.png" alt="How AgentStrike works" width="900">
</p>
You ask AgentStrike. The bot launches a Cursor cloud agent, the central step, drawn with the Cursor logo. That agent reads the GitHub repository. The solid arrow is that read. The dashed arrow is optional: it opens a fix pull request only if you ask. The agent writes the report and sends it to AgentStrike, and AgentStrike delivers it to you. AgentStrike opens the run in the box browser.

1. **You** tell AgentStrike which GitHub owner to look at, or you name one AI or agent app.
2. **AgentStrike**, the Grok Bot, keeps the work inside the AI-only scope, saves your answers, and launches a single read-only run with the known leads. The report comes back here, and AgentStrike delivers it to you.
3. **Cursor Cloud Agent** is the central step. The review uses [`prompts/cloud-agent-redteam-prompt.md`](prompts/cloud-agent-redteam-prompt.md), stays read-only, and does recon, the STRIDE and OWASP threat model, and the attack checks. It writes the report. A fix, when you ask, uses [`prompts/cloud-agent-fix-prompt.md`](prompts/cloud-agent-fix-prompt.md).
4. **GitHub** is the repository. The solid arrow labeled “Reads the code” is the read-only review. The dashed arrow labeled “Opens a fix PR (only if you ask)” is the only write, and only after you name the findings. The agent never merges.
5. **Box browser** is the live-view branch off the cloud agent. AgentStrike opens the run there. In the Grok Bot app, open AgentStrike's Computer tab. The box browser there shows the cloud agent run page with its live commands.
6. **Report** goes from the Cursor cloud agent to AgentStrike, then from AgentStrike to you. You get severity counts, tagged findings, evidence, payloads, fixes, controls that held, and a fix order. The report ends with “Say 'fix C1, H1' to open fix PRs.” After a fix pull request exists, Phase 5 retests those ids on that branch.

## Tech stack

- **Grok Bot app.** The bot profile, memories, skills, the getting-started skill, and the box browser.
- **Cursor cloud agents.** One read-only run per target, and an optional fix run that opens pull requests and does not merge. Both prompts are in this repo.
- **GitHub.** The inventory of your repositories, the source the cloud agent reads, and the pull requests the fix run opens.
- **Box desktop browser.** In the Grok Bot app, AgentStrike's Computer tab shows this browser. The page in it is the cloud agent run, with its live commands.
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

Grok Bot shares bots as a Bot template link, not as a JSON file import. [`template/agentstrike-template.json`](template/agentstrike-template.json) is the recipe reference. It records the profile name and description, the four memories, both skills, and `gettingStarted` set to `agentstrike-getting-started`. Routines and plugins are empty.

Open the AgentStrike Bot template link if you have one. The bot's getting-started skill runs on the first chat.

Otherwise, create a new bot by hand and add the memories and skills from this repo:

1. Name the bot **AgentStrike**.
2. Paste the profile description from the JSON.
3. Add the four memories, using each `title` and `text`: AI-only scope, red-teamer report format, auto-open live runs in the box browser, and keep usage lean.
4. Add the two skills from the files below. The getting-started skill must be the one that runs on the first conversation.
   - [`skills/ai-agent-red-team/SKILL.md`](skills/ai-agent-red-team/SKILL.md)
   - [`skills/agentstrike-getting-started/SKILL.md`](skills/agentstrike-getting-started/SKILL.md)
5. Leave routines and plugins empty.

### 3. Connect GitHub

Open the new bot’s chat and let the getting-started skill ask its first question, or ask it to connect GitHub. Approve the connection card when it appears, and grant access to the repositories you want inventoried. Read access is enough for the review. Opening fix pull requests later needs permission to push a branch and open a pull request. The bot still never merges.

### 4. Confirm cloud agents

Cursor cloud agents have to be available on the same account. You do not start one yourself for the first run. AgentStrike launches a single read-only agent and opens it in the box browser.

### Files in this repo

| Path | What it is |
|------|------------|
| `template/agentstrike-template.json` | Bot profile, memories, skills, getting-started skill. No routines or plugins. |
| `skills/ai-agent-red-team/SKILL.md` | The workflow, including the opt-in Fix phase, and the report rules. |
| `skills/agentstrike-getting-started/SKILL.md` | The first conversation. |
| `prompts/cloud-agent-redteam-prompt.md` | The read-only prompt the cloud agent runs under for the review and the retest. |
| `prompts/cloud-agent-fix-prompt.md` | The opt-in prompt that opens fix pull requests. It never merges. |
| `templates/report-template.md` | Empty report shape. Every finding in it is an example placeholder. |
| `assets/icon.svg` and `assets/icon.png` | Official mark: a red rounded blob with two white eyes. |
| `assets/architecture.svg` and `assets/architecture.png` | The figure above. |
| `scripts/build_architecture.py` | Rebuilds the figure. |

## Usage guide

The interaction is the chat, plus two places you look: the GitHub connection card, and AgentStrike's Computer tab in the Grok Bot app. The steps below are the whole loop, from the first question to sharing the template.

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

The bot launches one Cursor cloud agent with the prompt in [`prompts/cloud-agent-redteam-prompt.md`](prompts/cloud-agent-redteam-prompt.md). That prompt stays read-only: no commits, pull requests, or issues; no live hosts; no real cloud credentials; never print a secret value. A fix is a later run, with [`prompts/cloud-agent-fix-prompt.md`](prompts/cloud-agent-fix-prompt.md), and only if you name the findings.

Phases on the read-only run:

1. **Recon.** Map LLM calls, prompts, tools, MCP servers, RAG sources, auth, and untrusted input. Cite `file:line`.
2. **Threat model.** STRIDE, OWASP LLM01–LLM10 (2025), and the agentic tags where the path is an agent.
3. **Attack.** Payloads tied to those code paths. Checked by reading the code, or with a local harness that does not use the network.
4. **Report.** The markdown shape in [`templates/report-template.md`](templates/report-template.md). It closes with “Say 'fix C1, H1' to open fix PRs.”
5. **Retest.** Only when you ask, and only for the ids you name, against the fix pull request branch or the default branch after you merge.

### 6. Watch the Computer tab

When the run starts, AgentStrike opens it in the box browser. That is the live-view branch in the figure.

1. In the Grok Bot app, open AgentStrike's Computer tab. The box browser there shows the cloud agent run page with its live commands.
2. Watch the commands as they run. You should see reads of the target repo, not pushes, and not requests to a deployed URL.
3. If a command is heading at a live host, an external service, or a write to the repo, stop the run on that page and tell the bot: `Stop. That run tried to leave the repo. Start it again read-only.`

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

### 8. Open fix PRs (optional)

Skip this if you would rather edit the code yourself. The review that produced the report stays read-only.

1. In AgentStrike's chat, name the findings. Example: `fix C1, H1`.
   - One pull request per finding is the default.
   - For one pull request that covers a severity group, say so: `fix C1 and H1 in one pull request.`
2. AgentStrike launches a cloud agent with [`prompts/cloud-agent-fix-prompt.md`](prompts/cloud-agent-fix-prompt.md). In the Grok Bot app, open AgentStrike's Computer tab and watch the run. You should see a new branch, a small diff, and a test or local harness. You should not see a merge.
3. Open the pull request on GitHub when the run returns the link. The title includes the finding id, for example `fix(C1): ...`.
4. Review the diff. Confirm it is limited to that finding. Read the pull request body: finding, root cause, change, and verification. Run the test or harness locally if you want a second look. The payload from the report should now fail.
5. Ask for a retest on that branch before you merge. Example: `Retest C1 and H1 on the fix pull request branch.`
6. Merge the pull request yourself after the retest. AgentStrike does not merge.

### 9. Fix, then retest

You can also change the code yourself. Either way, you review and you merge.

When the fixes are on the branch you want checked:

`Retest C1, H1, and M1 on octocat/example-agent at the fix pull request branch.`

After you have merged, you can point the retest at the default branch instead.

Phase 5 rechecks those ids only and marks each one **fixed** or **open**. It uses the read-only prompt. It should not start a new hunt unless you ask. An open item keeps its id. A fixed item says what changed, with a new `file:line`.

To retest everything from the last report: `Retest every open finding from the last report on the fix pull request branch.`

### 10. Another target

`Inventory again and pick the next AI app, skipping anything we already reported.`

The off-limits list still applies. Live view still follows the preference you saved.

### 11. Share the template

In AgentStrike's chat, ask:

`give me your bot template`

It packs a shareable Bot template, which you confirm and publish.

[`template/agentstrike-template.json`](template/agentstrike-template.json) is the recipe reference for what that template contains. Do not put real findings, secret values, or personal data into the template when you share it.
