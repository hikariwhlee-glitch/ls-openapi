"""One-shot read-only verification for GitHub Actions secrets."""
from __future__ import annotations
import sys
from ls_openapi import LSOpenAPI


def main() -> int:
    try:
        client = LSOpenAPI()
        # Public futures product master lookup; no account or order operation.
        result = client.call("t8426", {"dummy": ""})
        response_fields = set(result) - {"_continuation"}
        if not response_fields:
            print("Read-only API returned an empty response.")
            return 1
        records = result.get("t8426OutBlock", [])
        if isinstance(records, dict):
            records = [records]
        if not isinstance(records, list):
            records = []
    except Exception as exc:
        # Do not print exception text or response payloads to public Actions logs.
        print(f"Read-only API verification failed ({type(exc).__name__}).")
        return 1
    print(f"조회 성공: 상품선물 마스터(t8426), 응답 블록 {len(response_fields)}개.")
    print(f"조회된 상품 수: {len(records)}개")
    for row in records[:5]:
        name = str(row.get("hname", "")).strip()
        code = str(row.get("shcode", "")).strip()
        if name or code:
            print(f"- {name or '상품명 없음'} (단축코드 {code or '없음'})")
    if records and not any(str(row.get("hname", "")).strip() or str(row.get("shcode", "")).strip() for row in records[:5]):
        print("상품 행은 받았지만 이름·단축코드 필드가 비어 있습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
