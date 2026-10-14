# 선물/옵션 정상주문

이 저장소는 LS증권 선물/옵션 정상주문 TR CFOAT00100 요청 함수를 제공합니다.
**함수를 호출하면 연결된 계좌로 실제 주문 요청이 전송됩니다.** 모듈 import와 클라이언트 생성만으로 주문이 나가지는 않습니다.

## 지원 범위와 확인 상태

공식 포털은 POST /futureoption/order와 TR CFOAT00100(선물옵션 정상주문), 초당 전송 건수 10회를 안내합니다. [공식 주문 API 가이드](https://openapi.ls-sec.co.kr/apiservice?api_id=b579d38a-3ce5-4b1b-b94e-b0c4bbbf1d27&group_id=2f1eea77-5606-4512-93c6-31b21d2ece90)

포털의 요청 필드 상세는 확인 시점에 표시되지 않았습니다. 구현은 저장소 소유자가 제공한 호출 샘플의 필드명을 따릅니다. 주문 요청은 mock HTTP 세션으로만 확인하며, **실계좌·모의계좌 모두 실서버 주문을 제출하지 않았습니다.** 또한 side/price-type 코드 의미와 응답 필드 해석은 확인되지 않았습니다.

현재 범위는 정상 신규 주문 하나입니다. 정정·취소 주문 및 계좌 주문가능수량 조회는 구현하지 않았습니다.

## API 사용

submit_futures_option_order(client, instrument_code, side_code, price_type_code, order_price, quantity)는 TRResponse를 반환합니다. 응답 본문은 그대로 담으므로 서버 응답 코드를 호출자가 확인해야 합니다.

~~~python
from ls_openapi import LSClient, Settings, TokenManager, submit_futures_option_order

settings = Settings.from_env()
client = LSClient(settings, token_manager=TokenManager(settings))

# 이 호출은 실제 주문 요청을 전송합니다.
response = submit_futures_option_order(
    client,
    instrument_code="101T9000",
    side_code="2",
    price_type_code="00",
    order_price=342.25,
    quantity=5,
)
print(response.body)
~~~

side_code와 price_type_code는 공식 코드표가 검증되기 전까지 문서나 구현에서 의미를 추측하지 않고 전달합니다. 주문은 자동 재시도하지 않습니다.

## Mock 테스트

pytest의 tests/test_orders.py는 가짜 HTTP 세션으로 경로, 헤더, 본문과 입력 검증을 확인합니다. 테스트는 네트워크를 호출하거나 주문을 제출하지 않습니다.

실서버 주문 검증은 이 저장소에서 수행하지 않습니다. 사용자가 별도로 직접 주문 테스트를 결정하더라도, **모의투자 계좌와 최소 수량·가격 등 거래 조건을 확인한 뒤 LS증권의 공식 절차로 실행해야 합니다.**
