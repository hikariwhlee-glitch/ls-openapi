"""Privacy-safe read-only account balance verification."""
from __future__ import annotations

import sys

from ls_openapi import LSAPIError, LSOpenAPI


def main() -> int:
    try:
        client = LSOpenAPI()
        result = client.call(
            "t0441",
            {"cts_expcode": "", "cts_medocd": ""},
        )
    except LSAPIError as exc:
        payload = exc.payload if isinstance(exc.payload, dict) else {}
        code = str(payload.get("rsp_cd", "")).strip()
        suffix = f" (LS API code {code})" if code else ""
        print(f"계좌 잔고 조회 실패{suffix}. 상세 오류와 계좌 정보는 로그에 출력하지 않습니다.")
        return 1
    except Exception as exc:
        print(f"계좌 잔고 조회 실패 ({type(exc).__name__}). 상세 내용은 로그에 출력하지 않습니다.")
        return 1

    # Do not print account number, cash, holdings, quantities, prices, or row counts.
    required_blocks = ("t0441OutBlock", "t0441OutBlock1")
    missing = [block for block in required_blocks if block not in result]
    if missing:
        print("계좌 잔고 조회 실패: 예상 응답 구조가 아닙니다. 민감한 응답 내용은 로그에 출력하지 않습니다.")
        return 1

    print("계좌 잔고 조회 성공: t0441 응답 구조 확인. 잔고 상세 데이터는 로그에 기록하지 않았습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
