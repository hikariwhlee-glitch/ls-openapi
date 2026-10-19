"""Small reusable REST client for LS Securities OpenAPI."""
from __future__ import annotations
import os
import time
import threading
from typing import Any, Iterator, Mapping
import requests
from .catalog import TR_CATALOG

class LSAPIError(RuntimeError):
    """Raised when LS Securities returns an HTTP/API error."""
    def __init__(self, message: str, *, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code, self.payload = status_code, payload

class LSOpenAPI:
    """REST client. Credentials come from LS_APP_KEY and LS_APP_SECRET."""
    def __init__(self, app_key: str | None = None, app_secret: str | None = None, *, base_url: str | None = None, mac_address: str | None = None, timeout: float = 15, allow_orders: bool = False):
        self.app_key = app_key or os.getenv("LS_APP_KEY")
        self.app_secret = app_secret or os.getenv("LS_APP_SECRET")
        if not self.app_key or not self.app_secret:
            raise ValueError("Set LS_APP_KEY and LS_APP_SECRET first.")
        self.base_url = (base_url or os.getenv("LS_BASE_URL") or "https://openapi.ls-sec.co.kr:8080").rstrip("/")
        self.mac_address = mac_address or os.getenv("LS_MAC_ADDRESS", "")
        self.timeout, self.allow_orders = timeout, allow_orders
        self.session = requests.Session()
        self._token: str | None = None
        self._token_expires = 0.0
        self._last_call: dict[str, float] = {}
        self._rate_lock = threading.Lock()

    def token(self) -> str:
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        response = self.session.post(self.base_url + "/oauth2/token", data={"grant_type":"client_credentials", "appkey":self.app_key, "appsecretkey":self.app_secret, "scope":"oob"}, headers={"content-type":"application/x-www-form-urlencoded"}, timeout=self.timeout)
        data = self._json(response)
        token = data.get("access_token")
        if not token:
            raise LSAPIError("Token response did not include access_token", status_code=response.status_code, payload=data)
        self._token = token
        self._token_expires = time.time() + int(data.get("expires_in", data.get("expire_in", 3600)))
        return token

    @staticmethod
    def _json(
        response: requests.Response, *, accepted_codes: tuple[str, ...] = ()
    ) -> dict[str, Any]:
        try: data = response.json()
        except ValueError: data = {"raw": response.text}
        if not response.ok:
            raise LSAPIError(f"LS API HTTP {response.status_code}: {data}", status_code=response.status_code, payload=data)
        if isinstance(data, dict):
            code = str(data.get("rsp_cd", ""))
            accepted = ("00000", "0", "OK", *accepted_codes)
            if code and code not in accepted:
                raise LSAPIError(f"LS API error {code}: {data.get('rsp_msg', data)}", status_code=response.status_code, payload=data)
            return data
        return {"data": data}

    def _respect_rate_limit(self, tr_code: str, rate: str) -> None:
        try:
            per_second = float(rate)
        except (TypeError, ValueError):
            return
        if per_second <= 0:
            return
        interval = 1.0 / per_second
        with self._rate_lock:
            now = time.monotonic()
            wait = interval - (now - self._last_call.get(tr_code, 0.0))
            if wait > 0:
                time.sleep(wait)
            self._last_call[tr_code] = time.monotonic()

    def call(self, tr_code: str, params: Mapping[str, Any] | None = None, *, body: Mapping[str, Any] | None = None, continuation_key: str = "", continuation: bool = False) -> dict[str, Any]:
        """Call a REST TR. `body` accepts full block mappings; `params` fills a single input block."""
        tr = TR_CATALOG.get(tr_code)
        if not tr:
            raise ValueError(f"Unknown TR code: {tr_code}")
        if tr["protocol"] != "REST":
            raise ValueError(f"{tr_code} is not a REST transaction")
        if tr["is_order"] and not self.allow_orders:
            raise PermissionError(f"{tr_code} is an order-related TR; construct with allow_orders=True to enable")
        if body is not None and params is not None:
            raise ValueError("Pass either params or body, not both")
        if body is None:
            blocks = tr["request_blocks"]
            if len(blocks) != 1:
                raise ValueError(f"{tr_code} needs explicit full `body` with blocks: {blocks}")
            body = {blocks[0]: dict(params or {})}
        headers = {"content-type":"application/json; charset=utf-8", "authorization":"Bearer " + self.token(), "tr_cd":tr_code, "tr_cont":"Y" if continuation else "N", "tr_cont_key":continuation_key}
        if self.mac_address: headers["mac_address"] = self.mac_address
        self._respect_rate_limit(tr_code, tr["rate_limit_per_sec"])
        response = self.session.post(self.base_url + tr["path"], json=dict(body), headers=headers, timeout=self.timeout)
        # LS mock futures order APIs report accepted orders with rsp_cd 00039.
        # This code is accepted only for catalog entries explicitly marked as orders.
        accepted_codes = ("00039",) if tr["is_order"] else ()
        data = self._json(response, accepted_codes=accepted_codes)
        data["_continuation"] = {"tr_cont":response.headers.get("tr_cont", "N"), "tr_cont_key":response.headers.get("tr_cont_key", "")}
        return data

    def iter_pages(self, tr_code: str, params: Mapping[str, Any] | None = None, *, body: Mapping[str, Any] | None = None, max_pages: int = 100) -> Iterator[dict[str, Any]]:
        """Yield response pages using LS `tr_cont` and `tr_cont_key` headers."""
        key, more = "", False
        for _ in range(max_pages):
            data = self.call(tr_code, params, body=body, continuation=more, continuation_key=key)
            yield data
            state = data.get("_continuation", {})
            more, key = state.get("tr_cont") == "Y", state.get("tr_cont_key", "")
            if not more: break
