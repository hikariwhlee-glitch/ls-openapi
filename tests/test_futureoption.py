import pytest
import requests

from ls_openapi import APIError, LSClient, fetch_current_price
from ls_openapi.auth import AccessToken
from tests.conftest import FAKE_TOKEN, FakeResponse, FakeSession


class StubTokenManager:
    def get_token(self):
        return AccessToken(access_token=FAKE_TOKEN, token_type="Bearer", expires_in=86400)


def make_client(settings, *responses):
    session = FakeSession(*responses)
    return LSClient(settings, token_manager=StubTokenManager(), session=session), session


def test_fetch_current_price_sends_t2111_request_from_sample(settings):
    # 응답 필드 이름은 공식 명세로 확인되지 않아, 구조와 무관한 가짜 값만 사용합니다.
    payload = {"t2111OutBlock": {"dummy_field": "dummy_value"}}
    client, session = make_client(settings, FakeResponse(payload=payload))

    result = fetch_current_price(client, "A0000000")

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/futureoption/market-data"
    assert call["json"] == {"t2111InBlock": {"focode": "A0000000"}}
    assert call["headers"]["tr_cd"] == "t2111"
    assert call["headers"]["authorization"] == "Bearer " + FAKE_TOKEN
    assert call["headers"]["tr_cont"] == "N"
    assert call["headers"]["tr_cont_key"] == ""
    assert "mac_address" not in call["headers"]  # 법인만 필수
    assert result.tr_cd == "t2111"
    assert result.body == payload  # 해석하지 않고 그대로 전달


def test_focode_is_stripped_and_mac_address_is_passed_through(settings):
    client, session = make_client(settings, FakeResponse(payload={}))

    fetch_current_price(client, "  A0000000 ", mac_address="AABBCCDDEEFF")

    call = session.calls[0]
    assert call["json"] == {"t2111InBlock": {"focode": "A0000000"}}
    assert call["headers"]["mac_address"] == "AABBCCDDEEFF"


@pytest.mark.parametrize("bad", ["", "   ", None, 123])
def test_empty_or_non_string_focode_is_rejected_before_any_request(settings, bad):
    client, session = make_client(settings)
    with pytest.raises(ValueError):
        fetch_current_price(client, bad)
    assert session.calls == []


def test_http_error_propagates_as_api_error(settings):
    client, _ = make_client(settings, FakeResponse(status_code=500, text="server error"))
    with pytest.raises(APIError) as info:
        fetch_current_price(client, "A0000000")
    assert info.value.status_code == 500
    assert "t2111" in str(info.value)


def test_network_error_propagates_as_api_error(settings):
    client, _ = make_client(settings, requests.Timeout("slow"))
    with pytest.raises(APIError):
        fetch_current_price(client, "A0000000")
