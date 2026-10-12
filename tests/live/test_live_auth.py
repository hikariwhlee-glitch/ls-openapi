"""실서버 테스트: 접근토큰 발급 → 폐기.

기본 ``pytest`` 에서는 건너뜁니다. 실제 앱키/시크릿키가 필요하며 다음처럼 실행합니다.

    LS_LIVE_TEST=1 pytest -s tests/live          # macOS/Linux
    $env:LS_LIVE_TEST="1"; pytest -s tests/live  # Windows PowerShell

앱키/시크릿키는 ``.env`` 또는 환경변수(LS_APP_KEY, LS_APP_SECRET)로 설정합니다.
화면에는 토큰 값, 앱키, 시크릿키를 출력하지 않습니다. 대신 실서버가 돌려준
응답 필드의 **이름**과 유효기간, 폐기 응답의 code/message 만 출력합니다.
(공식 자료끼리 어긋나는 항목과 폐기 성공 코드를 실서버로 확인하기 위함입니다.)
"""

import os

import pytest
import requests

from ls_openapi import Settings, issue_token, revoke_token

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1",
    reason="실서버 테스트는 LS_LIVE_TEST=1 일 때만 실행됩니다",
)


class _RecordingSession:
    """requests 로 그대로 호출하면서 응답 JSON 을 기억합니다."""

    def __init__(self):
        self.last_payload = None

    def post(self, url, **kwargs):
        response = requests.post(url, **kwargs)
        try:
            self.last_payload = response.json()
        except ValueError:
            self.last_payload = None
        return response


def _field_names(payload):
    return sorted(payload) if isinstance(payload, dict) else None


def _scrub(text, *secrets):
    text = str(text)
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text[:100]


def test_issue_then_revoke_token():
    settings = Settings.from_env()

    issue_session = _RecordingSession()
    token = issue_token(settings, session=issue_session)
    try:
        assert token.access_token
        print("\n[발급] base_url      :", settings.base_url)
        print("[발급] 응답 필드명  :", _field_names(issue_session.last_payload))
        print("[발급] token_type   :", token.token_type)
        print("[발급] expires_in   :", token.expires_in)
        print("[발급] scope        :", token.scope)
    finally:
        revoke_session = _RecordingSession()
        result = revoke_token(settings, token.access_token, session=revoke_session)
        print("[폐기] 응답 필드명  :", _field_names(revoke_session.last_payload))
        print(
            "[폐기] code/message :",
            _scrub(result.get("code"), settings.app_key, settings.app_secret, token.access_token),
            "/",
            _scrub(result.get("message"), settings.app_key, settings.app_secret, token.access_token),
        )

    assert isinstance(result, dict)
