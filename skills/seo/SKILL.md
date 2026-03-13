---
name: seo
description: SEO + Web Performance review. Orchestrates seo-static (code analysis) and seo-lighthouse (Lighthouse CLI verification), then merges results into a unified HTML + CSV report. Covers Technical SEO (11 items), Web Performance (18 items), and Core Web Vitals metrics. Use when asked to review SEO, 검색엔진 최적화, SEO 검토, 성능 검토, Core Web Vitals, 웹 성능, or any SEO/performance audit.
model: sonnet
---

<Skill_Guide>
<Purpose>
Orchestrates a complete SEO + Web Performance review by coordinating two sub-skills:
- **seo-static**: Evaluates all 29 items (SEO-01~11, WP-01~18) via static code analysis
- **seo-lighthouse**: Verifies 17 items with Lighthouse CLI real measurements + Core Web Vitals metrics

Merges results from both, resolves conflicts (Lighthouse wins), and generates HTML + CSV reports in Korean.
</Purpose>

<Instructions>

## Step 1. Review Scope

Determine the files to review:

```bash
git diff --name-only HEAD
```

Filter to web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`

- Changed web files exist -> set as review targets
- No changed web files -> ask user to specify
- User specifies explicitly -> use that

---

## Step 2. Run Sub-Skills

Read and follow each sub-skill's SKILL.md. Both sub-skills accept the same file list
and return JSON arrays of item results.

### 2-1. Static Analysis

Read `../seo-static/SKILL.md` and follow its instructions with the target files.
This always runs — it has no external dependencies.

### 2-2. Lighthouse Verification

Read `../seo-lighthouse/SKILL.md` and follow its instructions with the target files.
This handles dev server startup and Lighthouse execution automatically.

If Lighthouse verification fails entirely (no dev server, no Lighthouse CLI, no Chrome),
the orchestrator proceeds with static analysis results only.

---

## Step 3. Merge Results

Both sub-skills return results keyed by item code (SEO-01 through SEO-11, WP-01 through WP-18).

### Merge Rules

1. **Lighthouse-verified items** (verdict_method = `Lighthouse`): Lighthouse result takes precedence
   over static analysis, regardless of whether they agree.

2. **Static-only items**: use as-is with verdict_method = `정적분석`.

3. **Conflict resolution**: if Lighthouse says `✅` but static says `❌` -> use `✅` (Lighthouse).
   The real measurement is the source of truth over code patterns.

4. **판정불가 items**: if Lighthouse returned `🔵 판정불가` for an item, fall back to the
   static analysis result for that item (verdict_method stays `정적분석`).

5. **Metrics**: if Lighthouse returned a `metrics` object (LCP, CLS, TBT, scores),
   include it in the report header.

### Items Coverage

| Source | Items |
| --- | --- |
| Static analysis only | All 29 items (SEO-01~11, WP-01~18) |
| Lighthouse can override | SEO-01, 02, 04, 05, 06, 09, 10, 11 / WP-01, 02, 03, 04, 05, 06, 10, 12, 17 (17 items) |
| Static analysis exclusive | SEO-03, 07, 08 / WP-07, 08, 09, 11, 13, 14, 15, 16, 18 (12 items) |

---

## Step 4. Classify Results

| Result | Meaning |
| --- | --- |
| `✅` | Pass: no violation found |
| `❌` | Fail: violation found (include filename:line) |
| `⚠️` | Advisory: improvement recommended |
| `➖` | N/A: relevant element does not exist |
| `🔵 판정불가` | Verification not possible — must state specific reason |

---

## Step 5. Generate Reports

Save results in 2 formats.

### Output Files

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_DIR="reports/seo/${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"
```

- `${REPORT_DIR}/report.html`
- `${REPORT_DIR}/report.csv`

### Report Templates

Read `references/output-format.md` for the full HTML + CSV report templates.

Key requirements:
- Result colors: `✅` (#28a745), `❌` (#dc3545), `⚠️` (#ffc107), `➖` (#6c757d), `🔵 판정불가` (#6c8ebf)
- Language: Korean / Style: inline CSS only
- Verdict method: `정적분석` / `Lighthouse` / `판정불가`
- CSV header: `코드,우선순위,항목명,결과,판정방식,발견된 문제,수정 가이드`

---

## Step 6. Verify Completeness

1. All 29 items evaluated — none skipped
2. Every `❌` includes: item code, filename:line, concrete violation
3. Every `⚠️` includes specific improvement recommendation
4. `🔵 판정불가` items state specific reason
5. Both report.html and report.csv written
6. If anything is missing, resolve before claiming completion

</Instructions>
</Skill_Guide>
