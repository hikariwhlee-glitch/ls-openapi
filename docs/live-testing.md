# 실서버(모의투자) 점검

자동 단위 테스트는 없고, 모의투자 키로 실서버를 직접 호출해 점검합니다. 방법은 두 가지입니다.

## 1. GitHub Actions에서 수동 실행

앱키가 코드에 남지 않고 GitHub Secrets에 암호화되어 저장됩니다.

**준비 (한 번만)**
1. Settings > Secrets and variables > Actions에 `LS_APP_KEY`, `LS_APP_SECRET`(모의투자 키)을 등록합니다.
2. Variables에 `LS_FOCODE`를 등록합니다. 8자리 월물 코드이며 쉼표로 여러 개를 넣을 수 있습니다(예: `A016C000,A0173000`).
3. (권장) Settings > Environments에서 `live-test` 환경을 만들고 Required reviewers를 지정합니다. 워크플로가 이 환경을 사용하므로, 만들지 않으면 환경이 자동 생성됩니다.

**실행:** Actions 탭 > `live-check (모의투자 수동 점검)` > Run workflow에서 항목을 고릅니다.

| 항목 | 내용 | 비고 |
|---|---|---|
| `auth` | 토큰 발급 → 폐기 | |
| `quote` | `t2111` 현재가 조회 (종목코드마다) | 값이 모두 0이거나 종목코드가 다르면 실패 |
| `orderbook` | `t2112` 호가 조회 | 응답 구조 확인용 |
| `master` | `t8467` 지수선물 마스터 조회 | 필드 이름과 행 수만 출력 |
| `websocket` | 모의투자 WebSocket 연결, `FC9`·`FH9` 구독 후 20초 수신 | 장 마감 중이면 수신 0건일 수 있음(실패로 보지 않음) |
| `order-cycle` | 정상주문 → 정정 → 취소 | **모의투자 주문이 실제로 나갑니다.** `confirm`에 `ORDER` 입력 필요 |

`order-cycle`은 현재가보다 5포인트 낮은 지정가로 1계약 매수 주문을 내서 체결되지 않게 하고, 응답에서 주문번호 필드(`OrdNo`)를 찾아 정정·취소에 씁니다. 필드를 찾지 못하면 실패하고 응답 필드 이름을 보여 줍니다. 정정이나 중간 단계가 실패해도 주문번호가 있으면 취소를 시도해 미체결 주문이 남지 않게 합니다.

**로그 공개 범위:** 저장소가 공개라 Actions 로그도 공개됩니다. 스크립트는 앱키·토큰·계좌 정보와 주문 응답 값을 출력하지 않고, 응답코드·메시지·필드 이름만 출력합니다. 시세 값은 공개 데이터라 출력합니다.

## 2. 내 PC에서 실행

`.env`에 모의투자 앱키를 넣고 저장소 루트에서 실행합니다.

~~~bash
pip install -e .
python scripts/live_check.py auth
python scripts/live_check.py quote A016C000,A0173000
python scripts/live_check.py order-cycle A0173000
~~~

## 성공 판정에 대해

`orderbook`, `master`, `order-cycle`은 `rsp_cd`가 `00`으로 시작하면 성공으로 봅니다. 공식 코드표로 확인한 규칙이 아니라 지금까지 관측한 `00000`(조회 완료)과 `00040`(모의투자 매수주문 완료)에 기대는 임시 기준입니다. 새 응답코드를 확인하면 [api-inventory.md](api-inventory.md)에 기록하고 기준을 고치세요.
