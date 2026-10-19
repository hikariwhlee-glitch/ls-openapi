"""Verify simulated realtime KOSPI 200 futures trade and order-book feeds."""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

from ls_openapi import LSOpenAPI
from ls_openapi.websocket import LSWebSocket


TR_CODES = ("FC9", "FH9")
SUCCESS_CODES = {"00000", "0", "OK"}


def classify(message: Any) -> tuple[str | None, str, str]:
    """Return (TR, kind, note) for a WS message without exposing auth headers."""
    if isinstance(message, dict):
        header = message.get("header", {})
        body = message.get("body")
        if not isinstance(header, dict):
            header = {}
        tr_code = str(header.get("tr_cd", "")).strip()
        rsp_code = str(header.get("rsp_cd", "")).strip()
        rsp_msg = " ".join(str(header.get("rsp_msg", "")).split())[:160]
        if rsp_code:
            kind = "ack" if rsp_code in SUCCESS_CODES else "error"
            return tr_code or None, kind, f"{rsp_code} {rsp_msg}".strip()
        if tr_code in TR_CODES and body not in (None, {}, "", []):
            return tr_code, "data", ""
        return tr_code or None, "other", ""

    if isinstance(message, str):
        raw = message.strip()
        prefix = raw.split("|", 1)[0].split("^", 1)[0].strip()
        if prefix in TR_CODES:
            return prefix, "data", raw[:240]
    return None, "other", ""


def main() -> int:
    futures_code = os.getenv("LS_WS_FUTURES_CODE", "A0173000").strip()
    try:
        duration = int(os.getenv("LS_WS_DURATION_SECONDS", "20"))
    except ValueError:
        print("오류: LS_WS_DURATION_SECONDS는 정수여야 합니다.")
        return 2
    if not futures_code or len(futures_code) > 16 or duration < 5 or duration > 60:
        print("오류: 선물코드 또는 관찰시간(5~60초)이 올바르지 않습니다.")
        return 2

    rest = LSOpenAPI(timeout=10)
    feed = LSWebSocket(rest, simulated=True)
    subscribed: list[str] = []
    acknowledgements: set[str] = set()
    data_counts = {code: 0 for code in TR_CODES}
    first_data: dict[str, str] = {}

    try:
        feed.connect()
        print("모의투자 WebSocket 연결 성공")
        for tr_code in TR_CODES:
            feed.subscribe(tr_code, futures_code)
            subscribed.append(tr_code)
            print(f"구독 요청 전송: {tr_code}, 종목코드 {futures_code}")

        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            feed.connection.settimeout(min(2.0, max(0.2, remaining)))
            try:
                message = feed.recv()
            except feed._websocket_module.WebSocketTimeoutException:
                continue

            tr_code, kind, note = classify(message)
            if kind == "error":
                raise RuntimeError(f"{tr_code or 'WebSocket'} 구독 응답 오류: {note}")
            if kind == "ack":
                if tr_code in TR_CODES:
                    acknowledgements.add(tr_code)
                    print(f"구독 응답: {tr_code} 정상 ({note})")
                continue
            if kind == "data" and tr_code in data_counts:
                data_counts[tr_code] += 1
                if tr_code not in first_data:
                    first_data[tr_code] = note or json.dumps(
                        message, ensure_ascii=False, default=str
                    )[:240]
                continue

        total = sum(data_counts.values())
        print(
            f"관찰 결과: FC9 체결 메시지 {data_counts['FC9']}건, "
            f"FH9 호가 메시지 {data_counts['FH9']}건"
        )
        if acknowledgements:
            print("구독 승인 응답: " + ", ".join(sorted(acknowledgements)))
        for tr_code, preview in first_data.items():
            print(f"첫 {tr_code} 데이터: {preview}")
        if total == 0:
            raise RuntimeError(
                "관찰시간 안에 실시간 데이터가 도착하지 않았습니다. "
                "장 운영시간, 종목코드, 모의투자 WS 제공 여부를 확인하세요."
            )
        if not acknowledgements and not first_data:
            raise RuntimeError("구독 승인 또는 시세 데이터를 확인하지 못했습니다.")
        return 0
    except Exception as exc:
        print(f"실시간 검증 실패: {' '.join(str(exc).split())[:220]}")
        return 1
    finally:
        for tr_code in subscribed:
            try:
                feed.unsubscribe(tr_code, futures_code)
            except Exception:
                pass
        if subscribed:
            print("구독 해제 요청 전송")
        feed.close()


if __name__ == "__main__":
    sys.exit(main())
