"""실서버 모의투자 계좌에서 CFOAQ50600 잔고 TR만 조회합니다.

요청 날짜와 코드값은 사용자가 제공한 샘플 그대로 사용합니다.
응답 본문에는 계좌 및 잔고 정보가 포함될 수 있어 값을 출력하지 않습니다.
"""

import os

import pytest

from ls_openapi import APIError, AuthError, LSClient, Settings, TokenManager, fetch_futures_option_balance

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1"
    or os.environ.get("LS_BALANCE_LIVE_TEST") != "1",
    reason="잔고 실서버 조회는 수동 Actions의 balance 범위에서만 실행됩니다",
)


def test_cfoaq50600_balance_inquiry():
    settings = Settings.from_env()
    manager = TokenManager(settings)
    client = LSClient(settings, token_manager=manager)

    try:
        # 제공된 샘플 요청의 입력값을 그대로 재현합니다.
        response = fetch_futures_option_balance(client, order_date="20240626")
        body = response.body if isinstance(response.body, dict) else {}
        response_code = body.get("rsp_cd")
        print("[잔고 조회] TR:", response.tr_cd)
        print("[잔고 조회] OrdDt: 20240626")
        print("[잔고 조회] 응답코드:", response_code)
        print("[잔고 조회] 최상위 필드명:", sorted(body))
        assert response.tr_cd == "CFOAQ50600", "응답 TR 코드가 요청과 다릅니다."
        assert response_code == "00000", "잔고 조회 성공 응답 코드가 아닙니다."
    except APIError as exc:
        # 예외 메시지에는 서버 응답이 포함될 수 있어 출력하지 않습니다.
        pytest.fail("CFOAQ50600 호출 실패 ({})".format(type(exc).__name__))
    finally:
        try:
            manager.revoke()
            print("[토큰 폐기] 완료")
        except AuthError as exc:
            print("[토큰 폐기] 실패 ({})".format(type(exc).__name__))
