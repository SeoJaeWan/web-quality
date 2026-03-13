# Output Format Reference

HTML + CSV report templates for SEO & Web Performance review results.

---

## HTML Report Template

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>SEO & Web Performance 검토 리포트 — {YYYY-MM-DD}</title>
<style>
  body { font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; max-width: 1200px; margin: 0 auto; padding: 24px; color: #333; line-height: 1.6; }
  h1 { border-bottom: 3px solid #333; padding-bottom: 8px; }
  h2 { border-left: 5px solid #555; padding-left: 12px; margin-top: 32px; }
  h3 { color: #444; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9em; }
  th { background: #f5f5f5; padding: 10px 12px; border: 1px solid #ddd; text-align: left; white-space: nowrap; }
  td { padding: 10px 12px; border: 1px solid #ddd; vertical-align: top; }
  tr:hover td { background: #fafafa; }
  .result-pass    { background: #d4edda; color: #155724; font-weight: bold; text-align: center; }
  .result-fail    { background: #f8d7da; color: #721c24; font-weight: bold; text-align: center; }
  .result-partial { background: #fff3cd; color: #856404; font-weight: bold; text-align: center; }
  .result-na      { background: #e2e3e5; color: #383d41; text-align: center; }
  .result-unknown { background: #dce8f8; color: #1a4a8a; text-align: center; font-size: 0.85em; }
  .method-lighthouse { color: #0066cc; font-size: 0.8em; font-weight: bold; }
  .method-static     { color: #666; font-size: 0.8em; }
  .method-unknown    { color: #999; font-size: 0.8em; }
  .summary-pass { color: #155724; font-weight: bold; }
  .summary-fail { color: #721c24; font-weight: bold; }
  .fix-fail    { background: #fff5f5; border-left: 4px solid #dc3545; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  .fix-partial { background: #fffdf0; border-left: 4px solid #ffc107; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
  .meta { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 16px; margin-bottom: 24px; }
  .meta ul { list-style: none; margin: 0; padding: 0; }
  .meta li { margin: 4px 0; }
  .lighthouse-badge { display: inline-block; background: #0066cc; color: white; font-size: 0.75em; padding: 2px 8px; border-radius: 10px; margin-left: 8px; }
  .metrics-card { background: #f0f7ff; border: 1px solid #b3d4fc; border-radius: 8px; padding: 20px; margin: 16px 0; }
  .metrics-card h3 { margin-top: 0; color: #0066cc; }
  .metric-good { color: #155724; font-weight: bold; }
  .metric-poor { color: #721c24; font-weight: bold; }
</style>
</head>
<body>

<h1>SEO & Web Performance 검토 리포트</h1>

<div class="meta">
<ul>
  <li><strong>날짜:</strong> {YYYY-MM-DD}</li>
  <li><strong>검토 파일:</strong> {변경된 파일 목록}</li>
  <li><strong>기준:</strong> Technical SEO (11항목) + Page Experience / Web Performance (18항목)</li>
  <li><strong>Lighthouse:</strong> {사용됨 <span class="lighthouse-badge">실측검증</span> / 미사용 — Lighthouse CLI 없음}</li>
</ul>
</div>

<!-- Lighthouse 메트릭 요약 (Lighthouse 실행 성공 시에만 포함) -->
<div class="metrics-card">
  <h3>Core Web Vitals 실측 메트릭</h3>
  <table>
    <tr><th>메트릭</th><th>측정값</th><th>기준값</th><th>상태</th></tr>
    <tr><td>Performance Score</td><td>{0-100}</td><td>—</td><td>—</td></tr>
    <tr><td>SEO Score</td><td>{0-100}</td><td>—</td><td>—</td></tr>
    <tr><td>LCP</td><td>{N}ms</td><td>&le; 2500ms</td><td class="result-pass">✅</td></tr>
    <tr><td>CLS</td><td>{N}</td><td>&le; 0.1</td><td class="result-pass">✅</td></tr>
    <tr><td>TBT</td><td>{N}ms</td><td>&le; 200ms</td><td class="result-pass">✅</td></tr>
  </table>
</div>

<h2>요약</h2>
<table>
  <tr>
    <th>영역</th><th>합격(✅)</th><th>권고(⚠️)</th><th>불합격(❌)</th><th>해당없음(➖)</th><th>판정불가(🔵)</th><th>합격률</th>
  </tr>
  <tr><td>Technical SEO (11항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr><td>Web Performance (18항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr style="font-weight:bold; background:#f5f5f5;">
    <td>전체 (29항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td><strong>--%</strong></td>
  </tr>
</table>

<h2>상세 결과</h2>

<h3>Technical SEO (11항목)</h3>
<table>
  <tr><th>코드</th><th>우선순위</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <tr>
    <td>SEO-01</td><td>Critical</td><td>noindex 없음</td>
    <td class="result-pass">✅</td>
    <td><span class="method-lighthouse">Lighthouse</span></td>
    <td></td><td></td>
  </tr>
  <tr>
    <td>SEO-02</td><td>Critical</td><td>title 태그 존재하고 고유</td>
    <td class="result-fail">❌</td>
    <td><span class="method-lighthouse">Lighthouse</span></td>
    <td>title 태그가 너무 짧음 (5자)</td>
    <td>50-60자 내외의 서술적 제목 작성</td>
  </tr>
  <tr>
    <td>SEO-03</td><td>Critical</td><td>h1 하나</td>
    <td class="result-pass">✅</td>
    <td><span class="method-static">정적분석</span></td>
    <td></td><td></td>
  </tr>
  <!-- SEO-04 through SEO-11 -->
</table>

<h3>Page Experience / Web Performance (18항목)</h3>
<table>
  <tr><th>코드</th><th>영역</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <tr>
    <td>WP-01</td><td>CRP</td><td>render-blocking script 없음</td>
    <td class="result-pass">✅</td>
    <td><span class="method-lighthouse">Lighthouse</span></td>
    <td></td><td></td>
  </tr>
  <!-- WP-02 through WP-18 -->
  <!-- 정적분석 전용 항목 예시 -->
  <tr>
    <td>WP-07</td><td>JS</td><td>코드 스플리팅</td>
    <td class="result-partial">⚠️</td>
    <td><span class="method-static">정적분석</span></td>
    <td>dynamic import() 미사용</td>
    <td>라우트 기반 코드 스플리팅 적용 권장</td>
  </tr>
</table>

<h2>수정 필요 항목</h2>

<h3>불합격 (❌)</h3>
<!-- 없으면: <p>없음</p> -->
<div class="fix-fail">
  <p><strong>{코드}. {항목명}</strong> — <code>{파일명}:{라인}</code></p>
  <p><strong>문제:</strong> {구체적인 코드 문제}</p>
  <p><strong>수정:</strong> <code>{구체적인 수정 코드}</code></p>
</div>

<h3>권고 (⚠️)</h3>
<!-- 없으면: <p>없음</p> -->
<div class="fix-partial">
  <p><strong>{코드}. {항목명}</strong></p>
  <p><strong>내용:</strong> {개선 권고 내용}</p>
</div>

</body>
</html>
```

---

## CSV Report Template

```
코드,우선순위,항목명,결과,판정방식,발견된 문제,수정 가이드
SEO-01,Critical,noindex 없음,✅,Lighthouse,,
SEO-02,Critical,title 태그 존재하고 고유,❌,Lighthouse,"title 태그가 너무 짧음 (5자)","50-60자 내외의 서술적 제목 작성"
SEO-03,Critical,h1 하나,✅,정적분석,,
SEO-04,Critical,HTTPS 사용,✅,Lighthouse,,
SEO-05,High,meta description,❌,Lighthouse,"meta description 누락","150-160자 내외의 서술적 설명 추가"
SEO-06,High,canonical URL,⚠️,Lighthouse,"canonical URL 미설정","<link rel=""canonical""> 태그 추가"
SEO-07,High,구조화 데이터 (JSON-LD),❌,정적분석,"JSON-LD 구조화 데이터 없음","schema.org 기반 JSON-LD 추가"
SEO-08,Medium,서술적 URL 구조,✅,정적분석,,
SEO-09,High,DOCTYPE html 선언,✅,Lighthouse,,
SEO-10,High,charset UTF-8 최상단,✅,Lighthouse,,
SEO-11,High,viewport meta 태그,✅,Lighthouse,,
WP-01,CRP,render-blocking script 없음,✅,Lighthouse,,
WP-02,CRP,LCP fetchpriority + preload,⚠️,Lighthouse,"LCP 이미지에 fetchpriority 미설정","<img fetchpriority=""high""> 추가"
WP-03,CRP,Critical CSS 처리,✅,Lighthouse,,
WP-04,이미지,img width/height 또는 aspect-ratio,❌,Lighthouse,"이미지 크기 미지정","width/height 속성 또는 aspect-ratio CSS 추가"
WP-05,이미지,loading="lazy",⚠️,Lighthouse,"below-fold 이미지에 lazy loading 미적용","loading=""lazy"" 속성 추가"
WP-06,이미지,WebP/AVIF 포맷,⚠️,Lighthouse,"레거시 이미지 포맷 사용","WebP/AVIF 포맷으로 변환"
WP-07,JS,코드 스플리팅,⚠️,정적분석,"dynamic import() 미사용","라우트 기반 코드 스플리팅 적용"
WP-08,JS,트리 쉐이킹 패턴,✅,정적분석,,
WP-09,JS,레이아웃 스래싱 없음,✅,정적분석,,
WP-10,폰트,font-display 최적화,❌,Lighthouse,"font-display: block 사용","font-display: swap 또는 optional로 변경"
WP-11,폰트,중요 폰트 preload,⚠️,정적분석,"폰트 preload 누락","<link rel=""preload"" as=""font""> 추가"
WP-12,LCP,LCP 요소 초기 HTML 존재,✅,Lighthouse,,
WP-13,INP,이벤트 핸들러 즉각 피드백,✅,정적분석,,
WP-14,INP,무거운 연산 지연 처리,✅,정적분석,,
WP-15,INP,React memo 활용,⚠️,정적분석,"대형 컴포넌트에 memo 미사용","React.memo() 또는 useMemo 적용"
WP-16,CLS,뷰포트 위 동적 삽입 금지,✅,정적분석,,
WP-17,CLS,애니메이션 transform/opacity,✅,Lighthouse,,
WP-18,CLS,동적 콘텐츠 공간 예약,✅,정적분석,,
```
