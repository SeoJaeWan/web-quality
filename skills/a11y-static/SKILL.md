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

Read each target file and review the script's **candidate** findings. The script can detect
structural patterns but can't judge meaning — that's where LLM judgment adds value.

For each candidate, determine the actual verdict:

| Candidate Pattern | What to Judge |
| --- | --- |
| A-01 empty alt on image | Is the image decorative (alt="" correct) or meaningful (needs description)? |
| A-03 table without caption/th | Is it a data table (needs structure) or layout table (OK without)? |
| A-10 div with onClick | Is it genuinely interactive (needs keyboard access) or event delegation? |
| A-13 single char key handler | Does it have modifier key support or focus-scoped activation? |
| A-17 missing skip nav | Is this a page/layout that needs skip nav, or a nested component? |
| A-18 heading skip | Is the skip intentional (component context) or an error? |
| A-19 vague link text | Does surrounding context clarify the link purpose? |
| A-22 onMouseDown | Does it execute critical action on down-event, or is it for drag/scroll? |
| A-23 icon button | Does surrounding context or CSS provide accessible name? |
| A-26 select onChange | Does it auto-navigate, or just filter/update local state? |
| A-28 required without error | Does the framework handle errors at a higher level (e.g., form library)? |
| A-33 role without ARIA | Are the required ARIA attributes provided elsewhere (parent, hook)? |

Also check items the script cannot detect (need code comprehension):
- A-05: Instructions using only color/position references
- A-08: Explicit CSS color/background-color contrast (compute ratio if values are hardcoded)
- A-14: setTimeout/setInterval for session timeout without extension UI
- A-21: Touch gesture handlers without single-pointer alternative
- A-24: DeviceMotion/Orientation handlers without button alternative
- A-30: CAPTCHA without alternative authentication

Items that require runtime/browser verification — mark as `➖ N/A (브라우저 검증 대상)`:
- A-02 (자막), A-04 (선형구조), A-06 (색 구분), A-09 (콘텐츠 구분)
- A-15 (정지 기능), A-16 (깜박임), A-20 (참조 위치), A-27 (도움 정보)

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

Return results as a JSON array. Each item:

```json
{
  "id": "A-01",
  "name": "대체 텍스트",
  "principle": "인식의 용이성",
  "result": "❌",
  "verdict_method": "정적분석",
  "issue": "page.tsx:83 — <img> missing alt attribute",
  "fix_guide": "Add descriptive alt text: <img alt=\"대시보드 통계 아이콘\">"
}
```

Semantic HTML items use IDs like `S-01`, `S-02`, etc.

Classification:
- `✅` Pass: no violation found
- `❌` Fail: violation found (include filename:line)
- `⚠️` Advisory: improvement recommended
- `➖` N/A: relevant element does not exist or item is browser verification target

All items must have `verdict_method: "정적분석"`.

</Instructions>
</Skill_Guide>
