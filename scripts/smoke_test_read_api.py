"""Read-only verification for public futures/options master data."""
from __future__ import annotations

import sys

from ls_openapi import LSOpenAPI


CHECKS = (
    ("t8426", {"dummy": ""}, "상품선물 마스터"),
    ("t8467", {"gubun": ""}, "지수선물 마스터"),
    ("t8433", {"dummy": ""}, "지수옵션 마스터"),
)


def main() -> int:
    try:
        client = LSOpenAPI()
        results = []
        for tr_code, params, label in CHECKS:
            result = client.call(tr_code, params)
            block_name = f"{tr_code}OutBlock"
            records = result.get(block_name, [])
            if isinstance(records, dict):
                records = [records]
            if not isinstance(records, list):
                records = []
            # A successful API response is meaningful even when a master is empty
            # outside its active session, but a missing expected block is not.
            if block_name not in result:
                print(f"조회 실패: {label}({tr_code}), 예상 응답 블록이 없습니다.")
                return 1
            results.append((tr_code, label, records))
    except Exception as exc:
        # Keep exception text and response payloads out of public Actions logs.
        print(f"읽기 전용 API 검증 실패 ({type(exc).__name__}).")
        return 1

    print("읽기 전용 API 검증 성공: 공개 상품 마스터 3종")
    for tr_code, label, records in results:
        print(f"- {label}({tr_code}): {len(records)}개")
        for row in records[:2]:
            name = str(row.get("hname", "")).strip()
            code = str(row.get("shcode", "")).strip()
            if name or code:
                print(f"  예: {name or '상품명 없음'} / 단축코드 {code or '없음'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
