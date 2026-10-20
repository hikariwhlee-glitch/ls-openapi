# Python SDK 구성

현재 SDK는 기존 REST/WebSocket 구현 위에 도메인별 진입점을 제공하는 얇은 파사드입니다. 기본값으로 조회 전용이며 응답은 LS 원본 딕셔너리를 그대로 반환합니다.

```text
LSFutureClient
├── market      quote, orderbook, tick_chart
├── account     balance, orders
├── orders      new, amend, cancel (allow_orders=True 필요)
├── websocket() 실시간 연결 객체 생성
└── call()      전체 카탈로그의 REST TR 직접 호출
    iter_pages() REST 연속 조회
```

## 빠른 시작

```python
import os
from ls_openapi import LSFutureClient

client = LSFutureClient()
quote = client.market.quote(os.environ["LS_FUTURES_CODE"])
print(quote["t2111OutBlock"])
```

현재 편의 함수가 없는 TR은 기존 저수준 메서드로 계속 사용할 수 있습니다.

```python
result = client.call("t2112", {"shcode": os.environ["LS_FUTURES_CODE"]})
```

## 현재 편의 함수

| 영역 | 메서드 | TR | 결과 |
|---|---|---|---|
| 시세 | `client.market.quote(code)` | t2111 | LS 원본 응답 딕셔너리 |
| 시세 | `client.market.orderbook(code)` | t2112 | LS 원본 응답 딕셔너리 |
| 시세 | `client.market.tick_chart(code, ...)` | t8464 | LS 원본 응답 딕셔너리 |
| 계좌 | `client.account.balance()` | t0441 | LS 원본 응답 딕셔너리 |
| 계좌 | `client.account.orders(...)` | t0434 | LS 원본 응답 딕셔너리 |

## 주문 권한

주문 메서드는 의도적으로 기본 차단됩니다. 모의투자 또는 실계좌 주문을 호출하려는 사용자가 생성 시 권한을 분명히 켜야 합니다.

```python
client = LSFutureClient(allow_orders=True)
response = client.orders.new(
    instrument_code="주문용 종목코드",
    side="buy",
    quantity=1,
    price=123.45,
)
```

`allow_orders=True`는 실계좌 주문도 가능하게 하므로 호출 전에 환경과 계좌를 확인하세요. 주문 메서드는 LS API에 요청을 전달할 뿐, 체결을 보장하거나 포지션을 관리하지 않습니다. 취소 수량은 LS 명세에 맞춰 문자열로 전송됩니다.

## 실시간 시세

```python
with client.websocket(simulated=True) as feed:
    feed.subscribe("FC9", os.environ["LS_FUTURES_CODE"])
    message = feed.recv()
    print(message)
    feed.unsubscribe("FC9", os.environ["LS_FUTURES_CODE"])
```

현재 버전은 WebSocket 연결과 구독/수신을 노출합니다. 재연결, 비동기 스트림, 이벤트별 정규화는 후속 단계입니다.

## 다음 확장 단계

1. 계좌·시세 응답을 이름 있는 데이터 모델로 변환합니다.
2. TR별 입력 파라미터와 반환 타입을 명세로 검증합니다.
3. 주문 상태와 체결 이벤트를 연계하는 고수준 기능은 주문 정정/취소 경로를 추가 검증한 뒤 설계합니다.
4. 전체 TR은 저수준 `call()`로 계속 접근 가능하도록 유지합니다.
