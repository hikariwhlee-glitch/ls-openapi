"""Verify read-only futures market data using a code from the index futures master."""
from __future__ import annotations

import sys

from ls_openapi import LSAPIError, LSOpenAPI


def records(value):
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def failure_detail(exc: Exception, client: LSOpenAPI) -> str:
    if not isinstance(exc, LSAPIError):
        return type(exc).__name__
    payload = exc.payload if isinstance(exc.payload, dict) else {}
    code = str(payload.get("rsp_cd", "")).strip()
    message = " ".join(str(payload.get("rsp_msg", "")).split())
    for secret in (client.app_key, client.app_secret):
        if secret:
            message = message.replace(secret, "[redacted]")
    detail = "LS API 오류"
    if code:
        detail += f" {code}"
    if message:
        detail += f": {message[:160]}"
    return detail


def main() -> int:
    client = LSOpenAPI()
    failures = 0
    try:
        master = client.call("t8467", {"gubun": ""})
        products = records(master.get("t8467OutBlock"))
        if not products:
            print("실패: 지수선물 마스터(t8467)에서 시세 조회용 종목코드를 가져오지 못했습니다.")
            return 1
        product = next((row for row in products if row.get("shcode")), None)
        if product is None:
            print("실패: 지수선물 마스터 응답에 단축코드가 없습니다.")
            return 1
        code = str(product["shcode"]).strip()
        name = str(product.get("hname", "")).strip()
    except Exception as exc:
        print(f"실패: 지수선물 종목 준비 단계 ({failure_detail(exc, client)}).")
        return 1

    print(f"시세 조회 종목: {name or '지수선물'} ({code})")

    checks = (
        ("t2111", "현재가", {"focode": code}, "t2111OutBlock"),
        ("t2112", "호가", {"shcode": code}, "t2112OutBlock"),
        (
            "t2212",
            "시간대별 체결",
            {"focode": code, "cvolume": 0, "stime": "0000", "etime": "2359", "cts_time": ""},
            "t2212OutBlock1",
        ),
        (
            "t2214",
            "기간별 시세",
            {"shcode": code, "futcheck": "0", "date": "", "cts_code": "", "lastdate": "99999999", "cnt": 10},
            "t2214OutBlock1",
        ),
        (
            "t8464",
            "틱 차트",
            {
                "shcode": code,
                "ncnt": 1,
                "qrycnt": 10,
                "nday": "0",
                "sdate": "",
                "stime": "000000",
                "edate": "99999999",
                "etime": "235959",
                "cts_date": "",
                "cts_time": "",
                "comp_yn": "N",
            },
            "t8464OutBlock1",
        ),
    )

    for tr_code, label, params, output_block in checks:
        try:
            result = client.call(tr_code, params)
            if output_block not in result:
                print(f"실패: {label}({tr_code}), 응답 블록이 없습니다.")
                failures += 1
                continue
            value = result[output_block]
            rows = records(value)
            if tr_code == "t2111" and isinstance(value, dict):
                price = str(value.get("price", "")).strip()
                print(f"성공: {label}({tr_code})" + (f", 현재가 {price}" if price else ""))
            elif tr_code == "t2112" and isinstance(value, dict):
                ask = str(value.get("offerho1", "")).strip()
                bid = str(value.get("bidho1", "")).strip()
                print(f"성공: {label}({tr_code}), 매도1호가 {ask or '-'}, 매수1호가 {bid or '-'}")
            else:
                print(f"성공: {label}({tr_code}), 응답 행 {len(rows)}개")
        except Exception as exc:
            print(f"실패: {label}({tr_code}) ({failure_detail(exc, client)}).")
            failures += 1

    if failures:
        print(f"시세 조회 검증 완료: 성공 {len(checks) - failures}/{len(checks)}, 실패 {failures}개.")
        return 1
    print(f"시세 조회 검증 성공: {len(checks)}/{len(checks)}개 기능.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
