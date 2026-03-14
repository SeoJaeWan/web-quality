---
name: a11y
description: Web accessibility/web standards review. Reviews changed code against KWCAG2.2 and generates HTML + CSV reports. Orchestrates a11y-static (code analysis) and a11y-browser (live browser verification), then merges results into a unified report. Use when asked to review accessibility, 접근성 검토, a11y 체크, 웹표준 확인, KWCAG, or any web accessibility audit.
model: sonnet
---

<Skill_Guide>
<Purpose>
Orchestrates a complete KWCAG2.2 accessibility review by coordinating two sub-skills:
- **a11y-static**: Script-based scan + LLM contextual judgment on source code (code-determinable items)
- **a11y-browser**: Live browser verification (interaction, visual rendering, runtime-dependent items)

a11y-static handles items determinable from code, and delegates runtime-dependent items
(A-02, A-04, A-06, A-09, A-15, A-16, A-20, A-27) to a11y-browser.
Merges results from both, resolves conflicts (browser wins), and generates HTML + CSV reports in Korean.
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

Read and follow each sub-skill's SKILL.md. Both sub-skills accept the same file list
and return JSON arrays of item results.

### 2-1. Static Analysis

Read `../a11y-static/SKILL.md` and follow its instructions with the target files.
This always runs — it has no external dependencies.

### 2-2. Browser Verification

Read `../a11y-browser/SKILL.md` and follow its instructions with the target files.
This handles dev server startup and agent-browser verification automatically.

If browser verification fails entirely (no dev server, no agent-browser), the orchestrator
proceeds with static analysis results only.

---

## Step 3. Merge Results

Both sub-skills return results keyed by KWCAG item ID (A-01 through A-33, plus S-01+ for semantic HTML).

### Merge Rules

1. **Browser-verified items** (verdict_method = `브라우저 검증`): browser result takes precedence
   over static analysis, regardless of whether they agree.

2. **Static-only items**: use as-is with verdict_method = `정적분석`.

3. **Conflict resolution**: if browser says `✅` but static says `❌` → use `✅` (브라우저 검증).
   The rendered DOM is the source of truth over source code patterns.

4. **판정불가 items**: if browser returned `🔵 판정불가` for an item, fall back to the
   static analysis result for that item (verdict_method stays `정적분석`).

### Items Coverage

| Source | Items |
| --- | --- |
| Static analysis | Code-determinable items (A-01, A-03, A-05, A-07, A-08, A-10, A-11, A-13, A-14, A-17, A-18, A-19, A-21, A-22, A-23, A-24, A-25, A-26, A-28, A-29, A-30, A-32, A-33), S-01+ (semantic) |
| Browser verification | Interaction items (A-08, A-10, A-11, A-12, A-26, A-28, A-31, A-32, A-33) + Runtime-only items (A-02, A-04, A-06, A-09, A-15, A-16, A-20, A-27) |
| Static → Browser delegation | A-02, A-04, A-06, A-09, A-15, A-16, A-20, A-27 are marked `➖ N/A (브라우저 검증 대상)` by static, verified by browser |

---

## Step 4. Classify Results

| Result | Meaning |
| --- | --- |
| `✅` | Pass: no violation found |
| `❌` | Fail: violation found (include filename:line) |
| `⚠️` | Advisory: improvement recommended |
| `➖` | N/A: relevant element does not exist |
| `🔵 판정불가` | Runtime verification not possible — must state specific reason |

---

## Step 5. Generate Reports

Save results in 2 formats.


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

- Result colors: `✅` (#28a745), `❌` (#dc3545), `⚠️` (#ffc107), `➖` (#6c757d), `🔵 판정불가` (#6c8ebf)
- Structure: summary table → detailed results by principle → semantic HTML → fix guide
- Language: Korean / Style: inline CSS only
- Verdict method column: `정적분석` / `브라우저 검증` / `판정불가`

### CSV Report

- Header: `번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드`
- All 33 KWCAG items + all semantic HTML items
- Wrap cells with commas/newlines in double-quotes; escape `"` as `""`

---

## Step 6. Verify Completeness

1. All 33 KWCAG2.2 items evaluated — none skipped
2. Semantic HTML section (7+ items) evaluated
3. Every `❌` includes: item number, filename:line, concrete violation
4. Every `⚠️` includes specific improvement recommendation
5. `🔵 판정불가` items state specific reason
6. Both report.html and report.csv written (standalone mode only)
7. If anything is missing, resolve before claiming completion

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:
- Result colors: `✅` (#28a745), `❌` (#dc3545), `⚠️` (#ffc107), `➖` (#6c757d), `🔵 판정불가` (#6c8ebf)
- Structure: summary → detailed by principle → semantic HTML → fix guide
- Language: Korean / Style: inline CSS only
- Verdict method: `정적분석` / `브라우저 검증` / `판정불가`
- CSV header: `번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드`

</Output_Format>
</Skill_Guide>
