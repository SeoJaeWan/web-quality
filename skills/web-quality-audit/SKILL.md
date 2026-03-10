---
name: web-quality-audit
description: Comprehensive web quality review across 4 areas: accessibility (KWCAG2.2), best-practices, SEO, and web-performance (Performance + Core Web Vitals). Generates unified HTML + CSV reports. Use when asked to "web quality audit", "종합 품질 검토", "웹 품질 감사", "전체 품질 리뷰", "접근성 검토", "a11y 체크", "웹표준 확인".
model: sonnet
context: fork
agent: web-quality-reviewer
---

<Skill_Guide>
<Purpose>
After completing work, performs a comprehensive review of changed web code
across four quality areas — Accessibility (KWCAG2.2), Best Practices, SEO,
and Web Performance (Performance + Core Web Vitals) — and generates a single
unified HTML + CSV report. The accessibility area is fully delegated to the
accessibility-review skill; the remaining three areas delegate to their
respective individual skills.
</Purpose>

<Instructions>

## 내부 실행 순서

1. accessibility-review 스킬 실행
2. best-practices 스킬 실행
3. seo 스킬 실행
4. web-performance 스킬 실행

진입점: 항상 web-quality-reviewer 에이전트를 통해 실행

---

## Step 1. Determine Review Scope

```bash
git diff --name-only HEAD
```

- Filter files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- Changed files exist → use as review targets
- No changed files → AskUserQuestion: "검토할 파일이나 작업 내용을 알려주세요."
- User specifies scope explicitly → use that instead

**결정된 파일 목록을 서브 스킬에 전달합니다. 서브 스킬은 scope를 재결정하지 않습니다.**

---

## Step 2. Accessibility Review — Delegate to accessibility-review skill

Delegate KWCAG2.2 33-item accessibility review to the `accessibility-review` skill.

Reference: `<plugin-root>/skills/accessibility-review/SKILL.md`

Delegation instructions:
- Step 1 (scope) is already determined — pass the same file set
- Steps 2–5: KWCAG2.2 33-item code review + Playwright automated checks (if `playwright.config.ts` exists)
- Step 6 (individual report generation) is skipped — collect only result data (✅/❌/⚠️/➖/🔵 per item)

Collected results → **Section A: Accessibility**

---

## Step 3. Best Practices Review — Delegate to best-practices skill

Execute the 'best-practices' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each BP-code item.
Collected results → Section B: Best Practices

---

## Step 4. SEO Review — Delegate to seo skill

Execute the 'seo' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each SEO-code item.
Collected results → Section C: SEO

---

## Step 5. Web Performance Review — Delegate to web-performance skill

Execute the 'web-performance' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each WP-code item.
Collected results → Section D: Web Performance

---

## Step 6. Generate Unified Report

Collect results from all 4 sections (A–D) and generate a single HTML + CSV file.

```bash
# 타임스탬프 계산
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_DIR="reports/web-quality/${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"

# Save path
${REPORT_DIR}/report.html
${REPORT_DIR}/report.csv
```

동일 분 내 재실행 시 폴더 재사용 허용 (suffix 불필요).

---

## Step 7. Verify Results

1. Confirm all four sections (A–D) have been collected — none may be skipped.
2. Confirm both `reports/web-quality/YYYYMMDD-HHmm/report.html` and `reports/web-quality/YYYYMMDD-HHmm/report.csv` have been written.
3. Verify the HTML report contains all four section headers (A–D).
4. Verify the CSV contains rows for all four areas.
5. If any section was skipped or failed, report the reason and do not claim completion.

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:
- 4-area summary grid (접근성/BP/SEO/Web Performance) with color-coded cards
- Badge classes: `badge-pass` (✅), `badge-fail` (❌), `badge-partial` (⚠️), `badge-na` (➖), `badge-unknown` (🔵)
- Section headers color-coded: a11y=#6c8ebf, bp=#82c882, seo=#f0a830, perf=#e05c5c
- Fix guide section: only ❌ items, with code examples
- CSV header: `영역,코드,항목명,결과,판정방식,발견된 문제,수정 가이드`
- Language: Korean / Style: inline CSS only

</Output_Format>
</Skill_Guide>
