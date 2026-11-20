# Cross-Application Handoff

## 1. You May Be the Receiving Application

Another application produced the task package. The file is authoritative; your chat is ephemeral.

## 2. Check Before Working

Confirm, and quote back:

- `task_id` and `task_version` you read.
- The path you read them from.
- That inputs, boundaries, acceptance criteria, and `submission_path` are all present.

If the transport dropped files or truncated the package, submit `BLOCKED` with reason `handoff`.

## 3. Write Only Where You Can

- Write `submission_path` when the workspace allows it.
- Otherwise return the inline YAML report and state `report_path: inline`.
- Never write the authoritative state source, even when you can reach it.

## 4. Return the Report the Way You Received the Work

Use `handoff.return_transport` from the dispatch instruction when it provides one, and name the transport in your first chat line so Lord can verify arrival.

## 5. Version Drift

If the package you hold differs from the version Lord names, stop and submit `BLOCKED`. Do not upgrade, downgrade, or merge versions yourself.
