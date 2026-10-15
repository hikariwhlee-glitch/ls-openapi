# ls-openapi

LS증권 국내 선물·옵션 Open API를 활용하기 위한 비공식 개발 자료 모음입니다.

## 1차 MVP — 공식 예제와 명세 바로가기

LS증권 공식 API 서비스는 국내 선물·옵션의 TR 명세와 Python·Java·JavaScript 코드 샘플을 제공합니다. 이 저장소는 91개 TR을 카테고리별로 정리하고, 각 TR의 공식 가이드 그룹과 언어별 샘플이 담긴 상세 JSON을 바로 열 수 있게 인덱싱합니다. 요청·응답 필드 명세도 함께 보관합니다.

- [국내 선물·옵션 TR별 공식 샘플 인덱스](docs/official-samples.md)
- [공식 명세 JSON 스냅샷](specs/domestic-futures-options.json)
- [사람이 읽는 전체 명세](docs/domestic-futures-options.md)
- [LS증권 API 서비스](https://openapi.ls-sec.co.kr/apiservice)

샘플 JSON 링크의 `codeSamples`에서 해당 TR의 언어별 예제를 확인할 수 있습니다. 이 저장소는 공식 코드 샘플 원문을 대량 복제하지 않고, 출처가 명확한 링크와 검색용 인덱스를 제공합니다.

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
