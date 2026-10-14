# 선물/옵션 잔고 조회

선물/옵션 계좌 잔고 및 평가 현황은 TR `CFOAQ50600`으로 조회합니다.

## Python API

~~~python
from ls_openapi import LSClient, Settings, TokenManager, fetch_futures_option_balance

settings = Settings.from_env()
manager = TokenManager(settings)
client = LSClient(settings, token_manager=manager)

try:
    response = fetch_futures_option_balance(client, order_date="20240626")
    # 계좌정보를 포함할 수 있으므로 전체 응답을 로그에 출력하지 마세요.
    print(response.body.get("rsp_cd"), response.body.get("rsp_msg"))
finally:
    manager.revoke()
~~~

이 함수는 조회 TR만 호출하며 주문을 제출하지 않습니다. 응답 원문은 `TRResponse.body`에 보관되므로 계좌번호, 잔고, 평가금액 등 민감한 값을 출력하거나 로그에 남길 때 주의하세요.

## 요청 필드와 확인 상태

- 경로: `POST /futureoption/accno`
- TR 코드: `CFOAQ50600` — 공식 포털 API 목록의 명칭은 “선물옵션 계좌잔고 및 평가현황3”입니다.
- 입력 블록: `CFOAQ50600InBlock1`
- 입력 필드: `RecCnt`, `OrdDt`, `BalEvalTp`, `FutsPrcEvalTp`, `LqtQtyQryTp`

엔드포인트와 필드명, 예시 기본 코드값(`1`)은 사용자가 제공한 호출 샘플을 기준으로 구현했습니다. 공식 포털에서 TR 코드와 이름은 확인했지만, 상세 요청 스키마와 코드값 의미는 별도로 대조하지 못했습니다. 실제 계좌로 조회하거나 모의투자 실서버에서 검증하지 않았습니다.

`order_date`는 유효한 `YYYYMMDD` 문자열이어야 합니다. 평가 구분값은 필요에 따라 문자열 인자로 전달할 수 있습니다. 기본값은 제공된 샘플의 값을 사용합니다.

## 독립 실행 예제

모의투자 앱키를 환경변수 또는 `.env`에 설정한 뒤 저장소 루트에서 실행합니다.

~~~bash
python examples/domestic_futureoption/04_futures_option_balance.py 20240626
~~~

예제는 응답코드, 메시지, 최상위 필드명만 출력하고 계좌 잔고 데이터는 출력하지 않습니다.
