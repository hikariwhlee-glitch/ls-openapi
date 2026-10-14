"""사용자가 명시적으로 활성화한 모의투자 주문 요청 테스트.

환경변수 두 개가 모두 설정된 때만 주문을 전송합니다:
LS_LIVE_TEST=1, LS_LIVE_ORDER_TEST=1.
이 테스트는 tests/live에서 일반적으로 실행될 때 건너뛰며, 실제 주문 재시도는 없습니다.
"""
import os

import pytest

from ls_openapi import LSClient, Settings, TokenManager, submit_futures_option_order

pytestmark = pytest.mark.skipif(
    os.environ.get("LS_LIVE_TEST") != "1"
    or os.environ.get("LS_LIVE_ORDER_TEST") != "1",
    reason="모의투자 주문 테스트는 수동 실행에서 두 플래그를 명시해야 합니다",
)


def test_submit_sample_simulated_order():
    """저장소 소유자가 제시한 샘플 주문을 한 번만 모의투자 서버로 전송합니다."""
    settings = Settings.from_env()
    client = LSClient(settings, token_manager=TokenManager(settings))

    # 사용자가 제시한 샘플 그대로: 101T9000 / BnsTpCode 2 / 지정가 342.25 / 수량 5.
    response = submit_futures_option_order(
        client,
        instrument_code="101T9000",
        side_code="2",
        price_type_code="00",
        order_price=342.25,
        quantity=5,
    )

    body = response.body if isinstance(response.body, dict) else {}
    response_code = body.get("rsp_cd")
    response_message = body.get("rsp_msg")
    print("[주문] base_url :", settings.base_url)
    print("[주문] tr_cd    :", response.tr_cd)
    print("[주문] rsp_cd   :", response_code)
    if response_message is not None:
        print("[주문] rsp_msg  :", str(response_message)[:120])
    for block_name, block in sorted(body.items()):
        if isinstance(block, dict):
            print("[주문] {} fields: {}".format(block_name, sorted(block)))

    assert response.tr_cd == "CFOAT00100"
    assert response_code == "00000", (
        "주문 응답 성공 여부를 확인할 수 없습니다. 응답 코드={!r}".format(response_code)
    )
