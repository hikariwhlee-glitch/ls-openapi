"""예제 3: 선물/옵션 정상주문(CFOAT00100).

실행 (저장소 루트에서):
  python examples/domestic_futureoption/03_futures_option_order.py <종목코드> <매매코드> <호가유형코드> <주문가격> <수량>

예:
  python examples/domestic_futureoption/03_futures_option_order.py A0173000 2 00 947.10 1

주문가격과 수량을 사용자가 직접 지정합니다. 시세 조회, 틱 계산, 주문 결정은
이 예제나 submit_futures_option_order 함수가 대신하지 않습니다.
호출하면 연결된 계좌로 즉시 주문이 제출됩니다. 모의투자 계좌로 먼저 확인하세요.
응답의 원문에는 계좌 관련 필드가 있을 수 있어 전체 응답을 출력하지 않습니다.
"""

import sys
from pathlib import Path

# pip install -e . 없이도 실행되도록 src 폴더를 경로에 추가합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ls_openapi import (  # noqa: E402
    APIError,
    AuthError,
    ConfigError,
    LSClient,
    Settings,
    TokenManager,
    submit_futures_option_order,
)


def main(argv) -> int:
    if len(argv) != 6:
        print(
            "사용법: python examples/domestic_futureoption/03_futures_option_order.py "
            "<종목코드> <매매코드> <호가유형코드> <주문가격> <수량>"
        )
        return 2

    instrument_code, side_code, price_type_code, raw_price, raw_quantity = argv[1:]
    try:
        order_price = float(raw_price)
        quantity = int(raw_quantity)
    except ValueError:
        print("실패: 주문가격은 숫자, 수량은 정수여야 합니다.")
        return 2

    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = submit_futures_option_order(
            client,
            instrument_code=instrument_code,
            side_code=side_code,
            price_type_code=price_type_code,
            order_price=order_price,
            quantity=quantity,
        )
    except (ConfigError, AuthError, APIError, ValueError) as exc:
        print("실패: {}".format(exc))
        return 1
    finally:
        if manager is not None:
            try:
                manager.revoke()
            except AuthError as exc:
                print("참고: 토큰 폐기에 실패했습니다 ({})".format(exc))

    body = response.body if isinstance(response.body, dict) else {}
    print("TR: {}".format(response.tr_cd))
    print("응답코드: {}".format(body.get("rsp_cd", "(없음)")))
    print("응답메시지: {}".format(body.get("rsp_msg", "(없음)")))
    print("응답 필드명: {}".format(", ".join(sorted(body)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
