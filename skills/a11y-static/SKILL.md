---
name: a11y-static
description: Static code analysis for KWCAG2.2 accessibility and semantic HTML. Runs a bundled scan script for mechanical detection, then applies contextual judgment for nuanced items. No dev server or browser required. Called by the a11y orchestrator or usable standalone. Use when asked for static-only accessibility analysis without browser verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Evaluates web source code against KWCAG2.2 (33 items) and semantic HTML using a two-phase approach:
1. **Script scan** — mechanical pattern detection (zero LLM tokens)
2. **LLM review** — contextual judgment on candidates the script flags

This combination catches more issues than either alone while keeping token usage low.
Runtime-dependent items (video playback, visual rendering, multi-page consistency) are
delegated to a11y-browser — this skill handles only what's determinable from source code.
</Purpose>

<Instructions>

## Step 1. Determine Target Files

When called by the orchestrator, the file list is passed directly. For standalone use:

```bash
git diff --name-only HEAD
```

Filter to web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`

---

## Step 2. Run Scan Script

Execute the bundled scanner on all target files. The script detects issues in two severity levels:
- **error**: definitive violations (missing alt, duplicate id, missing lang, etc.)
- **candidate**: patterns that need contextual judgment (icon buttons, vague link text, etc.)

```bash
python3 scripts/scan.py {file1} {file2} ...
```

The script outputs JSON with `summary` and `findings` arrays. Parse the output.

---

## Step 3. Contextual Review

Read each target file **once** and do two things simultaneously:

1. **Judge script candidates** — the script flags patterns as "candidate" when it can't
   determine context (e.g., is this image decorative? is this div genuinely interactive?).
   For each candidate, decide: true issue (❌/⚠️) or false positive (dismiss).

2. **Spot additional issues** — while reading the code, note any accessibility problems
   the script couldn't detect (ARIA misuse, missing aria-expanded on toggles, icon buttons
   without labels, etc.). Don't exhaustively check every KWCAG item — just flag what you
   naturally notice in the code. The script already handles the mechanical checks.

The goal is efficiency: trust the script for pattern matching, add human judgment only
where needed. Do NOT iterate through all 33 items one by one.

---

## Step 4. Fix Guide Lookup

For items judged as `❌` or `⚠️`, read the fix guide from:

```
references/kwcag22.md
```

Include the specific fix recommendation in the output. Only read this file when
violations are found — skip it if everything passes.

---

## Step 5. Compile Results

Merge script errors + LLM-judged candidates + code-only checks into a single result set.

### Semantic HTML Review

The script also flags semantic HTML issues (S-01 through S-07). Review these candidates
and add any additional semantic issues noticed while reading the code:

| Check | What to look for |
| --- | --- |
| Missing landmarks | All `<div>` with no `<header>`, `<main>`, `<footer>`, `<nav>` |
| Section structure | Content blocks using only `<div>` instead of `<article>`/`<section>` |
| Interactive elements | Clickable `<div>`/`<span>` → should be `<button>` or `<a>` |
| List structure | Repeated items as `<div>` → `<ul>`/`<ol>` + `<li>` |
| Form grouping | Related form fields → `<fieldset>` + `<legend>` |

> **Judgment rule:** Plain layout divs are fine. Flag as ⚠️ only when a semantically
> clear region omits an appropriate element.

---

## Output Format

**Only output items with issues** (❌ or ⚠️). Passing items (✅) and N/A items (➖) are
omitted — the purpose is to surface problems, not confirm what's fine. This dramatically
reduces output size and keeps the focus on actionable findings.

Return a JSON object with a summary and findings array:

```json
{
  "summary": {
    "files_reviewed": ["page.tsx", "StatsCard.tsx"],
    "total_items_checked": 40,
    "violations": 3,
    "advisories": 2
  },
  "findings": [
    {
      "id": "A-01",
      "name": "대체 텍스트",
      "result": "❌",
      "verdict_method": "정적분석",
      "issue": "page.tsx:83 — <img> missing alt attribute",
      "fix_guide": "Add descriptive alt text: <img alt=\"대시보드 통계 아이콘\">"
    }
  ]
}
```

- `findings` contains only ❌ (violation) and ⚠️ (advisory) items
- Semantic HTML items use IDs like `S-01`, `S-02`, etc.
- All items must have `verdict_method: "정적분석"`
- If no issues found, return empty `findings: []` with the summary

</Instructions>
</Skill_Guide>
