# Parallel Worker Rules

## 1. You Are One of Several

When Lord runs a fan-out, sibling workers hold other task packages in the same workspace.

## 2. Stay in Your Slice

- Touch only `allowed_paths`.
- Do not open, format, or "quickly fix" another worker's files.
- Do not run repo-wide formatters, migrations, or generators that rewrite unrelated files.
- Do not write the authoritative state source.

## 3. Shared Interfaces

A shared interface is frozen for the wave. If your work needs it changed, submit `CHANGE_REQUEST` and state whether you can continue.

## 4. Report Partial Work Honestly

If you must stop mid-way, list the paths you already changed and their state. Lord decides whether to resume, revert, or re-dispatch.

## 5. No Coordination Through Chat

Coordinate only through files and Lord. Do not assume a sibling's result exists because it was mentioned.
