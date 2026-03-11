# Output Format Reference

Unified HTML + CSV report templates for web quality audit results (2 areas).

---

## HTML Report Template

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
    .summary-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 32px; }
    .summary-card { border-radius: 6px; padding: 14px; text-align: center; color: #fff; }
    .summary-card .area { font-size: 0.75rem; font-weight: 600; margin-bottom: 6px; }
    .summary-card .score { font-size: 1.5rem; font-weight: 700; }
    .card-a11y { background: #6c8ebf; }
    .card-seo { background: #f0a830; }

    /* 섹션 */
    .section { margin-bottom: 36px; }
    .section-header { padding: 12px 16px; border-radius: 6px 6px 0 0; color: #fff; font-weight: 700; font-size: 1rem; }
    .header-a11y { background: #6c8ebf; }
    .header-seo { background: #f0a830; }

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
    기준: KWCAG2.2 + 시맨틱 HTML + SEO + Web Performance &nbsp;|&nbsp;
    Playwright: {사용됨 / 미사용 — playwright.config.ts 없음}
  </div>

  <!-- 종합 요약 -->
  <div class="summary-grid">
    <div class="summary-card card-a11y">
      <div class="area">접근성</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
    <div class="summary-card card-seo">
      <div class="area">SEO & Web Performance</div>
      <div class="score">{통과수}/{전체수}</div>
    </div>
  </div>

  <!-- 섹션 A: 접근성 -->
  <div class="section">
    <div class="section-header header-a11y">A. 접근성 (KWCAG2.2 33항목 + 시맨틱 HTML 7항목)</div>
    <table>
      <tr><th>번호</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th></tr>
      <!-- accessibility 스킬 위임 결과 33+7행 삽입 -->
    </table>
  </div>

  <!-- 섹션 B: SEO & Web Performance -->
  <div class="section">
    <div class="section-header header-seo">B. SEO & Web Performance (Technical SEO 11항목 + Page Experience 18항목)</div>
    <table>
      <tr><th>코드</th><th>영역</th><th>항목명</th><th>결과</th><th>발견된 문제</th></tr>
      <!-- SEO-01 ~ SEO-11, WP-01 ~ WP-18 rows -->
    </table>
  </div>

  <!-- 수정 가이드 (❌ 항목만) -->
  <div class="fix-guide">
    <h2 style="margin-bottom:16px;">수정 가이드</h2>
    <div class="fix-item">
      <div class="fix-title">{코드}: {항목명}</div>
      <p>{구체적인 수정 가이드} <code>{코드 예시}</code></p>
    </div>
    <!-- ❌ 항목마다 fix-item 블록 추가 -->
  </div>

</div>
</body>
</html>
```

---

## CSV Report Template

```csv
영역,코드,항목명,결과,판정방식,발견된 문제,수정 가이드
접근성,A-01,대체 텍스트,✅,정적분석,,
접근성,A-08,명도 대비,❌,Playwright,"#nav .link 대비 3.2:1 (기준 4.5:1)","색상을 #595959로 변경"
접근성,A-10,키보드 접근성,✅,Playwright,,
접근성,A-33,동적 ARIA,✅,Playwright,,
SEO,SEO-01,noindex 없음,✅,정적분석,,
SEO,SEO-05,meta description,❌,정적분석,meta description 없음,"<meta name=""description"" content=""...""> 추가"
SEO,SEO-09,DOCTYPE html 선언,✅,정적분석,,
Web Performance,WP-01,render-blocking script,❌,정적분석,defer 없는 script 태그,script 태그에 defer 추가
Web Performance,WP-02,fetchpriority="high",❌,정적분석,LCP 이미지에 속성 없음,히어로 이미지에 fetchpriority="high" 추가
```
