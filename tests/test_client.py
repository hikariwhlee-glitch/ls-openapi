import pytest
import requests

from ls_openapi import APIError, LSClient, build_in_block
from ls_openapi.auth import AccessToken
from tests.conftest import FAKE_APP_KEY, FAKE_TOKEN, FakeResponse, FakeSession


class StubTokenManager:
    def get_token(self):
        return AccessToken(access_token=FAKE_TOKEN, token_type="Bearer", expires_in=86400)


def make_client(settings, *responses):
    session = FakeSession(*responses)
    return LSClient(settings, token_manager=StubTokenManager(), session=session), session


def test_build_in_block_wraps_fields_under_tr_name():
    assert build_in_block("t0000", {"a": "1"}) == {"t0000InBlock": {"a": "1"}}


def test_post_tr_sends_common_headers_and_body(settings):
    client, session = make_client(
        settings, FakeResponse(payload={"t0000OutBlock": {"x": 1}})
    )
    body = build_in_block("t0000", {"a": "1"})

    result = client.post_tr("/dummy/path", "t0000", body)

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/dummy/path"
    assert call["json"] == body
    assert call["headers"] == {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + FAKE_TOKEN,
        "tr_cd": "t0000",
        "tr_cont": "N",
        "tr_cont_key": "",
    }
    assert result.tr_cd == "t0000"
    assert result.body == {"t0000OutBlock": {"x": 1}}
    assert result.tr_cont == "N"
    assert result.tr_cont_key == ""


def test_post_tr_passes_continuation_values_and_reads_response_headers(settings):
    client, session = make_client(
        settings,
        FakeResponse(payload={}, headers={"tr_cont": "Y", "tr_cont_key": "KEY123"}),
    )

    result = client.post_tr(
        "/dummy/path", "t0000", {}, tr_cont="Y", tr_cont_key="PREV", mac_address="AABBCCDDEEFF"
    )

    headers = session.calls[0]["headers"]
    assert headers["tr_cont"] == "Y"
    assert headers["tr_cont_key"] == "PREV"
    assert headers["mac_address"] == "AABBCCDDEEFF"
    assert result.tr_cont == "Y"
    assert result.tr_cont_key == "KEY123"


def test_http_error_raises_api_error_with_status_and_redacts_secrets(settings):
    text = "denied {} {}".format(FAKE_TOKEN, FAKE_APP_KEY)
    client, _ = make_client(settings, FakeResponse(status_code=403, text=text))

    with pytest.raises(APIError) as info:
        client.post_tr("/dummy/path", "t0000", {})

    assert info.value.status_code == 403
    assert FAKE_TOKEN not in str(info.value)
    assert FAKE_APP_KEY not in str(info.value)


def test_network_error_raises_api_error(settings):
    client, _ = make_client(settings, requests.Timeout("slow"))
    with pytest.raises(APIError) as info:
        client.post_tr("/dummy/path", "t0000", {})
    assert "Timeout" in str(info.value)


def test_non_json_response_raises_api_error(settings):
    client, _ = make_client(settings, FakeResponse(status_code=200, text="not json"))
    with pytest.raises(APIError):
        client.post_tr("/dummy/path", "t0000", {})
