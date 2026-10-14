"""실서버 테스트: 토큰 발급 → 선물/옵션 현재가(t2111) 조회 → 토큰 폐기.

기본 ``pytest`` 에서는 건너뜁니다. 다음 두 가지가 모두 필요합니다.

    LS_LIVE_TEST=1                          실서버 테스트 허용
    LS_FOCODE=<8자리>[,<8자리>...]             조회할 선물/옵션 종목코드

    LS_LIVE_TEST=1 LS_FOCODE=A016C000 pytest -s tests/live/test_live_futures.py

``LS_FOCODE`` 에 쉼표로 여러 코드를 넣으면 토큰 하나로 차례로 조회합니다.
현재 상장된 4개월물 등 확인할 코드를 GitHub Actions의 `LS_FOCODE` 변수에 쉼표로 등록할 수 있습니다.
각 응답에서 `rsp_cd=00000`이고 OutBlock의 `focode`가 요청 코드와 일치해야 그 종목을 성공으로 셉니다.
등록한 코드가 하나라도 조회되지 않으면 테스트가 실패합니다.

앱키/시크릿키는 ``.env`` 또는 환경변수(LS_APP_KEY, LS_APP_SECRET)로 설정합니다.
화면에는 앱키, 시크릿키, 토큰 값을 출력하지 않습니다. 응답 구조(블록 이름, 필드 이름)와
값을 출력해, 공식 명세에 없는 응답 형식을 확인하는 데 씁니다. 값은 공개 시세 데이터입니다.
"""

import os
import time

import pytest

from ls_openapi import APIError, AuthError, LSClient, Settings, TokenManager, fetch_current_price

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1",
    reason="실서버 테스트는 LS_LIVE_TEST=1 일 때만 실행됩니다",
)

# TR별 초당 호출 제한이 확인되지 않아, 연속 조회 사이에 여유를 둡니다.
_PAUSE_BETWEEN_CALLS = 1.1


def _focodes():
    raw = os.environ.get("LS_FOCODE", "")
    return [code.strip() for code in raw.split(",") if code.strip()]


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
    focodes = _focodes()
    if not focodes:
        pytest.skip("LS_FOCODE(조회할 선물/옵션 종목코드)가 설정되지 않았습니다")

    settings = Settings.from_env()
    manager = TokenManager(settings)
    client = LSClient(settings, token_manager=manager)

    succeeded = []
    failed = []
    try:
        for index, focode in enumerate(focodes):
            if index:
                time.sleep(_PAUSE_BETWEEN_CALLS)
            print("\n[조회] base_url     :", settings.base_url)
            print("[조회] focode       :", focode)
            try:
                response = fetch_current_price(client, focode)
            except APIError as exc:
                failed.append(focode)
                print("[조회] 실패         :", exc)
                continue
            body = response.body
            out_block = body.get("t2111OutBlock") if isinstance(body, dict) else None
            response_code = body.get("rsp_cd") if isinstance(body, dict) else None
            returned_focode = out_block.get("focode") if isinstance(out_block, dict) else None
            if response_code != "00000" or returned_focode != focode:
                failed.append(focode)
                print(
                    "[조회] 실패         : 응답 코드/종목 불일치 "
                    "(rsp_cd={!r}, focode={!r})".format(response_code, returned_focode)
                )
                _print_structure(body if isinstance(body, dict) else {"body": body})
                continue
            succeeded.append(focode)
            print("[조회] 응답 tr_cd   :", response.tr_cd)
            print(
                "[조회] tr_cont      :",
                response.tr_cont,
                "/ tr_cont_key:",
                response.tr_cont_key or "(없음)",
            )
            _print_structure(response.body)
    finally:
        try:
            result = manager.revoke()
            print(
                "\n[폐기] code/message :",
                (result or {}).get("code"),
                "/",
                (result or {}).get("message"),
            )
        except AuthError as exc:
            print("\n[폐기] 실패:", exc)

    print("[요약] 성공:", succeeded or "(없음)", "/ 실패:", failed or "(없음)")
    assert not failed and len(succeeded) == len(focodes), (
        "요청한 모든 종목코드의 유효한 응답이 필요합니다 "
        "(성공: {}, 실패: {})".format(succeeded, failed)
    )
