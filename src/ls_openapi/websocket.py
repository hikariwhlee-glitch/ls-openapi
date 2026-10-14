"""선물 실시간 시세 WebSocket 클라이언트."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Set, Tuple

import websocket

from .auth import TokenManager
from .config import Settings
from .exceptions import WebSocketError

LIVE_WS_URL = "wss://openapi.ls-sec.co.kr:9443/websocket"
SIMULATION_WS_URL = "wss://openapi.ls-sec.co.kr:29443/websocket"

# 1st MVP에서 제공하는 KOSPI200 선물 실시간 체결 및 호가
SUPPORTED_TRS = frozenset({"FC9", "FH9"})


class LSWebSocketClient:
    """KOSPI200 선물 실시간 체결(FC9)·호가(FH9) 동기식 클라이언트.

    모의투자 접속이 기본값입니다. 연결된 뒤 subscribe()를 호출하면
    공식 프레임 형식(header.token, header.tr_type=3)으로 구독합니다.
    """

    def __init__(
        self,
        settings: Settings,
        token_manager: Optional[TokenManager] = None,
        *,
        simulation: bool = True,
        timeout: float = 10.0,
    ) -> None:
        self._tokens = token_manager or TokenManager(settings)
        self._url = SIMULATION_WS_URL if simulation else LIVE_WS_URL
        self._timeout = timeout
        self._socket: Optional[Any] = None
        self._subscriptions: Set[Tuple[str, str]] = set()

    @property
    def connected(self) -> bool:
        """WebSocket 소켓이 연결된 상태인지 반환합니다."""
        return self._socket is not None

    def connect(self) -> None:
        """모의투자(기본) 또는 실전 WebSocket 서버에 연결합니다."""
        if self._socket is not None:
            raise WebSocketError("WebSocket이 이미 연결되어 있습니다.")
        try:
            self._socket = websocket.create_connection(
                self._url, timeout=self._timeout
            )
            # 연결 수립에는 timeout을 적용하고, 이후 수신은 장중에 계속 대기합니다.
            self._socket.settimeout(None)
        except (websocket.WebSocketException, OSError) as exc:
            self._socket = None
            raise WebSocketError(
                "LS증권 WebSocket 연결에 실패했습니다 ({}).".format(type(exc).__name__)
            ) from exc

    def subscribe(self, tr_cd: str, tr_key: str) -> None:
        """FC9 체결 또는 FH9 호가를 구독합니다. 현재 지원 종목코드는 8자리입니다."""
        self._validate_subscription(tr_cd, tr_key)
        self._send_subscription(tr_cd, tr_key, tr_type="3")
        self._subscriptions.add((tr_cd, tr_key))

    def unsubscribe(self, tr_cd: str, tr_key: str) -> None:
        """등록한 실시간 시세 구독을 해제합니다."""
        self._validate_subscription(tr_cd, tr_key)
        self._send_subscription(tr_cd, tr_key, tr_type="4")
        self._subscriptions.discard((tr_cd, tr_key))

    def receive(self) -> Dict[str, Any]:
        """다음 서버 프레임을 JSON 객체로 받아 반환합니다."""
        socket = self._require_socket()
        try:
            raw = socket.recv()
        except (websocket.WebSocketException, OSError) as exc:
            raise WebSocketError(
                "LS증권 WebSocket 수신에 실패했습니다 ({}).".format(type(exc).__name__)
            ) from exc
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        try:
            message = json.loads(raw)
        except (TypeError, ValueError, UnicodeDecodeError) as exc:
            raise WebSocketError("WebSocket 응답이 JSON 형식이 아닙니다.") from exc
        if not isinstance(message, dict):
            raise WebSocketError("WebSocket 응답이 JSON 객체가 아닙니다.")
        return message

    def close(self) -> None:
        """열려 있는 구독을 해제하고 연결을 닫습니다."""
        socket = self._socket
        if socket is None:
            return
        try:
            for tr_cd, tr_key in tuple(self._subscriptions):
                try:
                    self._send_subscription(tr_cd, tr_key, tr_type="4")
                except (websocket.WebSocketException, OSError):
                    break
        finally:
            self._subscriptions.clear()
            self._socket = None
            socket.close()

    def __enter__(self) -> "LSWebSocketClient":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def _validate_subscription(self, tr_cd: str, tr_key: str) -> None:
        if tr_cd not in SUPPORTED_TRS:
            raise ValueError(
                "현재 지원하는 실시간 시세 TR은 FC9(체결), FH9(호가)입니다."
            )
        if not isinstance(tr_key, str) or len(tr_key.strip()) != 8:
            raise ValueError("tr_key(선물 종목코드)는 8자리여야 합니다.")
        if self._socket is None:
            raise WebSocketError("WebSocket 연결 후 구독을 요청하세요.")

    def _send_subscription(self, tr_cd: str, tr_key: str, *, tr_type: str) -> None:
        socket = self._require_socket()
        token = self._tokens.get_token()
        frame = {
            "header": {"token": token.access_token, "tr_type": tr_type},
            "body": {"tr_cd": tr_cd, "tr_key": tr_key.strip()},
        }
        try:
            socket.send(json.dumps(frame, ensure_ascii=False))
        except (websocket.WebSocketException, OSError) as exc:
            raise WebSocketError(
                "LS증권 WebSocket 요청 전송에 실패했습니다 ({}).".format(
                    type(exc).__name__
                )
            ) from exc

    def _require_socket(self) -> Any:
        if self._socket is None:
            raise WebSocketError("WebSocket이 연결되어 있지 않습니다.")
        return self._socket
