"""실서버 테스트: 토큰 발급 → 선물/옵션 현재가(t2111) 조회 → 토큰 폐기.

기본 ``pytest`` 에서는 건너뜁니다. 다음 두 가지가 모두 필요합니다.

    LS_LIVE_TEST=1                  실서버 테스트 허용
    LS_FOCODE=<선물/옵션 종목코드>   조회할 종목코드 (없으면 이 테스트만 건너뜀)

    LS_LIVE_TEST=1 LS_FOCODE=... pytest -s tests/live/test_live_futures.py

앱키/시크릿키는 ``.env`` 또는 환경변수(LS_APP_KEY, LS_APP_SECRET)로 설정합니다.
화면에는 앱키, 시크릿키, 토큰 값을 출력하지 않습니다. 응답 구조(블록 이름, 필드 이름)와
값을 출력해, 공식 명세에 없는 응답 형식을 확인하는 데 씁니다. 값은 공개 시세 데이터입니다.
"""

import os

import pytest

from ls_openapi import AuthError, LSClient, Settings, TokenManager, fetch_current_price

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1",
    reason="실서버 테스트는 LS_LIVE_TEST=1 일 때만 실행됩니다",
)


def _short(value, limit=40):
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _print_structure(body):
    print("[응답] 최상위 키     :", sorted(body))
    for name in sorted(body):
        value = body[name]
        if isinstance(value, dict):
            print("[응답] {} (객체)".format(name))
            for key in sorted(value):
                print("         {} = {}".format(key, _short(value[key])))
        elif isinstance(value, list):
            print("[응답] {} (배열 {}건)".format(name, len(value)))
            if value and isinstance(value[0], dict):
                print("         첫 항목 키:", sorted(value[0]))
        else:
            print("[응답] {} = {}".format(name, _short(value)))


def test_t2111_current_price_between_issue_and_revoke():
    focode = os.environ.get("LS_FOCODE", "").strip()
    if not focode:
        pytest.skip("LS_FOCODE(조회할 선물/옵션 종목코드)가 설정되지 않았습니다")

    settings = Settings.from_env()
    manager = TokenManager(settings)
    client = LSClient(settings, token_manager=manager)

    try:
        response = fetch_current_price(client, focode)
        print("\n[조회] base_url     :", settings.base_url)
        print("[조회] focode       :", focode)
        print("[조회] 응답 tr_cd   :", response.tr_cd)
        print("[조회] tr_cont      :", response.tr_cont, "/ tr_cont_key:", response.tr_cont_key or "(없음)")
        _print_structure(response.body)
    finally:
        try:
            result = manager.revoke()
            print("[폐기] code/message :", (result or {}).get("code"), "/", (result or {}).get("message"))
        except AuthError as exc:
            print("[폐기] 실패:", exc)

    assert isinstance(response.body, dict)
