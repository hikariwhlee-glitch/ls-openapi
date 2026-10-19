"""Verify simulated futures order events while running the guarded order lifecycle."""
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


def safe_event_summary(tr_code: str, body: dict[str, Any]) -> str:
    # Deliberately omit account number, user ID, and full order numbers.
    full_order_no = str(body.get("ordno", "")).strip()
    suffix = full_order_no[-4:] if full_order_no else "미확인"
    fields = [f"주문번호 끝자리 {suffix}"]
    if tr_code == "C01":
        qty = str(body.get("chevol", "")).strip()
        price = str(body.get("cheprice", "")).strip()
        fields.append(f"체결수량 {qty or '미확인'}")
        if price:
            fields.append(f"체결가 {price}")
    elif tr_code == "H01":
        fields.append(f"주문구분 {str(body.get('ordgb', '')).strip() or '미확인'}")
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
            ack_deadline = time.monotonic() + 20
            while not stop.is_set() and time.monotonic() < ack_deadline:
                feed.connection.settimeout(1.0)
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
                        got = ", ".join(sorted(acknowledged))
                    print(f"구독 승인: {tr_code} ({note})")
                    if len(acknowledged) == len(EVENT_TRS):
                        ready.set()
                        break
                    continue
                if kind == "event" and tr_code in counts:
                    with lock:
                        counts[tr_code] += 1
                        n = counts[tr_code]
                    print(f"주문 이벤트 {tr_code} 수신 #{n}: {safe_event_summary(tr_code, body)}")
            if not ready.is_set() and not stop.is_set():
                raise RuntimeError("C01/H01/O01 계좌 이벤트 구독 승인을 모두 받지 못했습니다.")

            # Continue reading while the order workflow is active. After it
            # finishes, the caller allows a short drain window before stopping.
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
                    print(f"주문 이벤트 {tr_code} 수신 #{n}: {safe_event_summary(tr_code, body)}")
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
    if not ready.wait(25):
        stop.set()
        listener.join(timeout=5)
        print("실패: 주문 이벤트 구독 승인을 기다리는 동안 시간 초과")
        return 1
    if stream_errors:
        stop.set()
        listener.join(timeout=5)
        print(f"실패: {stream_errors[0]}")
        return 1
    with lock:
        if acknowledged != set(EVENT_TRS):
            stop.set()
            listener.join(timeout=5)
            print("실패: C01/H01/O01 구독 승인이 완전하지 않습니다.")
            return 1
    print("C01 체결, H01 정정/취소, O01 접수 이벤트 구독 확인; 주문 로직 시작")

    try:
        # This is the existing one-contract, sell-to-close paper lifecycle test.
        import verify_paper_order_api
        order_result = verify_paper_order_api.main()
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
        print("주문 로직이 완료되지 않았습니다. 추가 주문 없이 계좌의 잔고와 미체결을 확인하세요.")
        return order_result
    missing = [tr for tr in ("O01", "H01") if final_counts[tr] == 0]
    if missing:
        print("주문 로직은 완료됐지만 다음 이벤트를 수신하지 못했습니다: " + ", ".join(missing))
        return 1
    if final_counts["C01"] == 0:
        print("신규/정정/취소 이벤트는 수신했지만 C01 체결 이벤트는 수신하지 못했습니다.")
        return 1
    print("주문 이벤트 검증 완료: 접수(O01), 정정/취소(H01), 체결(C01)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
