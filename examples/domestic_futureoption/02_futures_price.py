"""예제 2: 선물/옵션 현재가(t2111) 조회.

공식 요청 필드 focode는 8자리 종목코드입니다. 5자리 등 길이가 다른 값은
서버에서 빈 시세를 정상 응답처럼 돌려줄 수 있어 호출 전에 거부합니다.

실행 (저장소 루트에서)
  python examples/domestic_futureoption/02_futures_price.py <8자리 종목코드>

토큰을 발급받아 한 번 조회한 뒤, 마지막에 토큰을 폐기합니다.
앱키/시크릿키/토큰 값은 화면에 출력하지 않습니다.
"""

import json
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
    fetch_current_price,
)


def main(argv) -> int:
    if len(argv) != 2:
        print("사용법: python examples/domestic_futureoption/02_futures_price.py <8자리 종목코드>")
        return 2

    focode = argv[1].strip()
    if len(focode) != 8:
        print("실패: 선물/옵션 종목코드는 공식 요청 필드 기준 8자리여야 합니다.")
        return 2

    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = fetch_current_price(client, focode)
    except (ConfigError, AuthError, APIError, ValueError) as exc:
        print("실패: {}".format(exc))
        return 1
    finally:
        if manager is not None:
            try:
                manager.revoke()
            except AuthError as exc:
                print("참고: 토큰 폐기에 실패했습니다 ({})".format(exc))

    print(json.dumps(response.body, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
