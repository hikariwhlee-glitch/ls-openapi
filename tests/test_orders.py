import pytest

from ls_openapi import LSClient, submit_futures_option_order
from ls_openapi.auth import AccessToken
from tests.conftest import FAKE_TOKEN, FakeResponse, FakeSession


class StubTokenManager:
    def get_token(self):
        return AccessToken(access_token=FAKE_TOKEN, token_type="Bearer", expires_in=86400)


def make_client(settings, *responses):
    session = FakeSession(*responses)
    return LSClient(settings, token_manager=StubTokenManager(), session=session), session


def test_submit_futures_option_order_sends_sample_shape(settings):
    payload = {"rsp_cd": "00000", "CFOAT00100OutBlock1": {"dummy": "accepted"}}
    client, session = make_client(settings, FakeResponse(payload=payload))

    result = submit_futures_option_order(
        client,
        "101T9000",
        "2",
        "00",
        342.25,
        5,
    )

    call = session.calls[0]
    assert call["url"] == "https://example.invalid:8080/futureoption/order"
    assert call["json"] == {
        "CFOAT00100InBlock1": {
            "FnoIsuNo": "101T9000",
            "BnsTpCode": "2",
            "FnoOrdprcPtnCode": "00",
            "FnoOrdPrc": 342.25,
            "OrdQty": 5,
        }
    }
    assert call["headers"]["tr_cd"] == "CFOAT00100"
    assert call["headers"]["authorization"] == "Bearer " + FAKE_TOKEN
    assert call["headers"]["tr_cont"] == "N"
    assert call["headers"]["tr_cont_key"] == ""
    assert "mac_address" not in call["headers"]
    assert result.tr_cd == "CFOAT00100"
    assert result.body == payload


def test_order_fields_are_trimmed_and_mac_address_is_passed(settings):
    client, session = make_client(settings, FakeResponse(payload={}))

    submit_futures_option_order(
        client,
        "  101T9000 ",
        " 2 ",
        " 00 ",
        342.25,
        5,
        mac_address="AABBCCDDEEFF",
    )

    call = session.calls[0]
    assert call["json"]["CFOAT00100InBlock1"] == {
        "FnoIsuNo": "101T9000",
        "BnsTpCode": "2",
        "FnoOrdprcPtnCode": "00",
        "FnoOrdPrc": 342.25,
        "OrdQty": 5,
    }
    assert call["headers"]["mac_address"] == "AABBCCDDEEFF"


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_invalid_order_quantity_is_rejected_before_request(settings, quantity):
    client, session = make_client(settings)

    with pytest.raises(ValueError):
        submit_futures_option_order(client, "101T9000", "2", "00", 342.25, quantity)

    assert session.calls == []


@pytest.mark.parametrize("price", [-1, float("nan"), float("inf"), True, "342.25"])
def test_invalid_order_price_is_rejected_before_request(settings, price):
    client, session = make_client(settings)

    with pytest.raises(ValueError):
        submit_futures_option_order(client, "101T9000", "2", "00", price, 5)

    assert session.calls == []


@pytest.mark.parametrize(
    "instrument_code,side_code,price_type_code",
    [
        ("", "2", "00"),
        ("101T9000", "", "00"),
        ("101T9000", "2", ""),
    ],
)
def test_required_order_codes_are_rejected_before_request(
    settings, instrument_code, side_code, price_type_code
):
    client, session = make_client(settings)

    with pytest.raises(ValueError):
        submit_futures_option_order(
            client, instrument_code, side_code, price_type_code, 342.25, 5
        )

    assert session.calls == []
