import pytest

from ls_openapi import APIError, LSClient, fetch_account_balance
from ls_openapi.auth import AccessToken
from tests.conftest import FAKE_TOKEN, FakeResponse, FakeSession


class StubTokenManager:
    def get_token(self):
        return AccessToken(access_token=FAKE_TOKEN, token_type="Bearer", expires_in=86400)


def make_client(settings, *responses):
    session = FakeSession(*responses)
    return LSClient(settings, token_manager=StubTokenManager(), session=session), session


def test_fetch_account_balance_sends_sample_shape(settings):
    payload = {"rsp_cd": "00000", "CFOAQ50600OutBlock1": {"dummy": "x"}}
    client, session = make_client(settings, FakeResponse(payload=payload))

    result = fetch_account_balance(client, "20240626")

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/futureoption/accno"
    assert call["json"] == {
        "CFOAQ50600InBlock1": {
            "RecCnt": 1,
            "OrdDt": "20240626",
            "BalEvalTp": "1",
            "FutsPrcEvalTp": "1",
            "LqtQtyQryTp": "1",
        }
    }
    assert call["headers"]["tr_cd"] == "CFOAQ50600"
    assert call["headers"]["authorization"] == "Bearer " + FAKE_TOKEN
    assert call["headers"]["tr_cont"] == "N"
    assert "mac_address" not in call["headers"]
    assert result.tr_cd == "CFOAQ50600"
    assert result.body == payload


def test_options_are_passed_and_trimmed(settings):
    client, session = make_client(settings, FakeResponse(payload={}))

    fetch_account_balance(
        client,
        " 20240626 ",
        balance_eval_type="2",
        futures_price_eval_type="3",
        liquidation_qty_query_type="4",
        mac_address="AABBCCDDEEFF",
    )

    call = session.calls[0]
    block = call["json"]["CFOAQ50600InBlock1"]
    assert block["OrdDt"] == "20240626"
    assert (block["BalEvalTp"], block["FutsPrcEvalTp"], block["LqtQtyQryTp"]) == ("2", "3", "4")
    assert call["headers"]["mac_address"] == "AABBCCDDEEFF"


@pytest.mark.parametrize("bad", ["", "  ", None, 20240626, "2024-06-26", "2024062", "abcdefgh"])
def test_bad_date_is_rejected_before_any_request(settings, bad):
    client, session = make_client(settings)
    with pytest.raises(ValueError):
        fetch_account_balance(client, bad)
    assert session.calls == []


def test_empty_type_code_is_rejected(settings):
    client, session = make_client(settings)
    with pytest.raises(ValueError):
        fetch_account_balance(client, "20240626", balance_eval_type=" ")
    assert session.calls == []


def test_http_error_propagates_as_api_error(settings):
    client, _ = make_client(settings, FakeResponse(status_code=500, text="server error"))
    with pytest.raises(APIError) as info:
        fetch_account_balance(client, "20240626")
    assert info.value.status_code == 500
    assert "CFOAQ50600" in str(info.value)
