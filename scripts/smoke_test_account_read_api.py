"""Read-only futures balance verification with opt-in paper-account logging."""
from __future__ import annotations

import os
import sys

from ls_openapi import LSAPIError, LSOpenAPI


def rows(value):
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def field(row, name):
    value = row.get(name, "")
    return str(value).strip() if value is not None else ""


def main() -> int:
    log_mode = os.getenv("LS_ACCOUNT_LOG_MODE", "redacted").strip().lower()
    if log_mode not in {"redacted", "paper"}:
        print("계좌 로그 모드는 redacted 또는 paper만 허용됩니다.")
        return 1

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
        print(f"계좌 잔고 조회 실패{suffix}. 계좌 응답 내용은 로그에 출력하지 않습니다.")
        return 1
    except Exception as exc:
        print(f"계좌 잔고 조회 실패 ({type(exc).__name__}). 계좌 응답 내용은 로그에 출력하지 않습니다.")
        return 1

    summary = result.get("t0441OutBlock")
    positions = rows(result.get("t0441OutBlock1"))
    if not isinstance(summary, dict) or "t0441OutBlock1" not in result:
        print("계좌 잔고 조회 실패: 예상 응답 구조가 아닙니다. 계좌 응답 내용은 로그에 출력하지 않습니다.")
        return 1

    if log_mode == "redacted":
        print("계좌 잔고 조회 성공: t0441 응답 구조 확인. 계좌 상세 데이터는 로그에 기록하지 않았습니다.")
        return 0

    # The paper mode is an explicit per-run opt-in; never print account IDs or credentials.
    print("모의투자 계좌 잔고 조회 성공: t0441")
    print(
        "계좌 합계: "
        f"평가금액={field(summary, 'tappamt') or '-'}, "
        f"평가손익={field(summary, 'tsunik') or '-'}, "
        f"매매손익={field(summary, 'tdtsunik') or '-'}"
    )
    print(f"보유 종목 행 수: {len(positions)}")
    if not positions:
        print("현재 보유 잔고 행이 없습니다.")
    for row in positions[:100]:
        print(
            "- "
            f"종목코드={field(row, 'expcode') or '-'}, "
            f"구분코드={field(row, 'medosu') or field(row, 'medocd') or '-'}, "
            f"잔고수량={field(row, 'jqty') or '-'}, "
            f"청산가능수량={field(row, 'cqty') or '-'}, "
            f"평균단가={field(row, 'pamt') or '-'}, "
            f"현재가={field(row, 'price') or '-'}, "
            f"평가금액={field(row, 'appamt') or '-'}, "
            f"평가손익={field(row, 'dtsunik1') or '-'}, "
            f"수익률={field(row, 'sunikrt') or '-'}"
        )
    if len(positions) > 100:
        print(f"로그 길이 제한으로 나머지 {len(positions) - 100}개 행은 생략했습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
