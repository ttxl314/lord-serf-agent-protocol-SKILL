# Change Control

## 1. Local Adjustments

An external agent may make local adjustments that do not affect public interfaces, overall architecture, shared data structures, shared paths, or other tasks. Record all such adjustments in the handoff.

## 2. Changes Requiring Approval

Submit the following changes to the master agent:

- Public functions, APIs, or call patterns.
- Input/output parameters and data structures.
- Database structures.
- Module boundaries.
- Technical direction or core dependencies.
- Shared configuration and public file paths.
- Modules owned by other agents.
- Replacement of already accepted outputs.

## 3. Required Change Request Contents

- Reason for change.
- Current limitation.
- Proposed approach.
- Alternatives.
- Affected files.
- Affected tasks.
- Rollback plan.
- Whether the change blocks current work.

## 4. Synchronization Requirements

After approval, the master agent should update:

- Architecture or interface files.
- Authoritative task state source.
- Affected task files.
- Change records.
- Downstream agent launch instructions.
