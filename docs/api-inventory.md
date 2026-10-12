# API 목록과 확인 상태

이 저장소가 다루는 LS증권 OPEN API의 명세 확인 상태입니다.
기준 자료는 공식 포털의 [시작하기](https://openapi.ls-sec.co.kr/howto-use) 페이지와 포털이 제공하는 TR 명세 JSON(`ls-openapi-tr-guides.json`, 버전 `20261007070834325`)입니다.
다른 증권사의 명세는 적용하지 않았고, 서드파티 라이브러리·블로그에서 본 내용은 근거로 쓰지 않았습니다.

상태 표기: **확인** = 공식 자료에서 직접 확인, **실서버 확인** = 실제 서버를 호출해 동작을 확인(관측 일자와 조건 병기), **미확인** = 공식 자료로 확인하지 못함, **미검증** = 공식 자료에는 있으나 실서버로 동작을 확인하지 않음.

## 서버

| 구분 | 주소 | 상태 |
|---|---|---|
| REST | `https://openapi.ls-sec.co.kr:8080` | 확인 |
| WebSocket(실전) | `wss://openapi.ls-sec.co.kr:9443` | 확인 (이 저장소에서는 미사용) |
| WebSocket(모의) | `wss://openapi.ls-sec.co.kr:29443` | 확인 (이 저장소에서는 미사용) |
| REST(모의투자) | `https://openapi.ls-sec.co.kr:8080` (실전과 동일) | **실서버 확인** — 공식 자료에는 REST 모의 주소가 명시되어 있지 않았으나(모의투자는 앱키/시크릿키만 별도 발급), 모의투자 키로 위 주소에서 토큰 발급·폐기가 성공함 (2026-10-12, 1회 관측, 발급 요청만 확인) |

## 인증

### 접근토큰 발급 — 확인, 구현됨, 실서버 확인 (모의투자 키, 2026-10-12)

- `POST /oauth2/token`, `Content-Type: application/x-www-form-urlencoded`
- 요청 본문

| 필드 | 값 |
|---|---|
| `grant_type` | `client_credentials` 고정 |
| `appkey` | 포털에서 발급된 앱키 |
| `appsecretkey` | 포털에서 발급된 앱 시크릿키 |
| `scope` | `oob` 고정 |

- 응답 필드(실서버 확인): `access_token`, `expires_in`, `scope`(`oob`), `token_type`(`Bearer`). 유효기간 필드명은 `expires_in`입니다.
- "시작하기" 예시는 86400초(24시간)였지만 실제 응답의 `expires_in`은 46332초였습니다(1회 관측). 값이 고정이 아닐 수 있으니 하드코딩하지 말고 응답 값을 사용하세요.
- 구현: `src/ls_openapi/auth.py` (`issue_token`, `TokenManager`)

### 접근토큰 폐기 — 확인, 구현됨, 실서버 확인 (모의투자 키, 2026-10-12)

- `POST /oauth2/revoke`, `Content-Type: application/x-www-form-urlencoded`
- 요청 본문: `appkey`, `appsecretkey`, `token_type_hint`(`access_token` 또는 `refresh_token`), `token`
- 응답 필드(실서버 확인): `code`, `message`. 성공 시 `code`는 `200`, `message`는 "접근토큰 폐기에 성공하였습니다."였습니다(1회 관측). 실패 시의 `code` 값은 확인하지 않았고, 코드는 응답을 해석하지 않고 그대로 반환합니다.
- 구현: `src/ls_openapi/auth.py` (`revoke_token`, `TokenManager.revoke`)

## TR 호출 공통 규칙 — 확인, 구현됨 (실서버 미검증)

업종 시세(`/indtp/market-data`) 등 REST TR 명세에서 공통으로 확인된 형식입니다. 국내선물 TR에도 같은 형식이 적용될 것으로 보이지만, 해당 TR 명세를 직접 확인하기 전까지는 가정입니다.

| 항목 | 내용 |
|---|---|
| 메서드 | `POST` (명세의 기본값) |
| 요청 헤더 | `content-type`(`application/json; charset=utf-8`), `authorization`(접근토큰), `tr_cd`(거래 코드), `tr_cont`(연속 여부 `Y`/`N`), `tr_cont_key`(연속 키), `mac_address`(법인만 필수) |
| 요청 본문 | `{"<TR코드>InBlock": {...}}` |
| 응답 헤더 | `tr_cd`, `tr_cont`, `tr_cont_key` |
| 응답 본문 | `<TR코드>OutBlock`, `<TR코드>OutBlock1` 등 (TR마다 다름) |

- 구현: `src/ls_openapi/client.py` (`LSClient.post_tr`, `build_in_block`). 개별 API(TR 코드, 경로)는 들어 있지 않습니다.
- 토큰 응답의 `token_type`은 실서버에서 `Bearer`로 확인했습니다. 다만 `authorization` 헤더에 `Bearer ` 접두사를 붙여 TR을 호출하는 동작은 실제 TR 호출로 확인하지 않아 **미검증**입니다.

## 국내선물 시세 조회 — 미확인, 미구현

아래 항목은 모두 공식 자료로 확인하지 못해 구현하지 않았습니다.

| 항목 | 상태 |
|---|---|
| API 이름, TR 코드 | 미확인 |
| 엔드포인트 경로 | 미확인 |
| 요청 InBlock 필수 파라미터 | 미확인 |
| 응답 OutBlock 구조 | 미확인 |
| 초당 호출 제한 (TR별) | 미확인 |
| 연속조회 방식 | 미확인 |

확인 방법: 포털 "시작하기" 하단의 `ls-openapi-tr-guides.json`을 내려받아 `[선물/옵션] 시세` 카테고리의 해당 TR 항목을 확인합니다. 확인되면 이 표를 채우고 구현을 추가합니다.

## 자료 간 불일치

| 항목 | 내용 | 현재 처리 |
|---|---|---|
| 토큰 유효기간 필드명 | TR 명세 JSON은 `expire_in`, "시작하기" 예시 응답은 `expires_in` | **해결**: 실서버 응답은 `expires_in` (2026-10-12). 코드는 두 이름을 모두 허용하되 `expires_in`을 우선 사용 |
| 시세 호출 예시 | "시작하기"의 주식 현재가 예시는 `GET`, 헤더 `tr_id` 사용. TR 명세 JSON은 `POST`, 헤더 `tr_cd` | TR 명세 JSON을 기준으로 삼음. 예시 코드는 따르지 않음 |

## 범위 제외

- 주문 API: MVP에서 구현하지 않습니다.
- 실시간(WebSocket) 시세: MVP 범위가 아닙니다.
- 업종, ELW, 주식, 해외 등 국내선물 외 API
