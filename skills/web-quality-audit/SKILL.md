---
name: web-quality-audit
description: Comprehensive web quality review across 5 areas: accessibility (KWCAG2.2), best-practices, SEO, performance, and Core Web Vitals. Generates unified HTML + CSV reports. Use when asked to "web quality audit", "종합 품질 검토", "웹 품질 감사", "전체 품질 리뷰", "접근성 검토", "a11y 체크", "웹표준 확인".
---

<Skill_Guide>
<Purpose>
After completing work, performs a comprehensive review of changed web code
across five quality areas — Accessibility (KWCAG2.2), Best Practices, SEO,
Performance, and Core Web Vitals — and generates a single unified HTML + CSV
report. The accessibility area is fully delegated to the accessibility-review
skill; the remaining four areas delegate to their respective individual skills.
</Purpose>

<Instructions>

## Step 1. Determine Review Scope

```bash
git diff --name-only HEAD
```

- Filter files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- Changed files exist → use as review targets
- No changed files → AskUserQuestion: "검토할 파일이나 작업 내용을 알려주세요."
- User specifies scope explicitly → use that instead

---

## Step 2. Accessibility Review — Delegate to accessibility-review skill

Delegate KWCAG2.2 33-item accessibility review to the `accessibility-review` skill.

Reference: `.claude/skills/accessibility-review/SKILL.md`

Delegation instructions:
- Step 1 (scope) is already determined — pass the same file set
- Steps 2–5: KWCAG2.2 33-item code review + Playwright automated checks (if `playwright.config.ts` exists)
- Step 6 (individual report generation) is skipped — collect only result data (O/X/△/-/판정불가 per item)

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

## Step 5. Performance Review — Delegate to performance skill

Execute the 'performance' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each PERF-code item.
Collected results → Section D: Performance

---

## Step 6. Core Web Vitals Review — Delegate to core-web-vitals skill

Execute the 'core-web-vitals' skill Step 3 (Static Analysis) against the same file set determined in Step 1.
Collect the result row for each CWV-code item.
Collected results → Section E: Core Web Vitals

---

## Step 7. Generate Unified Report

Collect results from all 5 sections (A–E) and generate a single HTML + CSV file.

```bash
# Save path
.claude/reports/web-quality-YYYYMMDD.html
.claude/reports/web-quality-YYYYMMDD.csv
```

If a file with the same date already exists, append `-2`, `-3` suffix.

---

## Step 8. Verify Results

1. Confirm all five sections (A–E) have been collected — none may be skipped.
2. Confirm both `.claude/reports/web-quality-YYYYMMDD.html` and `.csv` have been written.
3. Verify the HTML report contains all five section headers (A–E).
4. Verify the CSV contains rows for all five areas.
5. If any section was skipped or failed, report the reason and do not claim completion.

</Instructions>

<Output_Format>

## HTML 리포트 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>웹 품질 종합 감사 리포트 — {YYYY-MM-DD}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; padding: 24px; }
    .container { max-width: 1100px; margin: 0 auto; background: #fff; border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
    h1 { font-size: 1.6rem; margin-bottom: 8px; }
    .meta { color: #666; font-size: 0.9rem; margin-bottom: 28px; }
    .playwright-badge { background: #4a90d9; color: #fff; font-size: 0.75rem; padding: 2px 6px; border-radius: 3px; }

    /* 종합 요약 */
    .summary-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 32px; }
    .summary-card { border-radius: 6px; padding: 14px; text-align: center; color: #fff; }
    .summary-card .area { font-size: 0.75rem; font-weight: 600; margin-bottom: 6px; }
    .summary-card .score { font-size: 1.5rem; font-weight: 700; }
    .card-a11y { background: #6c8ebf; }
    .card-bp { background: #82c882; }
    .card-seo { background: #f0a830; }
    .card-perf { background: #e05c5c; }
    .card-cwv { background: #9b59b6; }

    /* 섹션 */
    .section { margin-bottom: 36px; }
    .section-header { padding: 12px 16px; border-radius: 6px 6px 0 0; color: #fff; font-weight: 700; font-size: 1rem; }
    .header-a11y { background: #6c8ebf; }
    .header-bp { background: #82c882; }
    .header-seo { background: #f0a830; }
    .header-perf { background: #e05c5c; }
    .header-cwv { background: #9b59b6; }

    table { width: 100%; border-collapse: collapse; }
    th { background: #f9f9f9; font-size: 0.8rem; padding: 8px 10px; text-align: left; border-bottom: 2px solid #ddd; }
    td { padding: 8px 10px; border-bottom: 1px solid #eee; font-size: 0.85rem; vertical-align: top; }
    tr:last-child td { border-bottom: none; }

    /* 판정 배지 */
    .badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-weight: 700; font-size: 0.8rem; }
    .badge-pass { background: #e6f4ea; color: #1e7e34; }
    .badge-fail { background: #fdecea; color: #c62828; }
    .badge-partial { background: #fff8e1; color: #f57c00; }
    .badge-na { background: #f5f5f5; color: #777; }
    .badge-unknown { background: #e8f0fe; color: #1a56db; }

    /* 수정 가이드 */
    .fix-guide { margin-top: 32px; }
    .fix-item { background: #fff8e1; border-left: 4px solid #f0a830; padding: 12px 16px; margin-bottom: 12px; border-radius: 0 4px 4px 0; }
    .fix-item .fix-title { font-weight: 600; margin-bottom: 6px; }
    .fix-item code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; font-size: 0.82rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>웹 품질 종합 감사 리포트</h1>
  <div class="meta">
    날짜: {YYYY-MM-DD} &nbsp;|&nbsp;
    검토 파일: {파일 목록} &nbsp;|&nbsp;
    기준: KWCAG2.2 + Best Practices + SEO + Performance + Core Web Vitals &nbsp;|&nbsp;
    Playwright: {사용됨 / 미사용 — playwright.config.ts 없음}
  </div>

  <!-- 종합 요약 -->
  <div class="summary-grid">
    <div class="summary-card card-a11y">
      <div class="area">접근성</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
    <div class="summary-card card-bp">
      <div class="area">Best Practices</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
    <div class="summary-card card-seo">
      <div class="area">SEO</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
    <div class="summary-card card-perf">
      <div class="area">Performance</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
    <div class="summary-card card-cwv">
      <div class="area">Core Web Vitals</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
  </div>

  <!-- 섹션 A: 접근성 -->
  <div class="section">
    <div class="section-header header-a11y">A. 접근성 (KWCAG2.2 33항목)</div>
    <table>
      <tr><th>번호</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th></tr>
      <!-- accessibility-review 스킬 위임 결과 33행 삽입 -->
      <!-- 예시: -->
      <tr><td>1</td><td>대체 텍스트</td><td><span class="badge badge-pass">O</span></td><td>정적분석</td><td></td></tr>
    </table>
  </div>

  <!-- 섹션 B: Best Practices -->
  <div class="section">
    <div class="section-header header-bp">B. Best Practices</div>
    <table>
      <tr><th>코드</th><th>영역</th><th>항목명</th><th>결과</th><th>발견된 문제</th></tr>
      <tr><td>BP-01</td><td>보안</td><td>HTTPS / mixed content 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-02</td><td>보안</td><td>취약 의존성 없음</td><td><span class="badge badge-na">-</span></td><td>npm audit 실행 환경 필요</td></tr>
      <tr><td>BP-03</td><td>보안</td><td>CSP 헤더</td><td><span class="badge badge-fail">X</span></td><td>Content-Security-Policy 미설정</td></tr>
      <tr><td>BP-04</td><td>보안</td><td>보안 헤더</td><td><span class="badge badge-fail">X</span></td><td>X-Frame-Options 미설정</td></tr>
      <tr><td>BP-05</td><td>보안</td><td>innerHTML 미검증 입력</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-06</td><td>호환성</td><td>DOCTYPE html</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-07</td><td>호환성</td><td>charset UTF-8 최상단</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-08</td><td>호환성</td><td>viewport meta</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-09</td><td>호환성</td><td>deprecated API 미사용</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-10</td><td>호환성</td><td>passive listener</td><td><span class="badge badge-partial">△</span></td><td>scroll 핸들러에 passive 옵션 없음</td></tr>
      <tr><td>BP-11</td><td>코드품질</td><td>콘솔 에러 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-12</td><td>코드품질</td><td>중복 id 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-13</td><td>코드품질</td><td>시맨틱 HTML 요소</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>BP-14</td><td>코드품질</td><td>적절한 에러 처리</td><td><span class="badge badge-partial">△</span></td><td>일부 async 함수에 try/catch 없음</td></tr>
    </table>
  </div>

  <!-- 섹션 C: SEO -->
  <div class="section">
    <div class="section-header header-seo">C. SEO</div>
    <table>
      <tr><th>코드</th><th>우선순위</th><th>항목명</th><th>결과</th><th>발견된 문제</th></tr>
      <tr><td>SEO-01</td><td>Critical</td><td>HTTPS 사용</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-02</td><td>Critical</td><td>noindex 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-03</td><td>Critical</td><td>title 태그 존재하고 고유</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-04</td><td>Critical</td><td>h1 하나</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-05</td><td>High</td><td>meta description</td><td><span class="badge badge-fail">X</span></td><td>meta description 없음</td></tr>
      <tr><td>SEO-06</td><td>High</td><td>canonical URL</td><td><span class="badge badge-fail">X</span></td><td>canonical 링크 없음</td></tr>
      <tr><td>SEO-07</td><td>High</td><td>구조화 데이터 (JSON-LD)</td><td><span class="badge badge-fail">X</span></td><td>JSON-LD 스크립트 없음</td></tr>
      <tr><td>SEO-08</td><td>High</td><td>이미지 alt 텍스트</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-09</td><td>Medium</td><td>서술적 URL 구조</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>SEO-10</td><td>Medium</td><td>내부 링크 anchor text</td><td><span class="badge badge-partial">△</span></td><td>"여기를 클릭" 패턴 2건</td></tr>
    </table>
  </div>

  <!-- 섹션 D: Performance -->
  <div class="section">
    <div class="section-header header-perf">D. Performance</div>
    <table>
      <tr><th>코드</th><th>영역</th><th>항목명</th><th>결과</th><th>발견된 문제</th></tr>
      <tr><td>PERF-01</td><td>CRP</td><td>render-blocking script 없음</td><td><span class="badge badge-fail">X</span></td><td>defer/async 없는 script 태그</td></tr>
      <tr><td>PERF-02</td><td>CRP</td><td>LCP 이미지 fetchpriority + preload</td><td><span class="badge badge-fail">X</span></td><td>히어로 이미지에 fetchpriority 없음</td></tr>
      <tr><td>PERF-03</td><td>CRP</td><td>Critical CSS 처리</td><td><span class="badge badge-partial">△</span></td><td>전체 CSS 블로킹 로드</td></tr>
      <tr><td>PERF-04</td><td>이미지</td><td>width/height 지정</td><td><span class="badge badge-fail">X</span></td><td>3개 이미지에 크기 속성 없음</td></tr>
      <tr><td>PERF-05</td><td>이미지</td><td>loading="lazy"</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>PERF-06</td><td>이미지</td><td>WebP/AVIF 포맷</td><td><span class="badge badge-partial">△</span></td><td>일부 PNG 이미지 WebP 미변환</td></tr>
      <tr><td>PERF-07</td><td>JS</td><td>코드 스플리팅</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>PERF-08</td><td>JS</td><td>트리 쉐이킹 패턴</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>PERF-09</td><td>JS</td><td>레이아웃 스래싱 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
    </table>
  </div>

  <!-- 섹션 E: Core Web Vitals -->
  <div class="section">
    <div class="section-header header-cwv">E. Core Web Vitals</div>
    <table>
      <tr><th>코드</th><th>지표</th><th>항목명</th><th>결과</th><th>발견된 문제</th></tr>
      <tr><td>CWV-01</td><td>LCP</td><td>LCP 요소 초기 HTML 존재</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>CWV-02</td><td>LCP</td><td>fetchpriority="high"</td><td><span class="badge badge-fail">X</span></td><td>LCP 이미지에 속성 없음</td></tr>
      <tr><td>CWV-03</td><td>LCP</td><td>폰트 렌더 차단 없음</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>CWV-04</td><td>INP</td><td>이벤트 핸들러 즉각 피드백</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>CWV-05</td><td>INP</td><td>무거운 연산 지연 처리</td><td><span class="badge badge-partial">△</span></td><td>일부 동기 루프 최적화 필요</td></tr>
      <tr><td>CWV-06</td><td>CLS</td><td>img width/height 또는 aspect-ratio</td><td><span class="badge badge-fail">X</span></td><td>3개 이미지 크기 미지정</td></tr>
      <tr><td>CWV-07</td><td>CLS</td><td>뷰포트 위 동적 삽입 금지</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>CWV-08</td><td>CLS</td><td>애니메이션 transform/opacity만</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
      <tr><td>CWV-09</td><td>CLS</td><td>폰트 교체 레이아웃 시프트 방지</td><td><span class="badge badge-pass">O</span></td><td></td></tr>
    </table>
  </div>

  <!-- 수정 가이드 (X 항목만) -->
  <div class="fix-guide">
    <h2 style="margin-bottom:16px;">수정 가이드</h2>
    <div class="fix-item">
      <div class="fix-title">PERF-01 · CWV-02: render-blocking script / fetchpriority 미설정</div>
      <p>모든 비필수 스크립트에 <code>defer</code> 또는 <code>async</code>를 추가하고, LCP 이미지에 <code>fetchpriority="high"</code>를 설정하세요.</p>
    </div>
    <!-- X 항목마다 fix-item 블록 추가 -->
  </div>

</div>
</body>
</html>
```

## CSV 리포트 템플릿

```csv
영역,코드,항목명,결과,판정방식,발견된 문제,수정 가이드
접근성,A-01,대체 텍스트,O,정적분석,,
접근성,A-08,명도 대비,X,Playwright,"#nav .link 대비 3.2:1 (기준 4.5:1)","색상을 #595959로 변경"
접근성,A-10,키보드 접근성,O,Playwright,,
접근성,A-33,동적 ARIA,O,Playwright,,
Best Practices,BP-01,HTTPS / mixed content 없음,O,정적분석,,
Best Practices,BP-03,CSP 헤더,X,정적분석,Content-Security-Policy 미설정,meta 또는 헤더에 CSP 추가
SEO,SEO-05,meta description,X,정적분석,meta description 없음,"<meta name=""description"" content=""...""> 추가"
Performance,PERF-01,render-blocking script,X,정적분석,defer 없는 script 태그,script 태그에 defer 추가
Core Web Vitals,CWV-02,fetchpriority="high",X,정적분석,LCP 이미지에 속성 없음,히어로 이미지에 fetchpriority="high" 추가
```

</Output_Format>
</Skill_Guide>
