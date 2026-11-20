# Changelog

Protocol releases for the Lord and Serf skill pair.

## 0.6.0

The two coordination capabilities become part of the protocol. Field names are unchanged from 0.5; the `protocol_version` constant moves to `"0.6"`, so regenerate unfinished artifacts.

### Added

- Cross-application coordination: `references/cross-application-handoff.md` in both skills, with application slots, a transport ladder, continuity rules, and a failure matrix.
- Intra-application division of labor: `lord/references/intra-app-parallelism.md` and `serf/references/parallel-worker.md`, with fan-out preconditions, single-writer rules, failure isolation, and aggregation.
- Host documentation for Claude Code, Codex, and DSH in both `references/host-runtimes.md`, including per-host write limits and the DeepSeek executor profile.
- Optional `host` and `handoff` objects in the dispatch instruction schema.
- Optional `execution_host` in the submission envelope and both report schemas.
- Rules for duplicate submissions, stale versions, and in-flight task package changes.
- `CHANGELOG.md` and validator checks for template heading structure, reference indexing, coordination assets, optional-field emptiness, CRLF, and release headings.

### Changed

- `protocol_version` is `"0.6"` in every schema, template, and example.
- Report templates no longer embed a Lord command heading; routing lives in chat and is documented once in `serf/references/submission-reporting.md`.
- `worker_invocation` is host-specific free text; `$serf` remains the Codex default.
- Skill descriptions, UI prompts, and README install steps cover all three hosts instead of assuming Codex.
- `TASKS.md` is documented as the small-project state file, distinct from the `TASKS/` package directory.
- Serf may no longer write the authoritative state source under any assignment.

### Fixed

- Three report templates carried two level-one headings, which stored a chat command inside the report file.
- An optional `execution_host` left empty in a template produced a report that failed its own schema.
- The 0.5 note that allowed a stale `REVIEW` after a version bump contradicted the review rules.
