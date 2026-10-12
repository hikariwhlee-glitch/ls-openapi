"""예제 1: 접근토큰 발급.

사전 준비
  1. LS증권 OPEN API 신청 후 앱키/시크릿키 확인
  2. 저장소 루트에서 `cp .env.example .env` 후 값 입력
  3. 저장소 루트에서 실행:  python examples/domestic_futureoption/01_issue_token.py

토큰 값은 화면에 출력하지 않습니다 (발급 여부, 길이, 유효기간만 표시).
"""

import sys
from pathlib import Path

# pip install -e . 없이도 실행되도록 src 폴더를 경로에 추가합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ls_openapi import AuthError, ConfigError, Settings, issue_token  # noqa: E402


def main() -> int:
    try:
        settings = Settings.from_env()
        token = issue_token(settings)
    except (ConfigError, AuthError) as exc:
        print("실패: {}".format(exc))
        return 1

    print("토큰 발급 성공")
    print("  token_type : {}".format(token.token_type))
    print("  토큰 길이  : {}자 (값은 출력하지 않습니다)".format(len(token.access_token)))
    print("  유효기간   : {}".format(
        "{}초".format(token.expires_in) if token.expires_in is not None else "응답에 없음"
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
