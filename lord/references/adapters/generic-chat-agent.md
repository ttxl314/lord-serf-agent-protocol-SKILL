# Generic Chat Agent Adapter

Use for agents that can receive only text, a few attachments, or ordinary chat context.

## Dispatch Requirements

- The launch instruction must be self-contained.
- Clearly list files the user must upload.
- Do not assume the agent can read the project directory.
- Do not use internal links visible only to the current master software.
- Provide the formal task file as an attachment or paste it in full.
- Require the result as a complete Markdown handoff report.

## Output Limits

If the agent cannot directly create files, require it to:

1. Provide the output body first.
2. Then output the full suggested handoff file.
3. Clearly list the files actually reviewed.
