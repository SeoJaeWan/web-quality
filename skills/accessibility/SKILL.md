---
name: accessibility
description: Web accessibility/web standards review. Reviews changed code against KWCAG2.2 and generates HTML + CSV reports. Invoked via web-quality orchestrator. Not directly triggerable.
model: sonnet
---

<Skill_Guide>
<Purpose>
After completing work, reviews changed web code against KWCAG2.2 (Korean Web Content Accessibility Guidelines) 33 items
and checks semantic HTML compliance, then generates HTML + CSV reports in Korean.

</Purpose>

<Instructions>

## Reference Document

Must read before review:

```
references/kwcag22.md
```

> Path resolved relative to this skill directory (`<plugin-root>/skills/accessibility-review/`).

- Full KWCAG2.2 33-item criteria table
- Each item includes: Compliance Criteria, Error Types, Details, Auto-Detection level, Detection Pattern, Fix Guide

---

## Step 1. Review Scope

When invoked via the quality orchestrator, use the file list passed from it as-is.
Proceed to Step 2.

Standalone execution only:

```bash
git diff --name-only HEAD
```

- Filter changed web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- If changed web files exist → set those files as review targets
- If no changed web files → AskUserQuestion: "Please specify the files or content to review."
- If user specifies a file/scope explicitly → use that instead

---

## Step 2. Load Criteria

Read the full `references/kwcag22.md`.

Identify the **Auto-Detection** level for each of the 33 items:

- `O`: Directly detectable via code pattern → inspect actively
- `△`: Requires Claude's contextual judgment → read and evaluate
- `X`: Requires actual runtime/visual verification → present as checklist

---

## Step 3. Code Review (per file)

Read the target file with Read, then **evaluate all 33 items simultaneously for each file**.
(Minimize repeated file reads)

### Auto-Detection (O) — Direct code inspection

| Item                                     | Detection Pattern                                       |
| ---------------------------------------- | ------------------------------------------------------- |
| 1. Alternative Text (대체 텍스트)        | `<img>` missing alt, `<input type="image">` missing alt |
| 7. Auto-play (자동 재생)                 | `autoplay` attribute used without control               |
| 11. Focus Visible (초점 표시)            | `outline: none/0` without replacement style             |
| 17. Skip Navigation (반복 영역 건너뛰기) | Missing skip nav link (`href="#main"`)                  |
| 25. Language of Page (기본 언어 표시)    | `<html>` missing `lang` attribute                       |
| 29. Label in Name (레이블 제공)          | `<input>` missing `<label>`, `aria-label`, or `title`   |
| 32. Parsing (마크업 오류)                | Duplicate `id`, invalid tag nesting                     |

### Contextual Judgment (△) — Claude interprets code meaning

| Item                                        | Evaluation Criteria                                                   |
| ------------------------------------------- | --------------------------------------------------------------------- |
| 1. Alt Text Quality (대체 텍스트 품질)      | Does alt text actually describe the image content?                    |
| 3. Table Structure (표의 구성)              | Is `<table>` data or layout? Appropriate `<caption>`/`<th>`?          |
| 10. Keyboard Access (키보드 사용)           | Non-interactive elements like `<div onClick>` lacking keyboard access |
| 13. Character Key Shortcuts (문자 단축키)   | Single-character key event handlers present                           |
| 18. Page Title (제목 제공)                  | `<title>` content appropriateness, heading hierarchy logic            |
| 19. Link Purpose (링크 텍스트)              | "더보기", "클릭", empty links, etc.                                   |
| 22. Pointer Cancellation (포인터 입력 취소) | `onMouseDown` immediate execution pattern                             |
| 23. Label and Name (레이블과 네임)          | Icon buttons missing `aria-label`                                     |
| 26. Change on Request (사용자 요구 실행)    | `<select onChange>` auto-navigation pattern                           |
| 28. Error Suggestion (오류 정정)            | Form validation missing error messages and focus management           |
| 33. Web App Accessibility (웹앱 접근성)     | Custom components missing ARIA role/state                             |

### Manual Verification (X) — Present as checklist

| Item                                 | Verification Method                                  |
| ------------------------------------ | ---------------------------------------------------- |
| 2. Captions (자막)                   | Check `<video>` for `<track>` or separate transcript |
| 6. Use of Color (색 구분)            | Directly check if color alone conveys information    |
| 8. Contrast (명도 대비)              | Measure with CCA tool or browser DevTools            |
| 9. Visual Presentation (콘텐츠 구분) | Directly check visual design                         |
| 15. Pause, Stop, Hide (정지 기능)    | Check auto-cycling content behavior                  |
| 16. Seizures (깜박임)                | Check for content flashing 3–50 times per second     |
| 20. Location (참조 위치)             | Check if e-publication document                      |
| 27. Help (도움 정보)                 | Check consistency of help/FAQ location across pages  |

---

### Semantic HTML Review (Web Standards)

Beyond KWCAG2.2, check whether HTML elements are used semantically.

#### Directly Detectable Patterns

| Check Item                    | Detection Pattern                          | Recommended Alternative                     |
| ----------------------------- | ------------------------------------------ | ------------------------------------------- |
| Presentational tags           | `<b>`, `<i>` used alone                    | `<strong>`, `<em>` (when meaningful) or CSS |
| Paragraph via line breaks     | Consecutive `<br><br>`                     | `<p>` tag                                   |
| Inline wrapping block content | `<span>` directly containing block content | `<div>` or semantic element                 |

#### Context-Dependent Patterns

| Check Item            | Evaluation Criteria                                                                |
| --------------------- | ---------------------------------------------------------------------------------- |
| Missing landmarks     | All `<div>` with no `<header>`, `<main>`, `<footer>`, `<nav>`                      |
| Section structure     | Independent content blocks using only `<div>` instead of `<article>` / `<section>` |
| Complementary content | Sidebar/related links area not using `<aside>`                                     |
| Interactive elements  | Clickable `<div>`/`<span>` → can it be replaced with `<button>` or `<a>`?          |
| List structure        | Repeated items as consecutive `<div>` → `<ul>`/`<ol>` + `<li>` recommended         |
| Form grouping         | `<div>`-wrapped form element group → `<fieldset>` + `<legend>` recommended         |
| Quotations            | Quote text not using `<blockquote>` / `<q>`                                        |
| Time/Date             | Date/time display not using `<time datetime="...">`                                |

> **Judgment rule:** Plain layout divs are allowed. Flag as ⚠️ only when a **semantically clear region** omits an appropriate semantic element.

---

## Step 4. Lighthouse Accessibility Verification

Lighthouse CLI uses the axe-core engine to quantitatively verify accessibility items.

### 4-1. Resolve Environment

When invoked via the quality orchestrator, use the passed `lighthouse_available`, `dev_server_url`, and `runtime_probe_reason` values.

Standalone execution — detect directly:

```bash
# ① Resolve dev server URL with the shared resolver
node scripts/resolve-dev-server.mjs

# ② Check Lighthouse CLI
npx lighthouse --version 2>/dev/null || echo "LH_NOT_INSTALLED"
```

- Parse the resolver JSON and use its final `reachable`, `dev_server_url`, and `reason` values.
- Lighthouse not installed or resolver says server unreachable → 10 Lighthouse-target items: keep static analysis result, verdict method = `정적분석`
- Environment ready → proceed to Step 4-2

### 4-2. Run Lighthouse

```bash
npx lighthouse {dev_server_url}{route} \
  --output json \
  --output-path /tmp/lh-a11y-report.json \
  --chrome-flags="--headless=new" \
  --preset=desktop \
  --only-categories=accessibility
```

Infer route from changed files:

- `src/pages/Dashboard.tsx` → `/dashboard`
- `src/app/about/page.tsx` → `/about`
- Cannot infer → use baseURL only (homepage)

### 4-3. Lighthouse Result Mapping

Map Lighthouse audit IDs to KWCAG2.2 items (10 items):

| KWCAG Item | Lighthouse audit ID   | Item Name                      |
| ---------- | --------------------- | ------------------------------ |
| A-01       | `image-alt`           | Alternative Text               |
| A-03       | `th-has-data-cells`   | Table Structure                |
| A-08       | `color-contrast`      | Color Contrast                 |
| A-17       | `bypass`              | Skip Navigation                |
| A-18       | `heading-order`       | Page Title / Heading Hierarchy |
| A-19       | `link-name`           | Link Purpose                   |
| A-23       | `button-name`         | Label and Name                 |
| A-25       | `html-has-lang`       | Language of Page               |
| A-29       | `label`               | Label in Name                  |
| A-32       | `duplicate-id-active` | Parsing / Markup Errors        |

### 4-4. Interpret Lighthouse Results

Extract `audits[audit_id]` from JSON:

```
score: 1 → ✅ Pass
score: 0 → ❌ Fail (extract failingElements from details.items)
score: null → ➖ N/A (element not present)
```

For ❌ results, extract the specific failing element's selector and snippet from `details.items` and include in the issue description.

### 4-5. Cross-Validation (Lighthouse vs Static Analysis)

**When Lighthouse and static analysis results differ → Lighthouse takes precedence.**
Lighthouse analyzes the actual rendered DOM, making it more accurate than static analysis.

- Lighthouse ❌ but static ✅ → **❌** (Lighthouse wins, verdict: `Lighthouse`)
- Lighthouse ✅ but static ❌ → **✅** (Lighthouse wins, verdict: `Lighthouse`)
- Both agree → use that result (verdict: `Lighthouse`)
- Lighthouse not run → keep static analysis result (verdict: `정적분석`)

---

## Step 5. Browser Interaction Verification (agent-browser)

agent-browser CLI verifies **interaction-based items** in a real browser — keyboard navigation,
focus movement, ARIA state changes, duplicate IDs, etc. It complements Lighthouse by covering
dynamic behaviors that Lighthouse cannot detect.

Why agent-browser over Playwright MCP: each Playwright MCP tool call returns the full
accessibility tree (~2-5K tokens per snapshot), and keyboard testing requires ~10 round-trips.
agent-browser chains all commands in a single Bash call, drastically reducing token usage.

### 5-1. Resolve Environment

When invoked via the quality orchestrator, use the passed `browser_available`, `dev_server_url`, and `runtime_probe_reason` values.

Standalone execution — detect directly:

```bash
# ① Dev server check
node scripts/resolve-dev-server.mjs

# ② agent-browser availability (npx handles install automatically)
npx agent-browser --version 2>/dev/null || echo "AB_NOT_AVAILABLE"
```

- Dev server unreachable or agent-browser unavailable → browser-target items: `🔵 판정불가` (state reason)
- Both ready → proceed to Step 5-2

### 5-2. Determine Target URL

When invoked via the quality orchestrator, use the passed `dev_server_url`.

Standalone resolution order:

1. Use the `dev_server_url` returned by `node scripts/resolve-dev-server.mjs`
2. Infer route from changed files
3. If route inference fails, use the base URL returned by the resolver as-is

### 5-3. Browser Verification Targets

| KWCAG Item | What to Verify        | Verification Technique                            |
| ---------- | --------------------- | ------------------------------------------------- |
| A-10       | Keyboard operability  | Tab key focus traversal (up to 5 times)           |
| A-11       | Focus visible         | Check focus style via JS eval after Tab           |
| A-12       | Focus order           | Check focus moves to modal/popup on open          |
| A-26       | Change on request     | Check select onChange auto-navigation             |
| A-28       | Error suggestion      | Check error message + focus after form submit     |
| A-31       | Consistent navigation | Check persistent navigation after page transition |
| A-33       | Web app accessibility | Check ARIA state changes after interaction        |

### 5-4. A-10 + A-11: Keyboard Accessibility & Focus Visible

Run keyboard traversal and focus style check in a **single chained command**.
The `-i -c` flags produce a compact, interactive-elements-only snapshot — this keeps
output small and token-efficient.

```bash
npx agent-browser open {URL} \
  && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser eval "(() => { const f = document.activeElement; const s = getComputedStyle(f); return JSON.stringify({tag:f.tagName,outline:s.outline,boxShadow:s.boxShadow,border:s.border}); })()"
```

Compare snapshots to see which elements received focus:

- A-10: All interactive elements reachable via Tab → `✅` / No focus movement or trap → `❌` / Partial → `⚠️`
- A-11: outline/boxShadow/border shows visual change → `✅` / No visual indicator → `❌`

### 5-5. A-32: Duplicate ID Verification

Static analysis suspects duplicate IDs → confirm with actual DOM count:

```bash
npx agent-browser eval "document.querySelectorAll('[id]').length + ' total, duplicates: ' + JSON.stringify([...new Set([...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i))])"
```

### 5-6. A-33: Web App Accessibility (ARIA State)

Check ARIA state changes before/after interaction in a single chain:

```bash
npx agent-browser snapshot -i -c \
  && npx agent-browser click "@eN" \
  && npx agent-browser snapshot -i -c
```

Replace `@eN` with the element reference from the first snapshot (e.g., hamburger button, filter toggle).
Compare the two snapshots for ARIA attribute changes:

- `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed` changes → `✅`
- No state change (static ARIA) → `⚠️`
- No interactive elements found → `➖`

### 5-7. Cross-Validation

When browser verification and static analysis results differ → **browser result takes precedence**.
Verdict method column: `Playwright` (keep this label for report consistency with KWCAG standards)

---

## Step 6. Classify Results

| Result        | Meaning                                                                                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `✅`          | Pass: no violation found                                                                                                                                                              |
| `❌`          | Fail: violation found (include filename:line)                                                                                                                                         |
| `⚠️`          | Advisory: no violation but improvement recommended                                                                                                                                    |
| `➖`          | N/A: the relevant element does not exist                                                                                                                                              |
| `🔵 판정불가` | Runtime verification not possible — must state specific reason: Lighthouse not installed / Playwright not available / Browser not installed / resolver could not reach the dev server |

---

## Step 7. Generate and Save Reports

Save the same review results in **2 formats**.

> **Note:** When invoked via the quality orchestrator, skip this step.
> Return result data only to the orchestrator.
> The steps below apply to standalone execution only.

### Output Files

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_DIR="reports/accessibility/${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"
```

- `${REPORT_DIR}/report.html` — visual HTML report
- `${REPORT_DIR}/report.csv` — CSV for documentation/spreadsheet use

Reuse the same directory for re-runs within the same minute (no suffix needed).

### HTML Report Requirements

- Result colors: `✅` (green #28a745), `❌` (red #dc3545), `⚠️` (yellow #ffc107), `➖` (gray #6c757d), `🔵 판정불가` (blue #6c8ebf)
- Structure: summary table → detailed results by principle → semantic HTML review → fix guide
- Language: Korean / Style: inline CSS only (no external dependencies)
- Verdict method column values: `정적분석` / `Lighthouse` / `Playwright` / `판정불가`

### CSV Report Requirements

- Header: `번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드`
- Include all 33 KWCAG items + all semantic HTML items
- Special character escaping: wrap cells containing commas or newlines in double-quotes; escape internal double-quotes as `""`

---

## Step 8. Verify Results

1. Confirm all 33 KWCAG2.2 items have been evaluated — none skipped.
2. Confirm the Semantic HTML section (7 items) has been evaluated.
3. Every ❌ result must include: KWCAG item number, filename + line number or pattern, concrete violation description.
4. Every ⚠️ result must include a specific improvement recommendation.
5. Items marked 🔵 판정불가 must state specific reason: Lighthouse not installed / Playwright not available / Browser not installed / resolver could not reach the dev server.
6. Confirm both `reports/accessibility/YYYYMMDD-HHmm/report.html` and `reports/accessibility/YYYYMMDD-HHmm/report.csv` have been written (standalone mode only).
7. If any condition above is not met, do not claim completion — identify what is missing and resolve it.

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:

- Result colors: `✅` (green #28a745), `❌` (red #dc3545), `⚠️` (yellow #ffc107), `➖` (gray #6c757d), `🔵 판정불가` (blue #6c8ebf)
- Structure: summary table → detailed results by principle → semantic HTML review → fix guide
- Language: Korean / Style: inline CSS only (no external dependencies)
- Verdict method column: `정적분석` / `Lighthouse` / `Playwright` / `판정불가`
- CSV header: `번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드`
- Include all 33 KWCAG items + all semantic HTML items

</Output_Format>
</Skill_Guide>
