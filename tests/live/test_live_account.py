"""실서버 테스트: 토큰 발급 → 계좌잔고(CFOAQ50600) 조회 → 토큰 폐기.

``LS_LIVE_TEST=1`` 일 때만 실행합니다. 저장소가 공개라 Actions 로그도 공개되므로
계좌·잔고 값은 출력하지 않고 응답코드, 메시지, 블록/필드 이름만 출력합니다.
"""

import os
from datetime import date

import pytest

from ls_openapi import LSClient, Settings, TokenManager, fetch_account_balance

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1",
    reason="실서버 테스트는 LS_LIVE_TEST=1 일 때만 실행됩니다",
)


def test_live_account_balance():
    settings = Settings.from_env()
    manager = TokenManager(settings)
    client = LSClient(settings, token_manager=manager)
    try:
        response = fetch_account_balance(client, date.today().strftime("%Y%m%d"))
    finally:
        manager.revoke()

    body = response.body if isinstance(response.body, dict) else {}
    print("[응답코드] {} / {}".format(body.get("rsp_cd"), body.get("rsp_msg")))
    for name in sorted(body):
        value = body[name]
        if isinstance(value, dict):
            print("[블록] {}: 필드 {}".format(name, ", ".join(sorted(value))))
        elif isinstance(value, list):
            print("[블록] {}: {}행".format(name, len(value)))
    assert isinstance(response.body, dict)
    assert body.get("rsp_cd") is not None
