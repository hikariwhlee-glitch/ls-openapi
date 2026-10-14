"""예제 4: 선물옵션 계좌잔고 및 평가현황(CFOAQ50600).

실행 (저장소 루트에서):
  python examples/domestic_futureoption/04_account_balance.py [YYYYMMDD]

날짜를 생략하면 오늘 날짜를 씁니다. 응답에는 계좌·잔고 값이 들어 있으므로 이 예제는
응답코드, 메시지, 블록/필드 이름만 출력하고 값은 출력하지 않습니다. 값이 필요하면 코드에서
``response.body`` 를 직접 다루되 로그나 공개 장소에 남기지 마세요.
"""

import sys
from datetime import date
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
    fetch_account_balance,
)


def main(argv) -> int:
    order_date = argv[1] if len(argv) > 1 else date.today().strftime("%Y%m%d")
    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = fetch_account_balance(client, order_date)
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
    for name in sorted(body):
        value = body[name]
        if isinstance(value, dict):
            print("블록 {}: 필드 {}".format(name, ", ".join(sorted(value))))
        elif isinstance(value, list):
            print("블록 {}: {}행".format(name, len(value)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
