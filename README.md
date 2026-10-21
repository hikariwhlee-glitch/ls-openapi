# ls-openapi

LS증권 국내 선물·옵션 Open API를 활용하는 비공식 Python 프로젝트입니다. 이 저장소에서 제공하는 실행 코드와 패키지는 Python만 지원합니다.

## 1차 MVP — 공식 예제와 명세 바로가기

LS증권 공식 API 서비스는 국내 선물·옵션의 TR 명세와 여러 언어의 공식 샘플을 제공합니다. 이 저장소는 공식 샘플 링크와 명세를 참고 자료로 연결하고, 직접 실행·재사용할 Python 클라이언트와 예제를 제공합니다. Java 및 JavaScript 구현은 제공하지 않습니다.

- [국내 선물·옵션 TR별 공식 샘플 인덱스](docs/official-samples.md)
- [공식 명세 JSON 스냅샷](specs/domestic-futures-options.json)
- [사람이 읽는 전체 명세](docs/domestic-futures-options.md)
- [LS증권 API 서비스](https://openapi.ls-sec.co.kr/apiservice)
- [Python SDK 사용 안내](docs/sdk.md)

샘플 JSON 링크는 LS증권 공식 사이트의 샘플 데이터를 엽니다. 그 데이터에 Python 외 언어의 공식 예제가 포함될 수 있지만, 이 저장소가 제공하는 코드는 Python뿐입니다. 공식 코드 원문은 복제하지 않고 출처 링크와 검색용 인덱스를 제공합니다.

## Python에서 바로 사용

Python 3.10 이상에서 저장소를 받은 뒤 의존성을 설치합니다. API 키는 LS증권 Open API에서 발급하고 환경변수로 설정하세요.

```bash
pip install -e .
# PowerShell 예시
$env:LS_APP_KEY="발급받은 앱키"
$env:LS_APP_SECRET="발급받은 앱시크릿"
$env:LS_FUTURES_CODE="조회할 선물 종목코드"
python examples/futures_quote.py
```

`t2111` 현재가와 `t8464` 차트 조회, `FC9` 실시간 구독 예제를 `examples/`에 두었습니다. TR을 직접 다루는 저수준 API와, 자주 쓰는 기능을 이름으로 호출하는 도메인 SDK를 함께 제공합니다.

### 도메인 SDK

```python
import os
from ls_openapi import LSFutureClient

client = LSFutureClient()
quote = client.market.quote(os.environ["LS_FUTURES_CODE"])
print(quote["t2111OutBlock"])

balance = client.account.balance()
```

`client.market`은 국내 파생상품 검색·현재가·호가·틱차트, `client.account`는 잔고·주문내역 조회를 제공합니다. 종목은 자연어로 검색할 수 있습니다.

```python
# 지수, 개별주식, 상품 선물 마스터를 검색하고 조건에 맞는 계약 후보를 반환합니다.
result = client.market.search_instruments(
    "삼성전자 주식선물 찾아줘",
    instrument_type="futures",
    asset_class="stock",
)
for item in result["results"]:
    print(item["name"], item["code"], item["asset_class"])

# 미니/위클리 등 조건이 있으면 후보 검색에 반영됩니다.
result = client.market.search_instruments(
    "코스피200 위클리 400 콜옵션",
    instrument_type="options",
    asset_class="index",
)
```

선물은 지수·개별주식·상품 마스터를 지원하며, 옵션은 LS의 지수옵션 마스터(정규·미니·위클리)를 지원합니다. 여러 만기나 행사가가 남으면 한 계약을 임의로 고르지 않고 후보를 반환합니다. MCP 도구 설명은 AI가 자연어 요청에서 상품 종류와 분류를 인식해 이 검색 인자에 넣도록 안내합니다. 전체 구조와 사용 예는 [SDK 안내](docs/sdk.md)를 참고하세요.

### 전체 TR 직접 호출

편의 메서드가 없는 TR도 `LSOpenAPI.call()`로 호출할 수 있습니다. 여러 입력 블록이 필요한 TR은 공식 필드명으로 전체 블록 구조를 `body=`에 전달합니다. 연속조회는 `iter_pages()`를 사용합니다. 전체 TR 목록은 `ls_openapi/catalog.py`에 있습니다.

주문·정정·취소는 기본 차단됩니다. 메서드가 필요한 경우에만 `LSFutureClient(allow_orders=True)`를 명시하세요. 이 설정은 실계좌 주문도 가능하게 합니다. API 호출에는 발급받은 키와 계좌 권한이 필요합니다.

## Codex 로컬 MCP

Windows에서는 저장소를 받은 뒤 `setup-codex-mcp.cmd`를 더블클릭하면 Python 가상환경과 MCP 서버를 설치하고 Codex에 등록합니다. 설치 중 LS 앱키와 시크릿을 입력하면 로컬 `.env`에 저장됩니다.

- [Codex 로컬 MCP 쉬운 설치 안내](docs/mcp-codex.md)

MCP는 종목 검색·현재가·호가·잔고·차트 조회 도구를 제공하며 주문 기능은 노출하지 않습니다. Codex가 사용자 PC에서 로컬로 실행하므로 별도 클라우드 서버가 필요하지 않습니다.

## 공식 자료 갱신

Python 3.9 이상이 필요합니다. 외부 패키지 없이 두 스크립트를 실행할 수 있습니다.

```bash
python scripts/sync_official_specs.py
python scripts/sync_official_sample_index.py
```

첫 번째 스크립트는 공식 명세 JSON과 읽기용 문서를 갱신합니다. 두 번째 스크립트는 공식 사이트의 국내 선물·옵션 TR 목록과 상세 페이지 링크를 다시 수집해 인덱스를 갱신합니다.

## 2차 MVP — 백테스터

백테스터는 2차 MVP 범위입니다. 국내 파생상품 명세와 공식 조회 예제를 먼저 파악한 뒤 과거 데이터 수집·정규화와 백테스트 엔진을 설계합니다. 이 저장소는 LS증권과 무관한 비공식 개인 프로젝트입니다.
