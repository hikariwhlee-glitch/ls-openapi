"""예제 2: 선물/옵션 현재가(t2111) 조회.

사전 준비
  1. 01_issue_token.py 로 인증이 되는지 먼저 확인
  2. 조회할 선물/옵션 종목코드(focode)를 준비

실행 (저장소 루트에서)
  python examples/domestic_futureoption/02_futures_price.py <종목코드>

토큰을 발급받아 한 번 조회한 뒤, 마지막에 토큰을 폐기합니다.
앱키/시크릿키/토큰 값은 화면에 출력하지 않습니다.

주의: 종목코드 형식과 현재 거래 중인 코드는 이 저장소에서 확인되지 않았습니다.
조회가 거절되면 종목코드가 맞는지 먼저 확인하세요. 응답 필드의 의미도 아직 정리되지
않아서, 서버가 돌려준 JSON을 그대로 출력합니다.
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
        print("사용법: python examples/domestic_futureoption/02_futures_price.py <종목코드>")
        return 2

    manager = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        client = LSClient(settings, token_manager=manager)
        response = fetch_current_price(client, argv[1])
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
