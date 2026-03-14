# KWCAG2.2 Fix Guide Reference

**Source:** 한국지능정보사회진흥원, 2024.10 | **Items:** 33개

스크립트(`scripts/scan.py`)가 탐지한 위반 항목의 수정 가이드입니다.
`❌` 또는 `⚠️` 판정 시 해당 항목의 Fix Guide를 참조하여 구체적인 수정 방법을 제시합니다.

---

## 원칙 1. 인식의 용이성

### A-01. 적절한 대체 텍스트
- 의미 있는 이미지: `<img src="chart.png" alt="2024년 1분기 매출 그래프">`
- 장식 이미지: `<img src="bullet.png" alt="">` (빈 alt)
- 복잡한 이미지: alt에 요약 + `aria-describedby` 제공
- `<input type="image">`: `alt` 속성 필수

### A-02. 자막 제공
- `<video>` → `<track kind="captions" src="captions.vtt" srclang="ko">` 추가
- 또는 영상 아래 전체 스크립트(원고) 텍스트 제공

### A-03. 표의 구성
- 데이터 표: `<caption>` 추가, 헤더 셀은 `<th scope="col/row">`
- 복잡한 표: `<th id="h1">`, `<td headers="h1">` 로 셀-헤더 연결

### A-04. 콘텐츠의 선형 구조
- 시각적 순서와 DOM 순서를 일치시키거나, `order` CSS 대신 HTML 순서 자체를 조정

### A-05. 명확한 지시 사항
- "빨간 버튼을 누르세요" → "저장 버튼을 누르세요" (명칭 사용)
- 색·위치 정보 사용 시 텍스트 레이블 병행 제공

### A-06. 색에 무관한 인식
- 필수 항목: 빨간 별(*) + "필수" 텍스트 병행
- 오류 표시: 빨간 테두리 + 오류 아이콘(⚠) + 오류 문구 제공

### A-07. 자동 재생 금지
- `autoplay` 속성 제거
- 자동 재생 필요 시 `muted` 속성 추가 + 정지 버튼 제공

### A-08. 명도 대비
- 일반 텍스트(18pt 미만): 4.5:1 이상 (흰 배경 #FFFFFF에 `#767676` 이상)
- 큰 텍스트(18pt 이상, 굵은 14pt 이상): 3:1 이상
- UI 컴포넌트(아이콘, 버튼 테두리): 3:1 이상

### A-09. 콘텐츠 구분
- 콘텐츠 블록 사이에 `border`, `padding`, `background-color` 등 시각적 구분 추가

---

## 원칙 2. 운용의 용이성

### A-10. 키보드 사용 보장
- 클릭 가능 요소는 `<button>` 또는 `<a>` 사용
- 커스텀 요소: `role="button"` + `tabIndex={0}` + `onKeyDown` 추가

### A-11. 초점 이동과 표시
- `outline: none` 제거 또는 `outline: 2px solid #005FCC` 등 커스텀 포커스 스타일 제공
- 모달: `focus-trap` 구현, 닫힘 시 원래 위치로 포커스 복귀

### A-12. 조작 가능
- 버튼 최소 크기: `min-width: 44px; min-height: 44px`
- 작은 아이콘 버튼: `padding`으로 터치 영역 확장

### A-13. 문자 단축키
- 단일 문자 단축키 비활성화 UI 제공 또는 수정키(Ctrl/Alt/Shift) 조합으로 변경

### A-14. 응답시간 조절
- 만료 20초 전 연장 확인 모달 표시
- 세션 연장 API 연동 버튼 제공

### A-15. 정지 기능
- 자동 슬라이드: 재생/정지 버튼 추가
- `prefers-reduced-motion` 미디어 쿼리 대응

### A-16. 깜박임 제한
- 깜박임 효과 제거 또는 주기를 3Hz 미만으로 변경
- 불가피한 경우 사전 경고 문구 표시

### A-17. 반복 영역 건너뛰기
```html
<a href="#main-content" class="skip-nav">본문 바로가기</a>
<!-- .skip-nav { position: absolute; top: -40px; } .skip-nav:focus { top: 0; } -->
<main id="main-content">...</main>
```

### A-18. 제목 제공
- `<title>페이지명 - 서비스명</title>` 형식
- `<iframe title="광고 배너">` 형식으로 의미 있는 title 제공
- 헤딩 계층: `h1` → `h2` → `h3` 순서 준수 (건너뜀 금지)

### A-19. 적절한 링크 텍스트
- `<a href="...">공지사항 더보기</a>` (맥락 포함)
- 아이콘 링크: `<a href="..."><img src="icon.svg" alt="다음 페이지로 이동"></a>`
- `aria-label="공지사항 더보기"` 활용

### A-20. 고정된 참조 위치
- 전자책 뷰어: 현재 페이지/전체 페이지 표시 + 페이지 이동 컨트롤 제공

### A-21. 단일 포인터 입력 지원
- 드래그 슬라이더: +/- 버튼 또는 직접 입력 필드 병행 제공
- 지도: 확대/축소 버튼 추가

### A-22. 포인터 입력 취소
- `onClick` (mouseup 기반) 사용 (`onMouseDown` 대신)
- 중요한 동작(삭제, 결제): 확인 다이얼로그 추가

### A-23. 레이블과 네임
- 아이콘 버튼: `<button aria-label="검색">🔍</button>`
- 시각적 레이블과 동일하거나 포함하는 `aria-label` 사용

### A-24. 동작 기반 작동
- 흔들기 기능: "흔들기" 버튼 또는 "동작 기반 기능 끄기" 설정 제공

---

## 원칙 3. 이해의 용이성

### A-25. 기본 언어 표시
- `<html lang="ko">` 추가 (한국어 서비스 기준)

### A-26. 사용자 요구에 따른 실행
- 새 창 열기: 링크 텍스트에 "(새 창)" 안내 또는 아이콘 제공
- select 자동 이동: 별도 "이동" 버튼 제공

### A-27. 찾기 쉬운 도움 정보
- 고객센터·FAQ·챗봇 링크를 헤더 또는 푸터에 일관된 위치로 고정

### A-28. 오류 정정
- 오류 시: `aria-invalid="true"` + `aria-describedby="error-msg"` + 오류 메시지
- 오류 발생 시 해당 필드로 초점 이동

### A-29. 레이블 제공
```html
<label for="email">이메일</label>
<input type="email" id="email" name="email">
<!-- 또는 -->
<input type="email" aria-label="이메일" placeholder="example@email.com">
```

### A-30. 접근 가능한 인증
- CAPTCHA 사용 시 이메일/SMS 인증 등 대체 수단 병행 제공

### A-31. 반복 입력 정보
- `<input autocomplete="email">` 등 `autocomplete` 속성 지정
- 다단계 폼: 이전 단계 입력값 자동 채움

---

## 원칙 4. 견고성

### A-32. 마크업 오류 방지
- `id`는 페이지 내 유일해야 함 (반복 컴포넌트에 동일 id 사용 금지)
- HTML 유효성: `<p>` 내부에 블록 요소 사용 금지
- 리스트 렌더링: `key` prop 추가

### A-33. 웹 애플리케이션 접근성
- 커스텀 탭: `role="tab"` + `aria-selected="true/false"` + `aria-controls="panel-id"`
- 커스텀 모달: `role="dialog"` + `aria-modal="true"` + `aria-labelledby="modal-title"`
- 토글 버튼: `role="button"` + `aria-pressed="true/false"`

---

## 시맨틱 HTML

### S-01. 표현용 태그
- `<b>` → `<strong>`, `<i>` → `<em>` 또는 CSS로 대체

### S-02. 줄바꿈 남용
- 연속 `<br><br>` → `<p>` 태그 사용

### S-03. 랜드마크 요소
- `<header>`, `<main>`, `<footer>`, `<nav>` 적극 활용

### S-04. 대화형 요소
- 클릭 가능 `<div>`/`<span>` → `<button>` 또는 `<a>` 사용

### S-05. 목록 구조
- 반복 항목 `<div>` 나열 → `<ul>`/`<ol>` + `<li>` 사용

### S-06. 폼 그룹
- 관련 입력 필드 그룹 → `<fieldset>` + `<legend>` 사용

### S-07. 기타 시맨틱 요소
- 인용문: `<blockquote>`/`<q>`, 날짜: `<time datetime="...">`
