# Working agreement

- Read `CLAUDE_HANDOFF.md` and `README.md` before continuing implementation.
- The user wants to switch between Codex and Claude Code. Preserve working code and maintain a concrete handoff at each stopping point: changes, validation, unfinished tasks and running jobs.
- Never launch extra agents without first telling the user the exact number. Use zero by default; the latest user allowance (2026-10-02) is at most TWO assistant agents, only when necessary, using smaller models for light work. Keep token usage economical. Do not let an assistant spawn more agents.
- Continue the existing placement-preparation product. Do not restart the project or replace its framework without a concrete reason.
- Keep source archives, OCR, candidate details and private QA outside `site/`. Publish only `site/` after the sharing choice is resolved.
- OCR extraction is not question review. Report archive coverage honestly; check source images for uncertain formulas, options and diagrams.
- Edit generators rather than generated content, preserve stable question IDs, and run checks appropriate to the change.
