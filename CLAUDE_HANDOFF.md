# Prep Atlas: Claude / Codex handoff

## Latest checkpoint: 2026-10-02 (Claude)

User instructions now: finish ALL remaining archive files, then give every question a clear, detailed solution (new Solution tab). Make the site look good without overdoing it. Add Next navigation. No C++. **Agent limit: at most 2, announced first, smaller models for light work.**

- **Running:** exactly 2 Sonnet workers (A and B), following `build/WORKER_SPEC.md`. They write `build/reviewed_auto_A*.py` / `B*.py` (auto-imported by `curate_local.py`), then add solutions for older questions in `build/solutions/A_*.json` / `B_*.json` (merged by id in `build_site_data.py`). Logs: `build/worker_A_log.md`, `build/worker_B_log.md`. Solution code checks: `build/solution_checks/`.
- **New pipeline helpers:** `build/coverage.py` (remaining files), `build/ocr_dump.py` (OCR text of uncovered files), `build/find_similar.py` (pattern-dedupe search), `alias(existing_id, company, files)` in `curate_local.py` (repeat attached to any public id).
- **Pause switch:** `PAUSE_WORK.cmd` creates `build/PAUSE`; workers stop cleanly at the next step. `RESUME_WORK.cmd` removes it. An hourly session cron (:17) resumes stopped workers when no PAUSE flag is set. The usage meter can't be read from the session (credential access is blocked), so the user pauses near 90%.
- **Redesign done:** new `site/styles.css` (paper or near-black themes, ink-blue accent, per-track colours, 15px body), self-hosted fonts (`site/vendor/fonts/`), highlight.js. In `app.js`: topic chips per bank; Solution tab with a try-first gate, copy buttons and "Load into editor"; answer-sheet MCQ bubbles with correct/wrong marking; Next/Previous bar using the list context (sessionStorage) plus next-topic jump; Next CTA after a correct answer or passing checks; N/P keys. Screenshots: `python build/snap_redesign.py` → `build/qa/redesign/`.
- **DONE (2026-10-02 morning):** both workers finished; no agents or cron jobs running. **All 1,320/1,320 files covered**. **752 questions** (DSA 241, aptitude 219, ML 173, CS 119), **every one with a detailed `solution`**. The 251 scripts in `build/solution_checks/` all pass on a re-run. `test_site.py` and `test_site_edges.py` both PASS; tests were updated for the 252px sidebar and the scrolling topic strip, and the solved ✓ moved to CSS. `build_site_data.py` has a per-id `SAMPLE_EMAILS` allow-list (the IBM email-regex sample data). Caveats live in question notes and solutions: ~7 low-confidence items from cropped photos, a few printed answer keys disputed in the solution, and paraphrased web-DSA prompts with the stated interpretation.
- **Still open:** hosting/audience decision (publish `site/` only).

Checkpoint: 2026-10-01, Asia/Calcutta. Workspace: `C:\My Stuff\Placement_Prep`.

## User intent and working rules

Continue the shared placement-preparation site using the 52-company target scope, local OA screenshots/documents and saved research. Tracks: DSA, AI/ML (engineering, applied scientist and research), aptitude and CS. Keep material variants; merge repeats. Include explanations, LC/CF links, Python/NumPy practice, filters, notes/progress, themes and honest collection-frequency labels. Present a coherent product, without user-facing phases.

User migrated from Claude after usage limits and plans to return after reset. NEVER launch assistants without announcing their exact number. Latest allowance: ONE assistant if needed; zero by default. One was announced and used this turn (`browser_checks`); it finished. No other assistants were used. Ordinary Python extraction/testing processes are not agents.

User chose to keep the laptop awake and resume local work. Cloud transfer was discussed but canceled; NO cloud task, Git repository or deployment was created. Public versus batchmates-only access remains unanswered. Do not publish private sources.

## Current working product

Visit http://127.0.0.1:8765. `START_PREP.cmd` launches `python serve.py --open`; the browser opens after binding. Serve ONLY `site/`, never the workspace. Direct file opening cannot run workers.

- Four searchable banks; company/topic/difficulty/status/origin and ML-role filters; 20-row pagination; company-wide views; topic/company counts; reports and coverage table.
- Problem/approach/notes tabs; MCQ/numeric checking; local browser code/stdin/notes/status; progress export/import preserves newer local records and ignores unknown IDs. No accounts or cross-device sync.
- Python 3.12 / NumPy 1.26.4 in a Pyodide 0.26.4 worker; Ace editor, stdin, errors, Stop, 10-second execution timeout, 64 KB output cap, 90-second first-load cap. No Torch/C++/Java.
- Local Marked 15.0.12, DOMPurify 3.2.6, Ace 1.43.3 and KaTeX 0.16.22/fonts. Vendor source URLs are recorded, including KaTeX.
- Mobile overview overflow fixed using constrained grid columns and wrapping. Dark/mobile views were inspected. Company-wide breadcrumb fixed. Cold-load Stop/restart race fixed and tested.
- Most-asked ranks represented companies per topic in this collection, not hiring-wide frequency.

Current payload: **399 questions**: DSA 112, aptitude 65, CS 49, ML 173. Origins: local 206, web 182, original practice 11. Fifteen executable exercises, four attached to local prompts. **537/1,320 source files contribute questions or explicit skips.** All 253 Oracle files are now accounted for, including duplicates and skips. This is NOT a claim that all pages/problems are fully reconstructed; explicit skips and solution-only PDFs still have gaps. Review remains the largest unfinished task. User was given a rough **6?10 more hours** for full archive review/final checks, subject to unclear sources; this is not a guaranteed finish time.

## Extraction: complete

`python build/extract_sources.py --audit`: **1,320/1,320 valid records, zero errors/missing/invalid**. Full and focused Oracle OCR workers finished. Reran the current extractor to rebuild a complete index: zero new files required. No extraction is currently needed unless new sources are added.

The hardened extractor validates source identity and JSON before reusing a cache, writes per-file/index JSON atomically, lazily loads OCR, uses exclusive per-file PID locks, and avoids saving interrupted partial work. `--audit`, `--company`, `--limit`, `--retry-errors` are supported. Verify owner process before removing a stale lock. Cache hashes use SHA-256 of manifest-relative path, first 20 hex characters. OCR/QA remain private.

Local server PID was 32204 at this checkpoint. Confirm command lines before acting; PIDs can be reused:

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Select-Object ProcessId,CommandLine
```

Laptop sleep suspends local execution; shutdown ends it. Nothing has moved to cloud.

## Content pipeline and continuation

- `build/manifest.json`: 49 companies with 1,320 files. Three additional targets without local files: Navi, Samsung SRIB, Turing.
- Original six `build/raw/` batches contain 39 questions. `b06` has 21 processed references but no questions. Do NOT count `processed_files` alone as reviewed.
- `build/curate_local.py` plus `reviewed_batch2.py` through `reviewed_batch15.py`: **167 reviewed additions**, source of truth for generated `build/raw/curated_local.json`. Stable IDs begin `curated-local-`. Helpers: add, merge, skip; merge explicitly attaches repeats/company aliases. Edit generators, not generated JSON.
- Initial additions cover Fractal, Axtria, Arpwood, Expedia, Adobe, Cadence, IBM, Oracle, HP and HiLabs. Later groups add Apple, Motorq, Meesho, DE Shaw, Microsoft, Myntra, Mastercard and more Oracle. Carefully marked cropped constraints, contradictory samples/options, and wrong candidate selections. Preserve these caveats; screenshots are not official answer keys.
- `build/source_sheet.py COMPANY --offset N --limit N`: private source review images in `build/qa/source-review/`. Offset counts images only, not PDF/document entries; do not assume a uniform offset into the manifest. Oracle sheets 1?63 were visually inspected. Four PDFs were read; both MCQ PDFs primarily repeat reviewed photos. Two coding PDFs contain solution-only entries whose missing prompts and buggy code are recorded in private `build/oracle_solution_review.md`. Oracle unresolved skips include diagrams, historical versions, named cloud services, ambiguous reading-comprehension options and a mismatched number-wheel/language prompt.
- Batch8 adds networking, OS, SQL and intelligent substrings; batch9 adds alternating-parity partitions and minimax clustering; batch10 recovers the modular exponent, phone chart, pollution ranks and three-letter subsequence count. Batch11 merges PDF repeats, qualifies i386 system calls, handles incomplete partition DDL, verifies Redis classification, explains animal survival/composition ambiguity, and separately labels a downward-tree-path reconstruction. Do not erase source caveats or grade ambiguous choices. `resolve()` removes only explicitly handled skip records.
- `build/build_site_data.py`: compile raw/research/outlines/practice; strip source paths/private notes; validate IDs/sections/email leakage; merge identical statements and explicit ML aliases. Counts question/skip file references, not all OCR. Raw sources are never served.
- `research/`: three saved reports and post-title index. Preserve historical/community/snippet limitations. Title-only posts are not full transcriptions.
- `build/practice.py`: 15 references, 208 cases. Four practice interfaces attach to histogram, distinct-cover window, prefix-kth and rod-cutting. Original standalone tasks include NumPy ML/math. `build/outlines.py` supplies labelled preparation outlines rather than official answers.

Rebuild after edits:

```powershell
python build/curate_local.py
python build/build_site_data.py
```

## Verification and remaining work

Passed: 15 reference exercises/208 cases; `build/verify_batch15.py` **2,250 independent comparisons** (booster permutations, outlier role indices, parcel compositions, literal pattern intersections and discount pairs); `build/verify_batch13.py` **2,556 independent comparisons** (whole-state swap shortest paths, literal power-product parity, all meeting orders, exhaustive festival positions); `build/verify_batch12.py` **12,601 independent comparisons** plus targeted grid final-jump/blocked-cell cases; `build/verify_reviewed.py` **19,972 independent comparisons** (normalization, bounded distinct moves, colored tiles, GF(2) groups, digit swaps, OR removal, weighted panels, return route, elimination, any/downward tree paths, alternating partitions, minimax clusters and repeated-letter subsequence counts); `build/test_extraction_cache.py` interruption/corrupt-cache recovery; compileall. Tree checks include all-negative 100,000-node chains and shuffled node labels.

`build/test_site.py` passed at the 382-question checkpoint. Assistant's `build/test_site_edges.py` passed cold-load Stop/restart, actual 10-second timeout/recovery, all 15 references in browser, backup merge/validation/export, settled mobile geometry. Dark/mobile screenshots were readable. The edge suite passed again at the 382-question checkpoint, including all browser reference cases and the actual timeout. Avoid full suite repetition after every data-only batch.

Next: continue full archive review outside Oracle (783 files not yet represented), then revisit explicit skips where new evidence resolves them. Do not claim archive curation is complete. Check public content/schema/privacy and run final browser verification after material changes. User may steer scope/timing while work continues. Resolve audience/hosting before deployment; publish ONLY site folder.

Launcher improvement: `serve.py` now binds Windows sockets exclusively, preventing two Python servers sharing port 8765. `--open` checks an already-running loopback server against this workspace?s index and reopens it. A mocked-browser repeat-launch check passed without starting another server. The temporary `python -` test PID 33560 was stopped; original site PID 32204 was preserved. No OCR jobs or extra agents are running. Batch12 adds eight coding prompts from all 20 files of BNY Mellon, Zepto, ThoughtSpot and Visa, with two explicit Zepto coin-problem skips for the missing statement. Private contact sheets were visually inspected. ThoughtSpot?s final-jump length-one rule was recovered visually after OCR omitted it. Qualcomm?s one source is a full VLSI textbook, not an OA; review its scope separately rather than bulk-importing textbook exercises. Confirm process identity before acting.

Batch13 reviews all 18 Atlassian photos into two prompts: power-product parity (exponent bounds cropped; positive and zero cases distinguished), and minimum-cost height multiset balancing. The latter recovers an Oracle solution-only gap. Batch14 reviews all ten LinkedIn photos: two new prompts (positive meeting prefixes and weighted Manhattan medians), with identical server-assignment photos explicitly merged into the Meesho question. All these contact sheets were visually inspected. No source paths were copied to public content.

Batch15 reviews all 30 Amazon source images into five coding prompts: capable winners, discounted pairs, pairwise pattern intersection wildcards, parcel load and largest outlier. Private contact sheets 1?8 were visually inspected. Repeated screenshots are attached rather than adding repeated questions. Partial numerical constraints remain marked as missing. All new algorithm checks and compileall passed; the last full browser suite was at 382 questions, with subsequent changes confined to content generators/tests/docs. No extraction jobs are active.
