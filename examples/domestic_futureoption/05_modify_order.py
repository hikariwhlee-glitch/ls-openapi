"""예제 5: 선물/옵션 정정주문(CFOAT00200).

실행 (저장소 루트에서):
  python examples/domestic_futureoption/05_modify_order.py <종목코드> <원주문번호> <호가유형코드> <정정가격> <정정수량>

예:
  python examples/domestic_futureoption/05_modify_order.py A0173000 12345 00 947.10 1

원주문번호는 정상주문 응답에서 확인합니다(03 예제의 --show-response). 호출하면 연결된
계좌의 주문이 즉시 정정됩니다. 모의투자 계좌로 먼저 확인하세요. 응답 원문에는 계좌 관련
필드가 있을 수 있어 응답코드, 메시지, 필드 이름만 출력합니다.
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
    modify_futures_option_order,
)


def main(argv) -> int:
    if len(argv) != 6:
        print(
            "사용법: python examples/domestic_futureoption/05_modify_order.py "
            "<종목코드> <원주문번호> <호가유형코드> <정정가격> <정정수량>"
        )
        return 2

    instrument_code, raw_order_no, price_type_code, raw_price, raw_quantity = argv[1:]
    try:
        order_no = int(raw_order_no)
        order_price = float(raw_price)
        quantity = int(raw_quantity)
    except ValueError:
        print("실패: 원주문번호와 수량은 정수, 가격은 숫자여야 합니다.")
        return 2

    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = modify_futures_option_order(
            client, instrument_code, order_no, price_type_code, order_price, quantity
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
    print("응답 필드명: {}".format(", ".join(sorted(body))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
