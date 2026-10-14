"""예제 4: 선물/옵션 계좌잔고 조회(CFOAQ50600).

실행 (저장소 루트에서):
  python examples/domestic_futureoption/04_futures_option_balance.py YYYYMMDD

응답 원문에는 계좌 및 잔고 정보가 포함될 수 있으므로, 전체 응답을 출력하지 않습니다.
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
    fetch_futures_option_balance,
)


def main(argv) -> int:
    if len(argv) != 2:
        print(
            "사용법: python examples/domestic_futureoption/04_futures_option_balance.py "
            "YYYYMMDD"
        )
        return 2

    order_date = argv[1]
    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = fetch_futures_option_balance(client, order_date=order_date)
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
