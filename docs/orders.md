# 선물/옵션 주문

선물/옵션 주문 TR을 기능별 모듈로 제공합니다.

| 기능 | TR | 함수 | 모듈 |
|---|---|---|---|
| 정상주문 | `CFOAT00100` | `submit_futures_option_order` | `orders/CFOAT00100.py` |
| 정정주문 | `CFOAT00200` | `modify_futures_option_order` | `orders/CFOAT00200.py` |
| 취소주문 | `CFOAT00300` | `cancel_futures_option_order` | `orders/CFOAT00300.py` |

각 함수는 전달된 주문 필드를 해당 TR 요청 블록에 넣어 `POST /futureoption/order`로 호출하고 원본 응답을 `TRResponse.body`로 반환합니다. 가격 산정, 틱 보정, 주문 선택 같은 전략은 포함하지 않습니다.

## 주의

정정 함수는 기존 주문의 가격/수량을 변경하고, 취소 함수는 기존 주문을 취소합니다. 호출 전에 계좌 환경, 종목코드, 원주문번호와 수량을 반드시 확인하세요. 두 기능의 경로·요청 필드명·자료형·길이는 공식 가이드 JSON 및 사용자가 제공한 호출 샘플을 대조해 구현했습니다. 아직 모의투자 실서버 검증은 하지 않았습니다. 자동 재시도도 하지 않습니다.

## 정정주문 CFOAT00200

공식 가이드 JSON 기준 요청 블록은 `CFOAT00200InBlock1`이며 초당 제한은 10회입니다. 필드는 다음과 같습니다.

| 필드 | 자료형/길이 | 설명 |
|---|---|---|
| `FnoIsuNo` | String / 12 | 선물옵션 종목번호 |
| `OrgOrdNo` | Number / 10 | 원주문번호 |
| `FnoOrdprcPtnCode` | String / 2 | 선물옵션 호가유형코드 (샘플은 지정가 `00`) |
| `FnoOrdPrc` | Number / 27.8 | 정정 주문가격 |
| `MdfyQty` | Number / 16 | 정정 수량 |


~~~python
from ls_openapi import LSClient, Settings, TokenManager, modify_futures_option_order

settings = Settings.from_env()
manager = TokenManager(settings)
client = LSClient(settings, token_manager=manager)

try:
    response = modify_futures_option_order(
        client,
        instrument_code="101T9000",
        original_order_number=67005,
        price_type_code="00",
        order_price=342.3,
        quantity=1,
    )
    print(response.body.get("rsp_cd"), response.body.get("rsp_msg"))
finally:
    manager.revoke()
~~~

## 취소주문 CFOAT00300

공식 가이드 JSON 기준 요청 블록은 `CFOAT00300InBlock1`이며 초당 제한은 10회입니다. 필드는 다음과 같습니다. | 필드 | 자료형/길이 | 설명 |
|---|---|---|
| `FnoIsuNo` | String / 12 | 선물옵션 종목번호 |
| `OrgOrdNo` | Number / 10 | 원주문번호 |
| `CancQty` | Number / 16 | 취소 수량 |


~~~python
from ls_openapi import LSClient, Settings, TokenManager, cancel_futures_option_order

settings = Settings.from_env()
manager = TokenManager(settings)
client = LSClient(settings, token_manager=manager)

try:
    response = cancel_futures_option_order(
        client,
        instrument_code="101T9000",
        original_order_number=68002,
        quantity=2,
    )
    print(response.body.get("rsp_cd"), response.body.get("rsp_msg"))
finally:
    manager.revoke()
~~~

샘플 원주문번호는 요청 형식 예시일 뿐입니다. 실제 계좌에서 해당 주문번호를 확인하고 사용하세요.

## 정상주문

정상주문은 `submit_futures_option_order`가 제공합니다. 정상주문 실서버 검증 결과와 기존 예제는 이전 내용을 따릅니다. 함수는 호출자가 지정한 가격과 수량 그대로 요청하며 시세 기반 결정을 하지 않습니다.

주문 응답 접수 여부를 체결 완료와 혼동하지 마세요. 계좌 주문 내역이나 체결 조회는 별도 기능입니다.
