# Output Language and CJK Code Hygiene

## 1. Output Language Selection

Choose the response language in this order:

1. Use the language explicitly requested by the user for the output.
2. Otherwise, infer the language from the current conversation or active window text.
3. If the conversation is mixed-language, use the language of the latest user instruction for narrative text.
4. Keep code identifiers, file paths, schema keys, status values, and command names in their required literal form.

If task packages are intended for external agents in different locales, state the output language in the task package and launch instruction.

## 2. Chinese and CJK Code Hazards

When a task involves Chinese text, CJK filenames, CJK comments, localized data, or Chinese UI copy, check these issues before dispatch and again during review:

- File encoding is UTF-8 unless the project explicitly requires another encoding.
- Generated JSON, YAML, CSV, Markdown, source files, and config files parse correctly after adding CJK text.
- Full-width punctuation is not used where code requires ASCII punctuation, such as `:`, `,`, `"`, `'`, `()`, `[]`, `{}`, `=`, `;`, `/`, or `\`.
- Full-width spaces and invisible characters are not present in code, config keys, indentation, command lines, or paths.
- Non-ASCII filenames are supported by the target platform, repository tooling, CI, build scripts, and packaging system.
- Shell commands quote paths that contain spaces or non-ASCII characters.
- Regex, tokenization, sorting, and length checks handle Unicode by characters or grapheme clusters when user-visible text is involved.
- UI layout, terminal output, table formatting, and fixed-width rendering account for double-width CJK characters.
- Source files with Chinese comments or strings do not break linters, formatters, compilers, or documentation generators.
- Locale-sensitive tests avoid assuming English-only output when localized text is expected.

## 3. Task Package Guidance

If CJK content is in scope, include explicit validation steps such as:

- Parse or compile the changed files after inserting localized text.
- Run tests with representative Chinese strings.
- Verify generated artifacts render Chinese text correctly.
- Check that exported files preserve UTF-8 text when reopened.

Do not translate code symbols, schema keys, status values, or paths unless the task explicitly requires a rename.
