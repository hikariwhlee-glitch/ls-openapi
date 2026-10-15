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

공식 가이드 JSON 기준 요청 블록은 `CFOAT00300InBlock1`이며 초당 제한은 10회입니다. 필드는 다음과 같습니다.

| 필드 | 자료형/길이 | 설명 |
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

## 정상주문 CFOAT00100

공식 포털은 `POST /futureoption/order`, 초당 10회를 안내합니다. 요청 필드는 사용자가 제공한 호출 샘플 기준입니다.

| 필드 | 설명 | 상태 |
|---|---|---|
| `FnoIsuNo` | 선물옵션 종목번호 (8자리 월물 코드, 예: `A0173000`) | 샘플 기준 |
| `BnsTpCode` | 매매구분코드 (모의투자 매수 주문에 `2` 사용) | 코드표 미확인 |
| `FnoOrdprcPtnCode` | 호가유형코드 (지정가 `00` 사용) | 코드표 미확인 |
| `FnoOrdPrc` | 주문가격 | 샘플 기준 |
| `OrdQty` | 주문수량 | 샘플 기준 |

~~~python
from ls_openapi import LSClient, Settings, TokenManager, submit_futures_option_order

settings = Settings.from_env()
manager = TokenManager(settings)
client = LSClient(settings, token_manager=manager)

try:
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

**실서버 확인:** 모의투자에서 8자리 월물 코드 4개에 1계약 매수 주문을 제출해 접수 응답을 받았습니다(`rsp_cd=00040`, "모의투자 매수주문이 완료 되었습니다."). 접수 확인일 뿐 체결 여부는 아닙니다. `00040`의 의미가 모든 환경·주문 유형에서 같다고 일반화하지 않습니다. 응답 필드 의미와 주문번호 필드는 확인되지 않았습니다.

주문 응답 접수 여부를 체결 완료와 혼동하지 마세요. 계좌 주문 내역이나 체결 조회는 별도 기능입니다.

## 예제

모의투자 앱키를 `.env`에 넣고 저장소 루트에서 실행합니다. 모든 예제는 호출 즉시 주문을 제출·변경·취소하며 응답코드, 메시지, 필드 이름만 출력합니다.

~~~bash
python examples/domestic_futureoption/03_futures_option_order.py <종목코드> <매매코드> <호가유형코드> <주문가격> <수량> [--show-response]
python examples/domestic_futureoption/05_modify_order.py <종목코드> <원주문번호> <호가유형코드> <정정가격> <정정수량>
python examples/domestic_futureoption/06_cancel_order.py <종목코드> <원주문번호> <취소수량>
~~~

## 모의투자에서 정정·취소 확인하기

1. 체결되지 않을 가격으로 정상주문을 내고 `--show-response`로 전체 응답을 봅니다. 응답에 계좌 정보가 있을 수 있으니 내 PC에서만 보고 공개 장소에 올리지 마세요.
2. 응답에서 주문번호 필드를 직접 찾습니다. 필드명은 확인되지 않았습니다.
3. 그 번호로 `05_modify_order.py`, `06_cancel_order.py`를 실행합니다.

정정수량·취소수량이 변경·취소할 수량인지 전체 잔량인지는 확인되지 않았습니다. 1계약으로 먼저 동작을 확인하고, 확인된 응답코드·메시지는 [api-inventory.md](api-inventory.md)에 기록하세요.
