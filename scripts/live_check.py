"""모의투자 실서버 점검 스크립트 (GitHub Actions 수동 실행용, 내 PC에서도 실행 가능).

실행 (저장소 루트에서, 앱키는 환경변수 또는 .env):
  python scripts/live_check.py auth
  python scripts/live_check.py quote  [종목코드,...]
  python scripts/live_check.py orderbook [종목코드]
  python scripts/live_check.py master
  python scripts/live_check.py websocket [종목코드]
  python scripts/live_check.py order-cycle [종목코드]   # 주문 → 정정 → 취소 (모의투자 주문이 실제로 나갑니다)

종목코드를 생략하면 t8467 지수선물 마스터에서 코스피200 선물 월물 코드를 조회해 씁니다.
마스터 조회가 실패하면 환경변수 LS_FOCODE(쉼표 구분)로 대신합니다. 인자로 주면 그 값을 우선합니다.

공개 저장소의 Actions 로그는 누구나 볼 수 있으므로 앱키·토큰·계좌 정보는 출력하지 않습니다.
시세는 공개 데이터라 값을 출력하고, 주문 응답은 응답코드·메시지·필드 이름만 출력합니다.
성공 판정이 필요한 곳에서 "rsp_cd가 00으로 시작"을 성공으로 보는 것은 공식 코드표로 확인된
규칙이 아니라 지금까지 관측한 값(00000, 00040)에 기대는 임시 기준입니다.
"""

import json
import os
import signal
import sys
import time
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ls_openapi import (  # noqa: E402
    APIError,
    AuthError,
    ConfigError,
    LSClient,
    LSWebSocketClient,
    Settings,
    TokenManager,
    WebSocketError,
    cancel_futures_option_order,
    fetch_current_price,
    fetch_index_futures_master,
    fetch_orderbook,
    modify_futures_option_order,
    submit_futures_option_order,
)

PAUSE = 1.1  # TR별 초당 제한이 확인되지 않은 시세 TR 사이의 여유
TICK = Decimal("0.05")  # 코스피200 선물 호가 단위(이전 모의투자 확인에서 사용한 값)


class CheckFailed(Exception):
    pass


def _body(response):
    return response.body if isinstance(response.body, dict) else {}


def _short(value, limit=60):
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _print_structure(body, show_values):
    print("  최상위 키:", sorted(body))
    for name in sorted(body):
        value = body[name]
        if isinstance(value, dict):
            print("  [{}] (객체)".format(name))
            for key in sorted(value):
                print("    {}{}".format(key, " = " + _short(value[key]) if show_values else ""))
        elif isinstance(value, list):
            print("  [{}] (배열 {}건)".format(name, len(value)))
            if value and isinstance(value[0], dict):
                print("    첫 항목 키:", sorted(value[0]))
        elif name in ("rsp_cd", "rsp_msg") or show_values:
            print("  {} = {}".format(name, _short(value)))


def _is_ok(body):
    return str(body.get("rsp_cd", "")).startswith("00")


def _master_codes(client):
    """t8467 마스터에서 코스피200 선물 월물 후보 코드를 고릅니다.

    응답 구조는 공식 명세(t8467OutBlock 배열, shcode/hname)를 따릅니다. 월물만 고르는 기준
    ("hname 이 '코스피200 F' 로 시작")은 t2111 응답에서 관측한 종목명(예: '코스피200 F 202612')에
    기대는 임시 기준이며, 스프레드 등 다른 종목의 이름 규칙은 확인되지 않았습니다.
    """
    response = fetch_index_futures_master(client, "")
    body = _body(response)
    rows = body.get("t8467OutBlock")
    if not _is_ok(body) or not isinstance(rows, list):
        raise CheckFailed("t8467 응답에서 종목 목록을 읽지 못했습니다 (rsp_cd={!r}).".format(body.get("rsp_cd")))
    codes = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        code = str(row.get("shcode", "")).strip()
        if len(code) == 8 and str(row.get("hname", "")).strip().startswith("코스피200 F"):
            codes.append(code)
    print("[마스터] t8467 {}건 중 월물 후보 {}건: {}".format(len(rows), len(codes), codes))
    if not codes:
        raise CheckFailed("t8467 목록에서 월물 후보를 찾지 못했습니다.")
    return codes


def _focodes(args, client=None):
    """종목코드 결정: 인자 > t8467 마스터 > LS_FOCODE 환경변수 순서입니다."""
    if args:
        raw = args[0]
    else:
        raw = ""
        if client is not None:
            try:
                time.sleep(PAUSE)
                return _master_codes(client)
            except (APIError, CheckFailed) as exc:
                print("[마스터] 사용 못 함: {}".format(exc))
        raw = os.environ.get("LS_FOCODE", "")
        if raw:
            print("[종목코드] LS_FOCODE 환경변수를 대신 사용합니다.")
    codes = [c.strip() for c in raw.split(",") if c.strip()]
    if not codes:
        raise CheckFailed("종목코드를 정하지 못했습니다. 인자로 주거나 LS_FOCODE를 설정하세요.")
    return codes


def _client():
    settings = Settings.from_env()
    manager = TokenManager(settings)
    return settings, manager, LSClient(settings, token_manager=manager)


def check_auth(args):
    settings = Settings.from_env()
    manager = TokenManager(settings)
    try:
        token = manager.get_token()
        print("[발급] 성공 token_type={} expires_in={}".format(token.token_type, token.expires_in))
    finally:
        result = manager.revoke()
        print("[폐기]", (result or {}).get("code"), "/", (result or {}).get("message"))


def check_quote(args):
    settings, manager, client = _client()
    failed = []
    try:
        codes = _focodes(args, client)
        for index, code in enumerate(codes):
            if index:
                time.sleep(PAUSE)
            print("\n[t2111] focode={}".format(code))
            response = fetch_current_price(client, code)
            body = _body(response)
            block = body.get("t2111OutBlock")
            if not _is_ok(body) or not isinstance(block, dict) or block.get("focode") != code:
                failed.append(code)
                print("  실패 rsp_cd={!r} rsp_msg={!r}".format(body.get("rsp_cd"), body.get("rsp_msg")))
            _print_structure(body, show_values=True)
    finally:
        manager.revoke()
    if failed:
        raise CheckFailed("조회 실패 종목: {}".format(failed))
    print("\n[요약] 성공:", codes)


def check_orderbook(args):
    settings, manager, client = _client()
    try:
        code = _focodes(args, client)[0]
        time.sleep(PAUSE)
        print("[t2112] shcode={}".format(code))
        response = fetch_orderbook(client, code)
        body = _body(response)
        _print_structure(body, show_values=True)
    finally:
        manager.revoke()
    if not _is_ok(body):
        raise CheckFailed("t2112 실패 rsp_cd={!r}".format(body.get("rsp_cd")))


def check_master(args):
    settings, manager, client = _client()
    try:
        print("[t8467] gubun='' (코스피200 선물)")
        response = fetch_index_futures_master(client, "")
        body = _body(response)
        _print_structure(body, show_values=False)
        for name, value in body.items():
            if isinstance(value, list):
                print("  {} 행 수: {}".format(name, len(value)))
    finally:
        manager.revoke()
    if not _is_ok(body):
        raise CheckFailed("t8467 실패 rsp_cd={!r}".format(body.get("rsp_cd")))


class _Timeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise _Timeout()


def check_websocket(args):
    seconds = int(os.environ.get("LS_WS_SECONDS", "20"))
    settings, manager, client = _client()
    try:
        code = _focodes(args, client)[0]
    except BaseException:
        manager.revoke()
        raise
    realtime = LSWebSocketClient(settings, token_manager=manager, simulation=True)
    received = []
    signal.signal(signal.SIGALRM, _on_alarm)
    try:
        realtime.connect()
        print("[WS] 모의투자 서버 연결 성공")
        realtime.subscribe("FC9", code)
        realtime.subscribe("FH9", code)
        print("[WS] FC9/FH9 구독 요청 전송 {}. {}초 동안 수신합니다.".format(code, seconds))
        signal.alarm(seconds)
        while True:
            message = realtime.receive()
            received.append(message)
            if len(received) <= 3:
                print("[WS] 수신", json.dumps(message, ensure_ascii=False)[:300])
    except _Timeout:
        pass
    except WebSocketError as exc:
        raise CheckFailed("WebSocket 오류: {}".format(exc))
    finally:
        signal.alarm(0)
        realtime.close()
        manager.revoke()
    print("[WS] 수신 {}건".format(len(received)))
    if not received:
        # 장이 닫혀 있으면 시세가 없을 수 있어, 연결·구독 성공과 구분해 알립니다.
        print("[WS] 프레임을 받지 못했습니다(장 마감/구독 응답 없음 가능). 실패로 보지 않습니다.")


def _find_key(obj, key, path=""):
    """응답 안에서 key 이름의 필드를 찾아 (경로, 값)을 돌려줍니다. 필드명 확인용입니다."""
    if isinstance(obj, dict):
        for name, value in obj.items():
            here = "{}.{}".format(path, name) if path else name
            if name == key:
                return here, value
            found = _find_key(value, key, here)
            if found:
                return found
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            found = _find_key(value, key, "{}[{}]".format(path, index))
            if found:
                return found
    return None


def _step(label, response):
    body = _body(response)
    print("\n[{}] rsp_cd={!r} rsp_msg={!r}".format(label, body.get("rsp_cd"), body.get("rsp_msg")))
    _print_structure(body, show_values=False)
    return body


def check_order_cycle(args):
    settings, manager, client = _client()
    order_no = None
    try:
        code = _focodes(args, client)[0]
        time.sleep(PAUSE)
        quote = _body(fetch_current_price(client, code)).get("t2111OutBlock") or {}
        price = Decimal(str(quote.get("price", "0")))
        lower_limit = Decimal(str(quote.get("dnlmtprice", "0")))
        if price <= 0:
            raise CheckFailed("현재가를 읽지 못했습니다.")
        # 체결되지 않도록 현재가보다 한참 낮은 매수 지정가를 씁니다(하한가 아래로는 내리지 않음).
        order_price = max(price - Decimal("5"), lower_limit + TICK)
        order_price = (order_price / TICK).to_integral_value() * TICK
        modify_price = order_price + TICK
        print("[준비] {} 현재가={} 매수지정가={} 정정가={} 수량=1".format(code, price, order_price, modify_price))
        time.sleep(PAUSE)

        placed = submit_futures_option_order(client, code, "2", "00", float(order_price), 1)
        body = _step("정상주문 CFOAT00100", placed)
        if not _is_ok(body):
            raise CheckFailed("정상주문이 접수되지 않았습니다.")
        found = _find_key(body, "OrdNo")
        if not found or not str(found[1]).strip().lstrip("0").isdigit():
            raise CheckFailed(
                "응답에서 주문번호 필드(OrdNo)를 찾지 못했습니다. 위 필드 이름을 확인하세요."
            )
        order_no = int(str(found[1]).strip())
        print("[주문번호] 응답 필드 경로 {} 에서 읽음 (값은 출력하지 않음)".format(found[0]))
        time.sleep(PAUSE)

        modified = modify_futures_option_order(client, code, order_no, "00", float(modify_price), 1)
        mbody = _step("정정 CFOAT00200", modified)
        if not _is_ok(mbody):
            raise CheckFailed("정정이 접수되지 않았습니다.")
        new_found = _find_key(mbody, "OrdNo")
        print("[정정 응답] OrdNo 필드 {}".format("있음: " + new_found[0] if new_found else "없음"))
        time.sleep(PAUSE)
    finally:
        cancel_error = None
        if order_no is not None:
            try:
                cancelled = cancel_futures_option_order(client, code, order_no, 1)
                cbody = _step("취소 CFOAT00300", cancelled)
                if not _is_ok(cbody):
                    cancel_error = "취소가 접수되지 않았습니다 (rsp_cd={!r}).".format(cbody.get("rsp_cd"))
            except (APIError, ValueError) as exc:
                cancel_error = "취소 호출 실패: {}".format(exc)
        manager.revoke()
        if cancel_error:
            print("\n경고:", cancel_error, "모의투자 계좌에 미체결 주문이 남았을 수 있습니다.")
            raise CheckFailed(cancel_error)


SCENARIOS = {
    "auth": check_auth,
    "quote": check_quote,
    "orderbook": check_orderbook,
    "master": check_master,
    "websocket": check_websocket,
    "order-cycle": check_order_cycle,
}


def main(argv):
    if len(argv) < 2 or argv[1] not in SCENARIOS:
        print("사용법: python scripts/live_check.py {{{}}} [인자]".format("|".join(SCENARIOS)))
        return 2
    try:
        SCENARIOS[argv[1]](argv[2:])
    except (ConfigError, AuthError, APIError, ValueError, CheckFailed) as exc:
        print("\n실패: {}".format(exc))
        return 1
    print("\n완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
