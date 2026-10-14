# 선물/옵션 정상주문

LS증권 선물/옵션 정상주문 TR `CFOAT00100`를 `submit_futures_option_order` 함수로 제공합니다. 이 기능은 요청한 종목·매매코드·호가유형·가격·수량을 주문 API 형식으로 전달합니다. **호출하면 연결된 계좌로 주문이 즉시 제출됩니다.** 가격 산정, 틱 보정, 종목 선택 같은 전략은 라이브러리 함수에 포함하지 않습니다.

## 기능 구성

- 시세 조회: `fetch_current_price(client, focode)` — `src/ls_openapi/tr/market_data/t2111.py`
- 신규 주문: `submit_futures_option_order(...)` — `src/ls_openapi/tr/orders/CFOAT00100.py`
- 공통 인증/HTTP: `TokenManager` 및 `LSClient` — `auth.py`, `client.py`

TR 기준으로 직접 가져오려면 다음 경로를 사용합니다. 편의를 위해 최상위 `ls_openapi`에서도 두 함수를 내보냅니다.

~~~python
from ls_openapi.tr.market_data.t2111 import fetch_current_price
from ls_openapi.tr.orders.CFOAT00100 import submit_futures_option_order
~~~
- 모의투자 시세+주문 통합 시나리오와 현재가 + 1틱 가격 선택은 라이브 테스트(`tests/live/test_live_order.py`)에만 둡니다. 주문 API 함수는 이 테스트 가격 규칙을 적용하지 않습니다.

## 확인 상태

공식 포털은 `POST /futureoption/order`, TR `CFOAT00100`, 초당 전송 건수 10회를 안내합니다. [공식 주문 API 가이드](https://openapi.ls-sec.co.kr/apiservice?api_id=b579d38a-3ce5-4b1b-b94e-b0c4bbbf1d27&group_id=2f1eea77-5606-4512-93c6-31b21d2ece90). 요청 필드 상세는 포털에서 확인 시 표시되지 않아 제공된 호출 샘플을 기준으로 했습니다.

- Mock HTTP 테스트로 요청 경로, 헤더, 본문과 입력 검사를 확인합니다.
- 모의투자 실서버에서 8자리 월물 코드 4개 각각에 1계약 주문 요청을 제출했고, 성공 응답을 확인했습니다. 모의투자 응답 `rsp_cd=00040`과 “모의투자 매수주문이 완료 되었습니다.”를 접수 성공으로 확인했습니다.
- 이 결과는 주문 요청 접수를 확인한 것이며 실제 체결 여부를 뜻하지 않습니다. `rsp_cd=00040`의 의미가 모든 환경/주문 유형에서 같다고 일반화하지 않습니다.
- 매매코드·호가유형코드의 공식 코드표, 응답 필드 의미, 주문번호 필드는 별도 확인이 필요합니다.
- 정정·취소 주문과 주문 내역 조회는 아직 지원하지 않습니다. 잔고 조회는 `CFOAQ50600`으로 별도 제공합니다 ([docs/balance.md](balance.md)).

## Python API

~~~python
from ls_openapi import LSClient, Settings, TokenManager, submit_futures_option_order

settings = Settings.from_env()
manager = TokenManager(settings)
client = LSClient(settings, token_manager=manager)

try:
    # 인자를 지정한 값 그대로 전달합니다. 이 호출은 실제 계좌로 주문을 제출합니다.
    response = submit_futures_option_order(
        client,
        instrument_code="A0173000",
        side_code="2",
        price_type_code="00",
        order_price=947.10,
        quantity=1,
    )
    print(response.body.get("rsp_cd"), response.body.get("rsp_msg"))
finally:
    manager.revoke()
~~~

`order_price`는 호출자가 결정합니다. 현재가 기준 +1틱이 필요하면 먼저 시세 API를 따로 호출해 가격을 정한 후 주문 함수에 넘기세요. 이 라이브러리는 전략 선택이나 자동 가격 조정을 하지 않습니다.

## 독립 실행 예제

모의투자 앱키를 환경변수 또는 `.env`에 설정하고 저장소 루트에서 실행하세요.

~~~bash
python examples/domestic_futureoption/03_futures_option_order.py A0173000 2 00 947.10 1
~~~

각 인수는 종목코드, 매매코드, 호가유형코드, 주문가격, 수량 순서입니다. 주문 전 계좌와 모든 인수를 확인하세요. 예제는 응답에 포함될 수 있는 계좌 관련 값을 출력하지 않습니다.

## 자동 재시도

주문 요청은 자동 재시도하지 않습니다. 네트워크 오류가 발생했을 때 서버가 주문을 접수했는지 불명확할 수 있으므로, 재호출 전에 계좌 주문 내역을 별도로 확인하세요.