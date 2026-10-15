"""예제 4: KOSPI200 선물 실시간 체결(FC9)·호가(FH9) 수신.

모의투자 WebSocket 서버가 기본값입니다. 실전 접속은 --live 를 명시하세요.
실시간 구독만 하며 주문 요청은 보내지 않습니다.

실행:
  python examples/domestic_futureoption/04_futures_realtime.py A016C000 A0173000
  python examples/domestic_futureoption/04_futures_realtime.py --live A016C000
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ls_openapi import (  # noqa: E402
    AuthError,
    ConfigError,
    LSWebSocketClient,
    Settings,
    TokenManager,
    WebSocketError,
)


def main(argv) -> int:
    parser = argparse.ArgumentParser(description="KOSPI200 선물 실시간 시세 수신")
    parser.add_argument(
        "--live",
        action="store_true",
        help="실전 WebSocket 서버 사용 (기본값: 모의투자)",
    )
    parser.add_argument("codes", nargs="+", help="8자리 KOSPI200 선물 종목코드")
    args = parser.parse_args(argv[1:])

    invalid = [code for code in args.codes if len(code.strip()) != 8]
    if invalid:
        print("실패: 모든 선물 종목코드는 8자리여야 합니다.")
        return 2

    manager = None
    realtime = None
    try:
        settings = Settings.from_env()
        manager = TokenManager(settings)
        realtime = LSWebSocketClient(
            settings,
            token_manager=manager,
            simulation=not args.live,
        )
        realtime.connect()
        for code in args.codes:
            realtime.subscribe("FC9", code)
            realtime.subscribe("FH9", code)

        mode = "실전" if args.live else "모의투자"
        print("{} WebSocket 연결. 구독 응답과 시세를 기다립니다. 종료: Ctrl+C".format(mode))
        while True:
            print(json.dumps(realtime.receive(), ensure_ascii=False))
    except KeyboardInterrupt:
        print("\n사용자 요청으로 수신을 종료합니다.")
    except (ConfigError, AuthError, WebSocketError) as exc:
        print("실패: {}".format(exc))
        return 1
    finally:
        if realtime is not None:
            realtime.close()
        if manager is not None:
            try:
                manager.revoke()
            except AuthError as exc:
                print("참고: 토큰 폐기에 실패했습니다 ({})".format(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
