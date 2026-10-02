# Worker spec: finish the archive + write detailed solutions

Workspace: `C:\My Stuff\Placement_Prep`. Read `CLAUDE_HANDOFF.md` (skim) and look at `build/reviewed_batch15.py` and the top of `build/curate_local.py` (`add`, `merge`, `skip`, `alias`) to see the exact format. Never launch sub-agents. Never edit files owned by the other worker (see "Ownership").

## Job 1: cover every remaining file of your companies

Check progress any time with `python build/coverage.py` (all companies) or `python build/coverage.py "Company"` (remaining files for one company). The job is done when your companies show nothing remaining.

Loop, one company at a time:
1. `python build/ocr_dump.py "Company" --offset 0 --limit 15` prints OCR text + full image path for the next uncovered files (in order; consecutive screenshots usually continue one question). OCR is noisy: **open the image itself with Read whenever numbers, constraints, options, code, formulas or diagrams matter**. That's most coding problems and most MCQs with numbers. Don't guess what you can't read.
2. Before adding, run `python build/find_similar.py "key words"`. Apply the pattern-dedupe rule:
   - Same problem or same pattern with only cosmetic changes (numbers/names/story), where the trick is identical → **don't add**. If the match is in the curated list (`curated-local-…`), call `merge(key, company, [files])`. Otherwise call `alias(existing_id, company, [files])`.
   - Genuinely different trick, constraint or approach → add a new question.
   - Instruction screens, blank or irrelevant photos, résumés, unreadable shots → `skip(company, filename, 'short reason')`.
   - Every file must end up in a question's `sources`, a `merge`/`alias`, or a `skip`. Otherwise coverage won't drop.
3. Write questions in your own module files `build/reviewed_auto_<W>NN.py` (W = your worker letter, NN = 01, 02, …; ~10–25 questions per file). Each module defines `def extend(add, merge, skip, alias): ...`, taking only the helper names you use, as parameters. The filename suffix passed in `sources` must uniquely identify the file within that company. Use the bare filename; `file()` raises if it's ambiguous.
4. Keys must be unique: prefix with a company slug, e.g. `add('uber-coupon-halving', 'Uber', ...)`.
5. After each module: `python build/curate_local.py` then `python build/build_site_data.py`. If a failure comes from the OTHER worker's module, wait a minute and retry. Never edit their file.

### Question fields (`add(key, company, title, statement, answer, explanation, *, ...)`)
- `section`: dsa | ml | aptitude | cs. `topic`: a subsection from `build/TRANSCRIBE_SPEC.md`. `type`: coding | mcq | numeric | subjective | sql. `hard=True` for genuinely hard ones.
- `statement`: full cleaned problem in Markdown, `$…$` for math, fenced code for code. Fix garbled OCR into correct English without changing meaning. Privacy: never copy candidate names, emails, roll numbers, IDs, links or watermarks. Story names in problem text, like "Adarsh", are fine.
- Coding extras: `function_signature`, `input_format`, `output_format`, `constraints`, `examples=[{'input','output','explanation'}]` (exact), `leetcode={'name','url','similarity':'same|similar'}` only when confident.
- MCQ: `options=[...]`, `answer` = exact option text. Numeric: `answer` = value. `confidence='medium'|'low'` when unsure. Use `notes=` for caveats (cropped constraints, contradictory sample, etc.). Preserve honesty.
- `explanation`: the short approach (3–8 sentences, like batch15). Always include it.
- `solution=`: **the detailed solution. Required for every question.** See standards below.

## Job 2: detailed solutions for older questions

After Job 1, write solutions for the existing questions assigned to you (see Ownership) into `build/solutions/<W>_NN.json` as `{"<question id>": "<solution markdown>", ...}` (~15–30 per file). Get ids and statements from `site/data/questions.json` (filter by section; skip ids that already have `solution` or appear in any `build/solutions/*.json`). Rebuild after each file.

## Solution standards (this is what users asked for: clear and detailed, not a one-liner)

Markdown, using these `###` headings in this order where they apply.

**Coding (dsa, ml-coding, sql):**
- `### Intuition`: what the problem is really asking and the key observation, in plain words.
- `### Approach`: numbered steps. For DP, define the state, transition, base cases and answer cell. For greedy, give the exchange argument. For graphs, the modelling.
- `### Why it works`: an invariant or proof sketch, 3–6 lines.
- `### Complexity`: time and space, with a one-line justification.
- `### Python solution`: complete, runnable, commented code matching the stated function signature (or reading stdin per the input format). For SQL, the full query. For ml-coding, NumPy.
- `### Dry run`: trace Example 1 briefly, showing key state changes.
- `### Edge cases & pitfalls`: bullets (overflow, empty input, duplicates, off-by-one, ties, recursion depth…).
- **Verify every coding solution:** save it as `build/solution_checks/<key>.py`, with its function plus asserts on all given examples. For non-trivial algorithms, also add a brute-force comparison on ~200 random small inputs. Run it with python and only publish code that passes. If a sample in the source looks wrong, say so in `notes` and in the solution.

**MCQ / numeric (aptitude, cs, ml MCQs):**
- `### Solution`: full step-by-step working with every intermediate number, ending in **Answer: …**.
- `### Why the other options are wrong`: one line per wrong option (MCQ only).
- `### Faster method`: a shortcut or trick usable under time pressure, if one exists.
- `### Common traps`: 1–3 bullets.
- For code-output questions, trace line by line. For SQL/OS/DBMS/networking, explain the concept behind the answer.

**Subjective / theory (ML theory, system design, behavioural-style technical):**
- Interview-quality answer: definition → intuition → the math (key formulas) → a concrete example → trade-offs and when to use what → `### Likely follow-ups`, with 2–4 short Q→A pairs. ML system design follows: clarify goals and metrics → data and labels → features → model choice → training and evaluation (offline and online) → serving and latency → monitoring and failure modes.

Length guide: coding 250–700 words plus code; MCQ 80–250 words; theory 250–600 words. Be correct before being long. Use `confidence` and `notes` honestly.

## Ownership
- **Worker A** owns companies: IBM, Gameskraft, Uber, Google, Trilogy, PayPal, Dream11, Zscaler, Adobe, Salesforce, Flipkart, Cadence, UBS, Qualcomm, Oracle / Goldman Sachs. Files: `build/reviewed_auto_A*.py`, `build/solutions/A_*.json`, `build/solution_checks/` (own keys). Job 2: existing questions with section **dsa** or **cs**.
- **Worker B** owns companies: ProcDNA, Sigmoid, Fractal, ZS Associates, Axtria, MAQ Software, SAP Labs, PhonePe, UiPath, Deutsche Bank, Groww, Pace Stock Broking, Edelweiss, HP, HiLabs. Files: `build/reviewed_auto_B*.py`, `build/solutions/B_*.json`. Job 2: existing questions with section **ml** or **aptitude**.
- Qualcomm's single source is a VLSI textbook, not an OA: `skip` it with that reason.

## Pause switch (usage limits)
Before starting each new module or solutions file, check whether `build/PAUSE` exists. If it does, make sure everything written so far is saved and rebuilt. Then append `<time> PAUSED at <where you are>` to your log and stop, with the final message `PAUSED`. You'll be resumed later and continue from your log.

## Progress log
Append one line per finished module or solutions file to `build/worker_<W>_log.md`: time, file, questions added, merges/aliases, skips, solutions written, and anything uncertain. This is how work resumes after interruptions. Before starting, read your own log and `coverage.py` to resume, not restart.

## Final message
Counts only: files covered per company, questions added, aliases/merges, skips, solutions written, checks passed, and open issues. No question text.
