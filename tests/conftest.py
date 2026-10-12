"""테스트 공용 도구. 실제 서버나 계정 없이 동작하는 가짜 HTTP 응답/세션."""

import json

import pytest

from ls_openapi import Settings

FAKE_APP_KEY = "test-app-key-0000"
FAKE_APP_SECRET = "test-app-secret-1111"
FAKE_TOKEN = "test-access-token-2222"


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=None, headers=None):
        self.status_code = status_code
        self._payload = payload
        if text is None:
            text = json.dumps(payload) if payload is not None else ""
        self.text = text
        self.headers = headers or {}

    def json(self):
        if self._payload is None:
            raise ValueError("JSON 이 아닙니다")
        return self._payload


class FakeSession:
    """미리 정해 둔 응답을 순서대로 돌려주고, 받은 요청을 기록합니다."""

    def __init__(self, *responses):
        self._queue = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append(dict(url=url, **kwargs))
        if not self._queue:
            raise AssertionError("준비된 가짜 응답이 없습니다")
        item = self._queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


@pytest.fixture
def settings():
    return Settings(
        app_key=FAKE_APP_KEY,
        app_secret=FAKE_APP_SECRET,
        base_url="https://example.invalid:8080",
    )


@pytest.fixture
def token_payload():
    return {
        "access_token": FAKE_TOKEN,
        "token_type": "Bearer",
        "expires_in": 86400,
        "scope": "oob",
    }
