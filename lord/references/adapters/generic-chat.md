# Generic Chat Adapter

## Task Package

- Keep the task self-contained when the session cannot read workspace files.
- Attach or paste the task package once.
- Include only required inputs unavailable by reference.
- State that chat is notification and the report is the submission.

## Dispatch

- Use `manual-copy` unless the platform exposes a verifiable launch API.
- Start with `$serf` when skill invocation is supported.
- Provide the expected submission path and matching report template.

## Submission Limits

- Require the smallest canonical Serf report format.
- Do not invent another generic report structure.
- Do not repeat task background, acceptance text, or complete logs already stored in artifacts.
- If the platform cannot save files, allow the compact inline YAML form defined by Serf.
