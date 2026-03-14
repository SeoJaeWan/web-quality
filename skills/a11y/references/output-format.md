# Output Format Reference

Issue-focused HTML + CSV report templates. Only violations (❌), advisories (⚠️),
and inconclusive (🔵) items are shown — passing items are omitted.

---

## HTML Report Template

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>웹 접근성 검토 리포트 — {YYYY-MM-DD}</title>
<style>
  body { font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; max-width: 1000px; margin: 0 auto; padding: 24px; color: #333; line-height: 1.6; }
  h1 { border-bottom: 3px solid #333; padding-bottom: 8px; }
  h2 { border-left: 5px solid #555; padding-left: 12px; margin-top: 32px; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9em; }
  th { background: #f5f5f5; padding: 10px 12px; border: 1px solid #ddd; text-align: left; white-space: nowrap; }
  td { padding: 10px 12px; border: 1px solid #ddd; vertical-align: top; }
  tr:hover td { background: #fafafa; }
  .result-fail    { background: #f8d7da; color: #721c24; font-weight: bold; text-align: center; }
  .result-partial { background: #fff3cd; color: #856404; font-weight: bold; text-align: center; }
  .result-unknown { background: #dce8f8; color: #1a4a8a; text-align: center; font-size: 0.85em; }
  .method-browser { color: #0066cc; font-size: 0.8em; font-weight: bold; }
  .method-static  { color: #666; font-size: 0.8em; }
  .method-unknown { color: #999; font-size: 0.8em; }
  .summary-box { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-bottom: 24px; }
  .summary-stat { display: inline-block; margin-right: 32px; }
  .summary-stat .num { font-size: 2em; font-weight: bold; }
  .summary-stat .label { font-size: 0.85em; color: #666; }
  .stat-fail .num { color: #dc3545; }
  .stat-warn .num { color: #856404; }
  .stat-clean .num { color: #28a745; }
  .fix-fail    { background: #fff5f5; border-left: 4px solid #dc3545; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  .fix-partial { background: #fffdf0; border-left: 4px solid #ffc107; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
  .clean-message { text-align: center; padding: 40px; color: #28a745; font-size: 1.2em; }
</style>
</head>
<body>

<h1>웹 접근성 검토 리포트</h1>

<div class="summary-box">
  <div><strong>날짜:</strong> {YYYY-MM-DD} | <strong>검토 파일:</strong> {파일 목록} | <strong>기준:</strong> KWCAG2.2</div>
  <div style="margin-top: 12px;">
    <span class="summary-stat stat-fail"><span class="num">{N}</span><span class="label"> 위반</span></span>
    <span class="summary-stat stat-warn"><span class="num">{N}</span><span class="label"> 권고</span></span>
    <!-- 위반 0건일 때 -->
    <!-- <span class="summary-stat stat-clean"><span class="num">0</span><span class="label"> 위반</span></span> -->
  </div>
</div>

<!-- 위반 항목이 있을 때만 표시 -->
<h2>위반 항목 (❌)</h2>
<table>
  <tr><th>#</th><th>항목명</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <tr>
    <td>1</td><td>적절한 대체 텍스트</td>
    <td><span class="method-static">정적분석</span></td>
    <td>page.tsx:83 — &lt;img&gt; alt 속성 누락</td>
    <td>&lt;img alt="프로모션 배너"&gt; 추가</td>
  </tr>
</table>

<!-- 권고 항목이 있을 때만 표시 -->
<h2>권고 항목 (⚠️)</h2>
<table>
  <tr><th>#</th><th>항목명</th><th>판정방식</th><th>내용</th><th>권장 수정</th></tr>
  <tr>
    <td>S-03</td><td>랜드마크 요소</td>
    <td><span class="method-static">정적분석</span></td>
    <td>페이지 최상위 &lt;div&gt;에 &lt;main&gt; 랜드마크 없음</td>
    <td>&lt;div&gt; → &lt;main&gt;으로 변경</td>
  </tr>
</table>

<!-- 판정불가 항목이 있을 때만 표시 -->
<!--
<h2>판정불가 (🔵)</h2>
<table>
  <tr><th>#</th><th>항목명</th><th>사유</th></tr>
  <tr><td>A-08</td><td>명도 대비</td><td>agent-browser 사용 불가</td></tr>
</table>
-->

<!-- 위반 0건일 때 -->
<!--
<div class="clean-message">
  ✅ 검토 결과 위반 항목 없음
</div>
-->

<h2>수정 가이드 상세</h2>

<div class="fix-fail">
  <p><strong>항목 {N}. {항목명}</strong> — <code>{파일명}:{라인}</code></p>
  <p><strong>문제:</strong> {구체적인 코드 문제}</p>
  <p><strong>수정:</strong> <code>{구체적인 수정 코드}</code></p>
</div>

<div class="fix-partial">
  <p><strong>항목 {N}. {항목명}</strong></p>
  <p><strong>내용:</strong> {개선 권고 내용}</p>
</div>

</body>
</html>
```

---

## CSV Report Template

Only rows with issues — no ✅ or ➖ rows.

```
번호,항목명,결과,판정방식,발견된 문제,수정 가이드
1,적절한 대체 텍스트,❌,정적분석,"page.tsx:83 — <img> alt 누락","<img alt=""프로모션 배너""> 추가"
10,키보드 사용,❌,브라우저 검증,"Tab 포커스 이동 시 div 요소 미접근","<button>으로 변경 또는 tabIndex={0} 추가"
S-03,랜드마크 요소,⚠️,정적분석,"<main> 랜드마크 없음","<div> → <main>으로 변경"
```

If no issues found, CSV has only the header row.
