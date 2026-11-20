# Host Runtimes

## 1. Rule

The Lord/Serf protocol is host-neutral. A host supplies three capabilities, and nothing else about the protocol changes:

- How the `lord` and `serf` skills are loaded and invoked.
- Whether both roles can see the same workspace.
- Whether the host can start an executor without a human action.

Record the host in the dispatch instruction, and never write an invocation form the host does not support.

## 2. Host Matrix

| Host | Skill directory | Invoke | Start an executor |
|---|---|---|---|
| Claude Code | `~/.claude/skills/<name>/` or `.claude/skills/<name>/` | `/lord`, `/serf`, or automatic by description | `Task` subagents |
| Codex | `~/.codex/skills/<name>/` or `.codex/skills/<name>/` | `$lord`, `$serf`; `/skills` lists them | multi-agent subagents where enabled |
| DSH (DeepSeek) | `~/.dsh/skills/<name>/` | the skill name through the `skill` tool | `subagent` or `subagent_fork` |
| Generic chat | paste or attach `SKILL.md` | none | human copy |

`$lord` and `$serf` are Codex shorthand used throughout this repository. On another host, read them as "load the named skill"; field names, status values, submission types, adapter names, and paths never change.

## 3. Claude Code

- Personal skills live in `~/.claude/skills/<name>/SKILL.md`; project skills live in `.claude/skills/<name>/SKILL.md`.
- Claude also loads a skill on its own when the `description` matches the request. `/lord` and `/serf` force it.
- Subagents are native: Lord opens one per task package. A subagent starts without the conversation history, which matches the protocol's no-shared-chat assumption.
- Claude Code accepts extra front matter such as `context: fork`, `agent`, or `allowed-tools`. Keep the shared `SKILL.md` minimal and add those keys only in a local copy when you want forked execution.
- Writes can require approval. A denied or unanswered prompt is a blocker, not a silent skip.

## 4. Codex

- User skills live in `~/.codex/skills/<name>/`; project skills live in `.codex/skills/<name>/`.
- Mention a skill with `$lord` or `$serf`; `/skills` lists what is loaded.
- `agents/openai.yaml` supplies the display name, short description, and default prompt. Codex reads it for the skill listing; other hosts ignore it.
- Recent Codex builds run subagents; older ones do not. When the host cannot start one, dispatch one task per session.
- The sandbox and approval policy decide which paths Serf can write. A blocked write is a blocker, not a reason to move the output somewhere else.

## 5. DSH (DeepSeek)

- Skills live in `~/.dsh/skills/<name>/SKILL.md` and load through the `skill` tool by name. Only the `name` and `description` front matter is read.
- Subagents are `subagent` and `subagent_fork`. The second inherits the parent conversation, so use it only when the task needs that context.
- File writes are workspace-scoped. When `submission_path` falls outside the workspace, the executor returns the inline report instead of forcing a write.
- Executors run DeepSeek models. Write their task packages with the rules in section 8.

## 6. Recording the Host

Optional dispatch instruction block:

```yaml
host:
  agent: dsh              # claude-code | codex | dsh | generic-chat | other
  model: deepseek-flash   # free text
  skill_invocation: 'skill("serf")'
  supports_subagents: true
  shared_workspace: true
```

`host` is additive. A dispatch without it remains valid for protocol 0.6.

## 7. Degradation Order

When a capability is missing, degrade in this order and record the choice:

1. No subagents: dispatch one task per session, sequentially.
2. No shared workspace: use `manual-copy` plus a transport from `references/cross-application-handoff.md`.
3. No skill loading: attach `SKILL.md` itself and keep every literal field name.
4. No file writes: accept the compact inline YAML report and transcribe it into the authoritative state source yourself.

Never emulate a capability that is absent. Claiming a dispatch that never started is a protocol violation.

## 8. Writing Task Packages for DSH and DeepSeek Executors

DSH runs DeepSeek models. Write their task packages so every step is checkable:

- Numbered steps, one action each: `execution_steps` for `standard` or `full`; for `micro`, one objective sentence plus ordered expected outputs.
- Exact paths and copyable commands instead of descriptions.
- Acceptance criteria that a command, file read, or artifact can prove.
- Explicit "do not" lines for scope, paths, and the state source.
- One objective per package; split long multi-goal work into separate tasks.

Avoid vague verbs such as "improve", "clean up", or "handle as appropriate" unless the task also states the checkable result.

The executor-side mirror is `references/host-runtimes.md` in the active Serf skill.
