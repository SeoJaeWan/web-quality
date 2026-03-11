---
name: quality
description: Comprehensive web quality review across 2 areas: accessibility (KWCAG2.2 + semantic HTML, 40 items) and SEO & web performance (Technical SEO + Page Experience, 29 items). Generates unified HTML + CSV reports. Use when asked to "web quality audit", "종합 품질 검토", "웹 품질 감사", "전체 품질 리뷰", "접근성 검토", "a11y 체크", "웹표준 확인", "SEO 검토", "성능 검토".
model: sonnet
context: fork
agent: web-quality
---

<Skill_Guide>
<Purpose>
After completing work, performs a comprehensive review of changed web code
across two quality areas — Accessibility (KWCAG2.2 + Semantic HTML) and
SEO & Web Performance (Technical SEO + Page Experience / Core Web Vitals) —
and generates a single unified HTML + CSV report. The accessibility area is
fully delegated to the accessibility skill; the SEO & performance area
delegates to the seo skill.
</Purpose>

<Instructions>

## 내부 실행 순서

1. accessibility 스킬 실행
2. seo 스킬 실행

진입점: 항상 web-quality 에이전트를 통해 실행

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

## Step 2. Accessibility Review — Delegate to accessibility skill

Delegate KWCAG2.2 33-item accessibility review to the `accessibility` skill.

Reference: `<plugin-root>/skills/accessibility/SKILL.md`

Delegation instructions:
- Step 1 (scope) is already determined — pass the same file set
- Steps 2–5: KWCAG2.2 33-item code review + Playwright automated checks (if `playwright.config.ts` exists)
- Step 6 (individual report generation) is skipped — collect only result data (✅/❌/⚠️/➖/🔵 per item)

Collected results → **Section A: Accessibility**

---

## Step 3. SEO & Web Performance Review — Delegate to seo skill

Execute the 'seo' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each SEO-code and WP-code item.
Collected results → **Section B: SEO & Web Performance**

---

## Step 4. Generate Unified Report

Collect results from both sections (A–B) and generate a single HTML + CSV file.

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

## Step 5. Verify Results

1. Confirm both sections (A–B) have been collected — none may be skipped.
2. Confirm both `reports/web-quality/YYYYMMDD-HHmm/report.html` and `reports/web-quality/YYYYMMDD-HHmm/report.csv` have been written.
3. Verify the HTML report contains both section headers (A–B).
4. Verify the CSV contains rows for both areas.
5. If any section was skipped or failed, report the reason and do not claim completion.

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:
- 2-area summary grid (접근성 / SEO & Web Performance) with color-coded cards
- Badge classes: `badge-pass` (✅), `badge-fail` (❌), `badge-partial` (⚠️), `badge-na` (➖), `badge-unknown` (🔵)
- Section headers color-coded: a11y=#6c8ebf, seo=#f0a830
- Fix guide section: only ❌ items, with code examples
- CSV header: `영역,코드,항목명,결과,판정방식,발견된 문제,수정 가이드`
- Language: Korean / Style: inline CSS only

</Output_Format>
</Skill_Guide>
