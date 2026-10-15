# ls-openapi

LS증권 국내 선물·옵션 Open API를 활용하는 비공식 Python 프로젝트입니다. 이 저장소에서 제공하는 실행 코드와 패키지는 Python만 지원합니다.

## 1차 MVP — 공식 예제와 명세 바로가기

LS증권 공식 API 서비스는 국내 선물·옵션의 TR 명세와 여러 언어의 공식 샘플을 제공합니다. 이 저장소는 공식 샘플 링크와 명세를 참고 자료로 연결하고, 직접 실행·재사용할 Python 클라이언트와 예제를 제공합니다. Java 및 JavaScript 구현은 제공하지 않습니다.

- [국내 선물·옵션 TR별 공식 샘플 인덱스](docs/official-samples.md)
- [공식 명세 JSON 스냅샷](specs/domestic-futures-options.json)
- [사람이 읽는 전체 명세](docs/domestic-futures-options.md)
- [LS증권 API 서비스](https://openapi.ls-sec.co.kr/apiservice)

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

`t2111` 현재가와 `t8464` 차트 조회, `FC9` 실시간 구독 예제를 `examples/`에 두었습니다. 모든 REST TR은 `LSOpenAPI.call()`로 호출할 수 있으며, 여러 입력 블록이 필요한 TR은 공식 필드명으로 전체 블록 구조를 `body=`에 전달합니다. 연속조회는 `iter_pages()`를 사용할 수 있습니다. TR 목록은 `ls_openapi/catalog.py`에서 확인합니다.

주문·정정·취소 TR은 기본 차단됩니다. 실제 주문 기능을 사용해야 할 때만 `LSOpenAPI(allow_orders=True)`를 명시하세요. 예제는 조회용이며 API 호출에는 발급받은 키와 계좌 권한이 필요합니다.

## 공식 자료 갱신

Python 3.9 이상이 필요합니다. 외부 패키지 없이 두 스크립트를 실행할 수 있습니다.

```bash
python scripts/sync_official_specs.py
python scripts/sync_official_sample_index.py
```

첫 번째 스크립트는 공식 명세 JSON과 읽기용 문서를 갱신합니다. 두 번째 스크립트는 공식 사이트의 국내 선물·옵션 TR 목록과 상세 페이지 링크를 다시 수집해 인덱스를 갱신합니다.

## 2차 MVP — 백테스터

백테스터는 2차 MVP 범위입니다. 국내 파생상품 명세와 공식 조회 예제를 먼저 파악한 뒤 과거 데이터 수집·정규화와 백테스트 엔진을 설계합니다. 이 저장소는 LS증권과 무관한 비공식 개인 프로젝트입니다.
