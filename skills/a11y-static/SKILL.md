---
name: a11y-static
description: Static code analysis for KWCAG2.2 accessibility and semantic HTML. Reads source files and evaluates all 33 KWCAG items plus semantic HTML patterns without requiring a dev server or browser. Called by the a11y orchestrator or usable standalone. Use when asked for static-only accessibility analysis without browser verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Evaluates web source code against KWCAG2.2 (Korean Web Content Accessibility Guidelines) 33 items
and semantic HTML patterns using static analysis only. No dev server or browser required —
this skill works purely from reading source code.
</Purpose>

<Instructions>

## Reference Document

Read before review:

```
references/kwcag22.md
```

Contains the full 33-item criteria table with compliance criteria, error types, detection patterns, and fix guides.

---

## Input

This skill accepts a list of target files. When called by the accessibility orchestrator,
the file list is passed directly. For standalone use, determine scope via:

```bash
git diff --name-only HEAD
```

Filter to web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`

---

## Code Review (per file)

Read each target file, then evaluate **all 33 items simultaneously** per file to minimize repeated reads.

### Auto-Detection (O) — Direct code inspection

| Item | Detection Pattern |
| --- | --- |
| 1. Alternative Text (대체 텍스트) | `<img>` missing alt, `<input type="image">` missing alt |
| 7. Auto-play (자동 재생) | `autoplay` attribute used without control |
| 11. Focus Visible (초점 표시) | `outline: none/0` without replacement style |
| 17. Skip Navigation (반복 영역 건너뛰기) | Missing skip nav link (`href="#main"`) |
| 25. Language of Page (기본 언어 표시) | `<html>` missing `lang` attribute |
| 29. Label in Name (레이블 제공) | `<input>` missing `<label>`, `aria-label`, or `title` |
| 32. Parsing (마크업 오류) | Duplicate `id`, invalid tag nesting |

### Contextual Judgment (△) — Claude interprets code meaning

| Item | Evaluation Criteria |
| --- | --- |
| 1. Alt Text Quality (대체 텍스트 품질) | Does alt text actually describe the image content? |
| 3. Table Structure (표의 구성) | Is `<table>` data or layout? Appropriate `<caption>`/`<th>`? |
| 8. Contrast (명도 대비) | Check CSS `color`/`background-color` values if explicitly set |
| 10. Keyboard Access (키보드 사용) | Non-interactive elements like `<div onClick>` lacking keyboard access |
| 13. Character Key Shortcuts (문자 단축키) | Single-character key event handlers present |
| 18. Page Title (제목 제공) | `<title>` content appropriateness, heading hierarchy logic |
| 19. Link Purpose (링크 텍스트) | "더보기", "클릭", empty links, etc. |
| 22. Pointer Cancellation (포인터 입력 취소) | `onMouseDown` immediate execution pattern |
| 23. Label and Name (레이블과 네임) | Icon buttons missing `aria-label` |
| 26. Change on Request (사용자 요구 실행) | `<select onChange>` auto-navigation pattern |
| 28. Error Suggestion (오류 정정) | Form validation missing error messages and focus management |
| 33. Web App Accessibility (웹앱 접근성) | Custom components missing ARIA role/state |

### Manual Verification (X) — Present as checklist

These items cannot be fully determined from code alone. Report what can be inferred
and mark the rest as requiring runtime verification.

| Item | What to check |
| --- | --- |
| 2. Captions (자막) | `<video>` with `<track>` or transcript |
| 6. Use of Color (색 구분) | Color alone conveying information |
| 9. Visual Presentation (콘텐츠 구분) | Visual design separation |
| 15. Pause, Stop, Hide (정지 기능) | Auto-cycling content |
| 16. Seizures (깜박임) | Flashing 3-50 times/sec |
| 20. Location (참조 위치) | E-publication context |
| 27. Help (도움 정보) | Help/FAQ location consistency |

---

## Semantic HTML Review

Beyond KWCAG2.2, evaluate whether HTML elements are used semantically.

### Directly Detectable

| Check Item | Detection Pattern | Recommended Alternative |
| --- | --- | --- |
| Presentational tags | `<b>`, `<i>` used alone | `<strong>`, `<em>` or CSS |
| Paragraph via line breaks | Consecutive `<br><br>` | `<p>` tag |
| Inline wrapping block content | `<span>` containing block content | `<div>` or semantic element |

### Context-Dependent

| Check Item | Evaluation Criteria |
| --- | --- |
| Missing landmarks | All `<div>` with no `<header>`, `<main>`, `<footer>`, `<nav>` |
| Section structure | Independent content blocks using only `<div>` instead of `<article>`/`<section>` |
| Complementary content | Sidebar/related links not using `<aside>` |
| Interactive elements | Clickable `<div>`/`<span>` → should be `<button>` or `<a>` |
| List structure | Repeated items as `<div>` → `<ul>`/`<ol>` + `<li>` |
| Form grouping | `<div>`-wrapped form group → `<fieldset>` + `<legend>` |
| Quotations | Quote text not using `<blockquote>`/`<q>` |
| Time/Date | Date display not using `<time datetime="...">` |

> **Judgment rule:** Plain layout divs are fine. Flag as ⚠️ only when a semantically clear region omits an appropriate element.

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
- `➖` N/A: relevant element does not exist

All items must have `verdict_method: "정적분석"`.

</Instructions>
</Skill_Guide>
