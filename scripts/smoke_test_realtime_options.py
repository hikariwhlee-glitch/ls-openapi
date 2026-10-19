"""Verify simulated KOSPI 200 options trade and order-book feeds."""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

from ls_openapi import LSOpenAPI
from ls_openapi.websocket import LSWebSocket


TR_CODES = ("OC0", "OH0")
SUCCESS_CODES = {"00000", "0", "OK"}


def _options(response: dict[str, Any]) -> list[dict[str, Any]]:
    rows = response.get("t8433OutBlock", [])
    return rows if isinstance(rows, list) else []


def _select_option(rest: LSOpenAPI, requested_code: str) -> tuple[str, str]:
    # t8433 is the official index-options master. It avoids hard-coding a
    # contract that expires or changes between workflow runs.
    rows = _options(rest.call("t8433", {"dummy": "0"}))
    candidates = [
        row for row in rows
        if isinstance(row, dict)
        and str(row.get("shcode", "")).strip()
        and len(str(row.get("shcode", "")).strip()) in (6, 8)
    ]
    if not candidates:
        raise RuntimeError("지수옵션 마스터(t8433)에서 구독 가능한 종목을 찾지 못했습니다.")

    if requested_code:
        chosen = next(
            (row for row in candidates if str(row.get("shcode", "")).strip() == requested_code),
            None,
        )
        if chosen is None:
            raise ValueError(f"입력한 옵션코드 {requested_code}가 현재 마스터에 없습니다.")
    else:
        # Prefer the highest positive previous close, typically a liquid
        # near-the-money contract, and use the symbol as a stable tie-breaker.
        chosen = max(
            candidates,
            key=lambda row: (
                _as_float(row.get("jnilclose", row.get("recprice", 0))),
                str(row.get("shcode", "")),
            ),
        )
    return str(chosen["shcode"]).strip(), str(chosen.get("hname", "")).strip()


def _as_float(value: Any) -> float:
    try:
        return float(str(value).strip() or "0")
    except (TypeError, ValueError):
        return 0.0


def classify(message: Any) -> tuple[str | None, str, str]:
    """Return (TR, kind, note) without exposing authentication headers."""
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
    requested_code = os.getenv("LS_WS_OPTION_CODE", "").strip()
    try:
        duration = int(os.getenv("LS_WS_DURATION_SECONDS", "30"))
    except ValueError:
        print("오류: LS_WS_DURATION_SECONDS는 정수여야 합니다.")
        return 2
    if len(requested_code) > 8 or duration < 5 or duration > 60:
        print("오류: 옵션코드 또는 관찰시간(5~60초)이 올바르지 않습니다.")
        return 2

    rest = LSOpenAPI(timeout=10)
    feed = LSWebSocket(rest, simulated=True)
    subscribed: list[str] = []
    option_code = ""
    acknowledgements: set[str] = set()
    counts = {code: 0 for code in TR_CODES}
    first_data: dict[str, str] = {}

    try:
        option_code, option_name = _select_option(rest, requested_code)
        print(f"검증 종목: {option_name or '(종목명 없음)'} ({option_code})")
        feed.connect()
        print("모의투자 WebSocket 연결 성공")
        for tr_code in TR_CODES:
            feed.subscribe(tr_code, option_code)
            subscribed.append(tr_code)
            print(f"구독 요청 전송: {tr_code}, 종목코드 {option_code}")

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
            if kind == "data" and tr_code in counts:
                counts[tr_code] += 1
                if tr_code not in first_data:
                    first_data[tr_code] = note or json.dumps(
                        message, ensure_ascii=False, default=str
                    )[:240]

        print(f"관찰 결과: OC0 체결 메시지 {counts['OC0']}건, OH0 호가 메시지 {counts['OH0']}건")
        if acknowledgements:
            print("구독 승인 응답: " + ", ".join(sorted(acknowledgements)))
        for tr_code, preview in first_data.items():
            print(f"첫 {tr_code} 데이터: {preview}")
        if not acknowledgements:
            raise RuntimeError("옵션 실시간 구독 승인 응답을 받지 못했습니다.")
        if sum(counts.values()) == 0:
            raise RuntimeError(
                "승인은 받았지만 관찰시간 내 시세 메시지가 없습니다. "
                "장 운영시간과 모의투자 실시간 옵션 시세 제공 여부를 확인하세요."
            )
        return 0
    except Exception as exc:
        print(f"실시간 옵션 검증 실패: {' '.join(str(exc).split())[:240]}")
        return 1
    finally:
        for tr_code in subscribed:
            try:
                feed.unsubscribe(tr_code, option_code)
            except Exception:
                pass
        if subscribed:
            print("구독 해제 요청 전송")
        feed.close()


if __name__ == "__main__":
    sys.exit(main())

