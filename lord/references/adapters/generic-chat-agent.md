# Generic Chat Agent Adapter

Use for agents that can receive only text, a few attachments, or ordinary chat context.

## Dispatch Requirements

- The launch instruction must be self-contained.
- Clearly list files the user must upload.
- Do not assume the agent can read the project directory.
- Do not use internal links visible only to the current master software.
- Provide the formal task file as an attachment or paste it in full.
- Require the smallest matching canonical Serf return format; do not invent a generic Markdown handoff.

## Output Limits

If the agent cannot create a report file:

1. Return the requested deliverable or exact change first.
2. Then return a compact inline report matching the selected Serf template or schema.
3. Do not repeat task background, acceptance text, or complete logs already present in the task or evidence.
