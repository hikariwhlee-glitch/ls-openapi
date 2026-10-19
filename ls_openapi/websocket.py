"""Minimal LS Securities realtime WebSocket client (requires websocket-client)."""
from __future__ import annotations
import json, os
from typing import Any
from .client import LSOpenAPI
from .catalog import TR_CATALOG

class LSWebSocket:
    def __init__(self, rest: LSOpenAPI, *, url: str | None = None, simulated: bool = False):
        try: import websocket
        except ImportError as exc: raise RuntimeError("Install websocket-client to use realtime feeds") from exc
        self._websocket_module = websocket
        default = "wss://openapi.ls-sec.co.kr:29443/websocket" if simulated else "wss://openapi.ls-sec.co.kr:9443/websocket"
        self.url = url or os.getenv("LS_WS_URL") or default
        self.rest, self.connection = rest, None
    def __enter__(self): return self.connect()
    def __exit__(self, exc_type, exc, tb): self.close()
    def connect(self) -> "LSWebSocket":
        self.connection = self._websocket_module.create_connection(self.url, timeout=self.rest.timeout, header=["Authorization: Bearer " + self.rest.token()])
        return self
    @staticmethod
    def _subscription_type(tr_code: str, *, unsubscribe: bool = False) -> str:
        # LS distinguishes order-event streams from market-data streams.
        order_events = {"C01", "H01", "O01", "C02", "H02", "O02"}
        if tr_code in order_events:
            return "2" if unsubscribe else "1"
        return "4" if unsubscribe else "3"

    def subscribe(self, tr_code: str, key: str = "") -> None:
        if not self.connection: raise RuntimeError("Call connect() first")
        tr = TR_CATALOG.get(tr_code)
        if not tr or tr["protocol"] != "WEBSOCKET": raise ValueError(f"Unknown realtime TR: {tr_code}")
        tr_type = self._subscription_type(tr_code)
        self.connection.send(json.dumps({"header":{"token":self.rest.token(),"tr_type":tr_type},"body":{"tr_cd":tr_code,"tr_key":key}}, ensure_ascii=False))

    def unsubscribe(self, tr_code: str, key: str = "") -> None:
        if not self.connection: raise RuntimeError("Call connect() first")
        tr = TR_CATALOG.get(tr_code)
        if not tr or tr["protocol"] != "WEBSOCKET": raise ValueError(f"Unknown realtime TR: {tr_code}")
        tr_type = self._subscription_type(tr_code, unsubscribe=True)
        self.connection.send(json.dumps({"header":{"token":self.rest.token(),"tr_type":tr_type},"body":{"tr_cd":tr_code,"tr_key":key}}, ensure_ascii=False))
    def recv(self) -> Any:
        if not self.connection: raise RuntimeError("Call connect() first")
        raw = self.connection.recv()
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            # LS realtime market data may arrive as a delimited text frame.
            return raw
    def close(self) -> None:
        if self.connection: self.connection.close(); self.connection = None
