---
name: a11y
description: Web accessibility/web standards review. Reviews changed code against KWCAG2.2 and generates HTML + CSV reports. Orchestrates a11y-static (code analysis) and a11y-browser (live browser verification), then merges results into a unified report. Use when asked to review accessibility, 접근성 검토, a11y 체크, 웹표준 확인, KWCAG, or any web accessibility audit.
model: sonnet
---

<Skill_Guide>
<Purpose>
Orchestrates a complete KWCAG2.2 accessibility review by coordinating two sub-skills:
- **a11y-static**: Script-based scan + LLM contextual judgment on source code
- **a11y-browser**: Live browser verification (interaction, visual rendering, runtime items)

Both sub-skills return **only issues** (violations and advisories) — passing items are omitted.
The orchestrator merges findings, resolves conflicts, and generates issue-focused reports.
</Purpose>

<Instructions>

## Step 1. Review Scope

Determine the files to review:

```bash
git diff --name-only HEAD
```

Filter to web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`

- Changed web files exist → set as review targets
- No changed web files → ask user to specify
- User specifies explicitly → use that

---

## Step 2. Run Sub-Skills

Read and follow each sub-skill's SKILL.md. Both sub-skills return JSON with
`summary` (counts) and `findings` (issues only — ❌, ⚠️, 🔵).

### 2-1. Static Analysis

Read `../a11y-static/SKILL.md` and follow its instructions with the target files.
This always runs — it has no external dependencies.

### 2-2. Browser Verification

Read `../a11y-browser/SKILL.md` and follow its instructions with the target files.
This handles dev server startup and agent-browser verification automatically.

If browser verification fails entirely (no dev server, no agent-browser), the orchestrator
proceeds with static analysis results only.

---

## Step 3. Merge Findings

Both sub-skills return only items with issues. Merge them by item ID.

### Merge Rules

1. **Same item found by both**: browser result takes precedence (rendered DOM is
   the source of truth over source code patterns).

2. **Item found only by static**: keep as-is with verdict_method = `정적분석`.

3. **Item found only by browser**: keep as-is with verdict_method = `브라우저 검증`.

4. **Browser 🔵 판정불가**: if browser couldn't verify an item but static found
   an issue, use the static result.

5. **No issues at all**: if both sub-skills return empty findings, the code is clean.

---

## Step 4. Generate Reports

Save results in 2 formats. Reports show **only issues** — no need to list passing items.

### Output Files

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_DIR="reports/accessibility/${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"
```

- `${REPORT_DIR}/report.html`
- `${REPORT_DIR}/report.csv`

### HTML Report

Read `references/output-format.md` for the full template.

Key structure:
- **Summary**: total items checked, violations count, advisories count
- **Findings**: only ❌ and ⚠️ items, grouped by principle, with file:line and fix guide
- **판정불가**: 🔵 items with reasons (if any)
- Language: Korean / Style: inline CSS only

### CSV Report

- Header: `번호,항목명,결과,판정방식,발견된 문제,수정 가이드`
- **Only rows with issues** (❌, ⚠️, 🔵) — no ✅ or ➖ rows
- Wrap cells with commas/newlines in double-quotes; escape `"` as `""`

---

## Step 5. Verify Quality

1. Every `❌` includes: item number, filename:line, concrete violation
2. Every `⚠️` includes specific improvement recommendation
3. Every `🔵 판정불가` states specific reason
4. Fix guides reference kwcag22.md recommendations
5. Both report.html and report.csv written
6. If no issues found, report states "검토 결과 위반 항목 없음"

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:
- Result colors: `❌` (#dc3545), `⚠️` (#ffc107), `🔵 판정불가` (#6c8ebf)
- Structure: summary → findings by principle → fix guides
- Language: Korean / Style: inline CSS only
- Verdict method: `정적분석` / `브라우저 검증` / `판정불가`

</Output_Format>
</Skill_Guide>
