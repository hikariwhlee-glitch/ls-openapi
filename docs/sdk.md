# Python SDK 구성

현재 SDK는 기존 REST/WebSocket 구현 위에 도메인별 진입점을 제공하는 얇은 파사드입니다. 기본값으로 조회 전용이며 응답은 LS 원본 딕셔너리를 그대로 반환합니다.

```text
LSFutureClient
├── market      search_instruments, quote, orderbook, tick_chart
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

| 영역 | 메서드 | 주요 TR | 결과 |
|---|---|---|---|
| 종목 | `client.market.search_instruments(query, instrument_type, asset_class, limit)` | t9943, t9944, t8433, t8435, t8401, t8426, t8467 | 상품 분류와 이름·단축코드·확장코드가 포함된 계약 후보 |
| 시세 | `client.market.quote(code)` | t2111 | LS 원본 응답 딕셔너리 |
| 시세 | `client.market.orderbook(code)` | t2112 | LS 원본 응답 딕셔너리 |
| 시세 | `client.market.tick_chart(code, ...)` | t8464 | LS 원본 응답 딕셔너리 |
| 계좌 | `client.account.balance()` | t0441 | LS 원본 응답 딕셔너리 |
| 계좌 | `client.account.orders(...)` | t0434 | LS 원본 응답 딕셔너리 |

## 상품 마스터 검색

`search_instruments`는 검색어를 정규화해 LS 공식 종목 마스터 응답과 대조합니다. 검색 대상은 다음과 같습니다.

- 선물: 지수선물(코스피200, 변동성·섹터, 코스닥150, 미니), 주식선물, 상품선물
- 옵션: 지수옵션(정규, 미니, 코스피200·코스닥150 위클리)
- 분류: `asset_class="index"`, `"stock"`, `"commodity"`, `"all"`
- 계약 종류: `instrument_type="futures"` 또는 `"options"`

```python
# 직접 사용하는 SDK에서는 검색 분류와 종류를 지정합니다.
candidates = client.market.search_instruments(
    "삼성전자 주식선물",
    instrument_type="futures",
    asset_class="stock",
)
for item in candidates["results"]:
    print(item["name"], item["code"], item["asset_class"])

options = client.market.search_instruments(
    "코스피200 위클리 400 콜옵션",
    instrument_type="options",
    asset_class="index",
)
```

MCP 도구는 사용자 자연어에서 상품 종류와 분류를 추출해 인자에 전달하도록 설명되어 있습니다. 한국어·영어 별칭과 흔한 요청 문구를 정규화하지만, 검색 자체는 공식 마스터의 이름·코드와 조건을 비교하는 결정적 로직입니다. AI가 자연어를 이해한다고 해서 서버가 임의로 만기·행사가를 선택하지는 않습니다.

마스터에는 공통 만기 필드가 없거나 상품별 표시 방식이 다를 수 있습니다. 따라서 여러 만기·행사가 후보가 반환되면 모두 보여주고, 요청이 불명확할 때는 사용자가 원하는 계약을 확인합니다. 주식옵션과 상품옵션은 현재 LS 국내 마스터 검색 대상에 없습니다.

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
