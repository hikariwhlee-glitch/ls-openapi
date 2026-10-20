"""Capture LS simulated order events around a guarded one-contract buy fill."""
from __future__ import annotations

import os
import sys
import threading
import time
from typing import Any

from ls_openapi import LSOpenAPI
from ls_openapi.websocket import LSWebSocket

EVENT_TRS = ("C01", "H01", "O01")
SUCCESS_CODES = {"00000", "0", "OK"}
ACK = "I_ACKNOWLEDGE_PAPER_SIMULATED_TRADING"


def parse_message(message: Any) -> tuple[str, str, str, dict[str, Any]]:
    if not isinstance(message, dict):
        return "", "other", "", {}
    header = message.get("header", {})
    body = message.get("body", {})
    if not isinstance(header, dict):
        header = {}
    if not isinstance(body, dict):
        body = {}
    tr_code = str(header.get("tr_cd", "")).strip()
    rsp_code = str(header.get("rsp_cd", "")).strip()
    rsp_msg = " ".join(str(header.get("rsp_msg", "")).split())[:140]
    if rsp_code:
        return tr_code, "ack" if rsp_code in SUCCESS_CODES else "error", f"{rsp_code} {rsp_msg}".strip(), body
    if tr_code in EVENT_TRS and body:
        return tr_code, "event", "", body
    return tr_code, "other", "", body


def event_summary(tr_code: str, body: dict[str, Any]) -> str:
    order_no = str(body.get("ordno", "")).strip()
    suffix = order_no[-4:] if order_no else "미확인"
    fields = [f"주문번호 끝자리 {suffix}"]
    if tr_code == "C01":
        fields.extend([
            f"체결수량 {str(body.get('chevol', '')).strip() or '미확인'}",
            f"체결가 {str(body.get('cheprice', '')).strip() or '미확인'}",
        ])
    elif tr_code == "H01":
        fields.append(f"거부코드 {str(body.get('rejcode', '')).strip() or '없음'}")
    return ", ".join(fields)


def main() -> int:
    if os.getenv("LS_ORDER_CONFIRM", "") != ACK:
        print("중단: 명시적인 모의투자 주문 확인 문자열이 없습니다.")
        return 2

    rest = LSOpenAPI(timeout=10)
    feed = LSWebSocket(rest, simulated=True)
    stop = threading.Event()
    ready = threading.Event()
    lock = threading.Lock()
    acknowledged: set[str] = set()
    counts = {tr: 0 for tr in EVENT_TRS}
    stream_errors: list[str] = []

    def listen() -> None:
        try:
            feed.connect()
            print("모의투자 주문 이벤트 WebSocket 연결 성공")
            for tr_code in EVENT_TRS:
                feed.subscribe(tr_code)
                print(f"계좌 이벤트 구독 요청: {tr_code}")
            deadline = time.monotonic() + 5
            while not stop.is_set() and time.monotonic() < deadline:
                feed.connection.settimeout(0.5)
                try:
                    message = feed.recv()
                except feed._websocket_module.WebSocketTimeoutException:
                    continue
                tr_code, kind, note, body = parse_message(message)
                if kind == "error":
                    raise RuntimeError(f"{tr_code or 'WebSocket'} 구독 오류: {note}")
                if kind == "ack" and tr_code in EVENT_TRS:
                    with lock:
                        acknowledged.add(tr_code)
                    print(f"구독 승인: {tr_code} ({note})")
                    continue
                if kind == "event" and tr_code in counts:
                    with lock:
                        counts[tr_code] += 1
                        n = counts[tr_code]
                    print(f"주문 이벤트 {tr_code} 수신 #{n}: {event_summary(tr_code, body)}")
            if not acknowledged:
                print("별도 승인 프레임 없음; 주문 이벤트 수신 여부로 검증합니다.")
            ready.set()
            while not stop.is_set():
                feed.connection.settimeout(1.0)
                try:
                    message = feed.recv()
                except feed._websocket_module.WebSocketTimeoutException:
                    continue
                tr_code, kind, note, body = parse_message(message)
                if kind == "error":
                    raise RuntimeError(f"{tr_code or 'WebSocket'} 구독 오류: {note}")
                if kind == "event" and tr_code in counts:
                    with lock:
                        counts[tr_code] += 1
                        n = counts[tr_code]
                    print(f"주문 이벤트 {tr_code} 수신 #{n}: {event_summary(tr_code, body)}")
        except Exception as exc:
            stream_errors.append(" ".join(str(exc).split())[:200])
            ready.set()
        finally:
            for tr_code in EVENT_TRS:
                try:
                    feed.unsubscribe(tr_code)
                except Exception:
                    pass
            feed.close()
            print("주문 이벤트 구독 해제")

    listener = threading.Thread(target=listen, name="ls-order-events", daemon=True)
    listener.start()
    if not ready.wait(10):
        stop.set()
        listener.join(timeout=5)
        print("실패: WebSocket 연결/구독 준비 시간 초과")
        return 1
    if stream_errors:
        stop.set()
        listener.join(timeout=5)
        print(f"실패: {stream_errors[0]}")
        return 1

    print("주문 이벤트 구독 준비 완료; A016C000 매수 체결 확인 시작")
    try:
        import verify_paper_new_buy_fill
        order_result = verify_paper_new_buy_fill.main()
    except Exception as exc:
        print(f"주문 로직 예외: {' '.join(str(exc).split())[:200]}")
        order_result = 1
    time.sleep(5)
    stop.set()
    listener.join(timeout=10)

    with lock:
        final_counts = dict(counts)
        final_acks = sorted(acknowledged)
    print("이벤트 수신 건수: " + ", ".join(f"{tr} {final_counts[tr]}건" for tr in EVENT_TRS))
    print("이벤트 구독 승인: " + ", ".join(final_acks))
    if stream_errors:
        print(f"이벤트 스트림 오류: {stream_errors[0]}")
        return 1
    if order_result != 0:
        print("주문 로직이 완료되지 않았습니다. 추가 주문 없이 잔고/미체결을 확인하세요.")
        return order_result
    missing = [tr for tr in ("O01", "C01") if final_counts[tr] == 0]
    if missing:
        print("REST상 체결은 확인했지만 다음 WebSocket 이벤트를 못 받았습니다: " + ", ".join(missing))
        return 1
    print("신규 매수 체결 검증 완료: 주문접수(O01), 체결(C01), 잔고 반영 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
