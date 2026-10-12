import pytest
import requests

from ls_openapi import AuthError, TokenManager, issue_token, revoke_token
from tests.conftest import FAKE_APP_KEY, FAKE_APP_SECRET, FAKE_TOKEN, FakeResponse, FakeSession


def test_issue_token_sends_documented_request(settings, token_payload):
    session = FakeSession(FakeResponse(payload=token_payload))

    token = issue_token(settings, session=session, timeout=5, clock=lambda: 1000.0)

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/oauth2/token"
    assert call["data"] == {
        "grant_type": "client_credentials",
        "appkey": FAKE_APP_KEY,
        "appsecretkey": FAKE_APP_SECRET,
        "scope": "oob",
    }
    assert call["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
    assert call["timeout"] == 5
    assert token.access_token == FAKE_TOKEN
    assert token.token_type == "Bearer"
    assert token.expires_in == 86400
    assert token.expires_at == 1000.0 + 86400
    assert token.authorization_header == "Bearer " + FAKE_TOKEN


@pytest.mark.parametrize("field", ["expires_in", "expire_in"])
def test_both_documented_expiry_field_names_are_accepted(settings, field):
    payload = {"access_token": FAKE_TOKEN, "token_type": "Bearer", field: "3600"}
    token = issue_token(settings, session=FakeSession(FakeResponse(payload=payload)))
    assert token.expires_in == 3600


def test_missing_expiry_is_none_and_never_considered_expired(settings):
    payload = {"access_token": FAKE_TOKEN, "token_type": "Bearer"}
    token = issue_token(settings, session=FakeSession(FakeResponse(payload=payload)))
    assert token.expires_in is None
    assert token.is_expired(now=10**12) is False


def test_missing_access_token_raises(settings):
    session = FakeSession(FakeResponse(payload={"token_type": "Bearer"}))
    with pytest.raises(AuthError):
        issue_token(settings, session=session)


def test_http_error_raises_and_redacts_credentials(settings):
    body = "invalid appkey={} secret={}".format(FAKE_APP_KEY, FAKE_APP_SECRET)
    session = FakeSession(FakeResponse(status_code=401, text=body))
    with pytest.raises(AuthError) as info:
        issue_token(settings, session=session)
    message = str(info.value)
    assert "401" in message
    assert FAKE_APP_KEY not in message
    assert FAKE_APP_SECRET not in message


def test_network_error_raises_auth_error(settings):
    session = FakeSession(requests.ConnectionError("boom"))
    with pytest.raises(AuthError) as info:
        issue_token(settings, session=session)
    assert "ConnectionError" in str(info.value)


def test_non_json_response_raises(settings):
    session = FakeSession(FakeResponse(status_code=200, text="<html>"))
    with pytest.raises(AuthError):
        issue_token(settings, session=session)


def test_token_repr_does_not_leak_token_value(settings, token_payload):
    token = issue_token(settings, session=FakeSession(FakeResponse(payload=token_payload)))
    assert FAKE_TOKEN not in repr(token)


def test_token_manager_reuses_token_until_near_expiry(settings, token_payload):
    now = [1000.0]
    session = FakeSession(
        FakeResponse(payload=token_payload),
        FakeResponse(payload=dict(token_payload, access_token="second-token")),
    )
    manager = TokenManager(settings, session=session, refresh_margin=60, clock=lambda: now[0])

    assert manager.get_token().access_token == FAKE_TOKEN
    now[0] = 1000.0 + 86400 - 61  # 만료 61초 전: 재사용
    assert manager.get_token().access_token == FAKE_TOKEN
    assert len(session.calls) == 1

    now[0] = 1000.0 + 86400 - 59  # 만료 59초 전: 새로 발급
    assert manager.get_token().access_token == "second-token"
    assert len(session.calls) == 2


def test_token_manager_invalidate_forces_new_token(settings, token_payload):
    session = FakeSession(
        FakeResponse(payload=token_payload),
        FakeResponse(payload=token_payload),
    )
    manager = TokenManager(settings, session=session)
    manager.get_token()
    manager.invalidate()
    manager.get_token()
    assert len(session.calls) == 2


def test_revoke_token_sends_documented_request(settings):
    session = FakeSession(FakeResponse(payload={"code": "200", "message": "ok"}))

    result = revoke_token(settings, FAKE_TOKEN, session=session)

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/oauth2/revoke"
    assert call["data"] == {
        "appkey": FAKE_APP_KEY,
        "appsecretkey": FAKE_APP_SECRET,
        "token_type_hint": "access_token",
        "token": FAKE_TOKEN,
    }
    assert result == {"code": "200", "message": "ok"}


def test_revoke_http_error_redacts_token(settings):
    session = FakeSession(FakeResponse(status_code=400, text="bad token " + FAKE_TOKEN))
    with pytest.raises(AuthError) as info:
        revoke_token(settings, FAKE_TOKEN, session=session)
    assert FAKE_TOKEN not in str(info.value)


def test_token_manager_revoke_clears_cached_token(settings, token_payload):
    session = FakeSession(
        FakeResponse(payload=token_payload),
        FakeResponse(payload={"code": "200", "message": "ok"}),
        FakeResponse(payload=token_payload),
    )
    manager = TokenManager(settings, session=session)
    assert manager.revoke() is None  # 발급 전에는 할 일이 없다
    manager.get_token()
    assert manager.revoke() == {"code": "200", "message": "ok"}
    manager.get_token()
    assert len(session.calls) == 3
