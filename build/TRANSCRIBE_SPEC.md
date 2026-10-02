# Transcription spec — OA screenshots → structured questions

You are turning photos/screenshots of real campus online-assessment (OA) questions into clean, structured data for a shared prep website. Work through every file in your batch, in order.

## Reading files
- Images (.jpg/.jpeg/.png/.webp): open with the Read tool (it shows the image).
- PDFs: Read with `pages` (max 20 pages per call).
- .docx: `python -c "import docx,sys; print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" "<path>"`
- .txt: Read.
- Paths in the batch file are relative to `C:\My Stuff\Placement_Prep\`.
- Files are sorted by name, so consecutive screenshots often continue one question (statement → constraints → examples). Merge them into one entry, listing every file in `source_files`.

## What to keep / skip
- Keep: DSA/coding problems, ML/AI/stats questions, aptitude (quant, logical, verbal, DI), CS fundamentals (OS, DBMS/SQL, networks, OOP, C/C++/Java output), quant puzzles.
- Skip: instructions screens, login pages, blank/irrelevant photos, résumés, offer letters, chat screenshots with no question. Record them in `skipped_files` with a 2–5 word reason.
- **Pattern dedupe inside your batch:** if a question is the same problem (or same pattern with only cosmetic changes — different numbers/names, same trick) as one you already recorded, do NOT add a new entry. Append the file to the existing entry's `source_files` and the company to `also_asked_by` if different. Add a new entry only if the problem is genuinely different (different trick, constraint, or approach).
- **Privacy — mandatory:** never copy candidate names, emails, phone numbers, roll numbers, test/candidate IDs, invite links, or watermarks. Transcribe the question only.

## Output
Maintain ONE JSON file: `C:\My Stuff\Placement_Prep\build\raw\<batch_key>.json`. Rewrite it with the Write tool after every ~10 files so progress survives interruptions. If the file already exists when you start, load it and resume: skip files already listed in `processed_files`.

```json
{
  "batch": "<batch_key>",
  "processed_files": ["..."],
  "skipped_files": [{"file": "...", "reason": "login screen"}],
  "questions": [ { ...question... } ]
}
```

Question object (omit fields that don't apply; never invent data you can't see — mark gaps in `notes`):
```json
{
  "id": "<batch_key>-001",
  "company": "Oracle",
  "also_asked_by": [],
  "role": "SDE | DS | Analyst | Intern | ... (only if visible)",
  "year": "2024 (only if visible)",
  "section": "dsa | ml | aptitude | cs",
  "subsection": "see list below",
  "topics": ["graph", "bfs"],
  "pattern": "short canonical pattern name, e.g. 'multi-source BFS on grid', 'relative speed of trains', 'precision vs recall trade-off'",
  "difficulty": "easy-medium | hard",
  "type": "coding | mcq | numeric | subjective | sql",
  "title": "Short descriptive title",
  "statement": "Full cleaned problem statement in Markdown. Use $...$ for math. Rewrite garbled OCR into correct English but keep the meaning exact.",
  "input_format": "...", "output_format": "...", "constraints": "...",
  "function_signature": "if the OA gave a function stub, its signature + language",
  "examples": [{"input": "exact text", "output": "exact text", "explanation": "..."}],
  "options": ["A text", "B text", "C text", "D text"],
  "answer": "correct option/value",
  "answer_source": "screenshot | solved",
  "answer_confidence": "high | medium | low",
  "explanation": "MCQ/aptitude: short working (2–6 lines). Coding: approach in 2–5 lines + time/space complexity.",
  "leetcode": {"name": "Closest LeetCode/Codeforces problem", "url": "https://...", "similarity": "same | similar"},
  "source_files": ["relative/path.jpg"],
  "notes": "e.g. 'constraints cropped', 'example 2 unreadable'"
}
```

Subsections:
- dsa: arrays, strings, hashing, two-pointers, sliding-window, binary-search, sorting, greedy, stack-queue, linked-list, trees, bst, heap, graphs, dp, backtracking, bit-manipulation, math, matrix, design, simulation
- ml: ml-theory, stats-probability, deep-learning, llm-genai, ml-coding, ml-system-design, data-analysis
- aptitude: quant, logical, verbal, data-interpretation, puzzles
- cs: os, dbms, sql, networks, oop, c-cpp-output, java-output, python-output, digital-electronics, computer-architecture, software-engineering, general-cs

Difficulty: "easy-medium" = standard/LeetCode easy-medium or routine aptitude; "hard" = LeetCode hard-level, multi-step tricky, or unusually time-consuming.

Answers: if the screenshot shows the answer, use it (`answer_source: screenshot`). Otherwise solve it yourself for MCQ/numeric/aptitude/CS (`answer_source: solved`, with honest confidence). For coding, give the approach in `explanation`; don't write full code.

## When done
Make sure the JSON file is complete and valid (run `python -c "import json;json.load(open(r'<path>',encoding='utf-8'))"`). Your final message: counts only — files processed, files skipped, questions recorded, breakdown by section, and anything notable (e.g. a company whose files were mostly unreadable). Don't paste questions into the final message.
