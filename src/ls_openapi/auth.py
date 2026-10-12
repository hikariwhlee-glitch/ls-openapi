"""접근토큰 발급·폐기.

근거: LS증권 OPEN API 포털 "시작하기"(https://openapi.ls-sec.co.kr/howto-use) 및
공식 TR 명세 JSON(ls-openapi-tr-guides.json, 버전 20261007070834325)의 "OAuth 인증" 항목.

- 발급: ``POST {base_url}/oauth2/token`` (application/x-www-form-urlencoded)
  ``grant_type=client_credentials``, ``appkey``, ``appsecretkey``, ``scope=oob``
- 폐기: ``POST {base_url}/oauth2/revoke`` (application/x-www-form-urlencoded)
  ``appkey``, ``appsecretkey``, ``token_type_hint``, ``token``

공식 자료끼리 어긋나는 부분: 유효기간 필드명이 TR 명세 JSON에서는 ``expire_in``,
"시작하기" 예시 응답에서는 ``expires_in`` 입니다. 실서버 응답으로 확인되기 전까지
두 이름을 모두 허용합니다.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Optional

import requests

from .config import Settings
from .exceptions import AuthError

TOKEN_PATH = "/oauth2/token"
REVOKE_PATH = "/oauth2/revoke"
DEFAULT_TIMEOUT = 10.0
_FORM_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


def _redact(text: str, secrets: Iterable[str], limit: int = 200) -> str:
    """오류 메시지에 비밀값이 섞여 나가지 않도록 가리고 길이를 제한합니다."""
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text[:limit]


def _parse_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class AccessToken:
    """발급된 접근토큰. ``repr`` 에는 토큰 값이 노출되지 않습니다."""

    access_token: str = field(repr=False)
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    issued_at: float = 0.0

    @property
    def expires_at(self) -> Optional[float]:
        if self.expires_in is None:
            return None
        return self.issued_at + self.expires_in

    def is_expired(self, margin: float = 60.0, now: Optional[float] = None) -> bool:
        """만료 ``margin`` 초 전부터 만료로 봅니다. 유효기간을 모르면 만료로 보지 않습니다."""
        if self.expires_at is None:
            return False
        current = time.time() if now is None else now
        return current >= self.expires_at - margin

    @property
    def authorization_header(self) -> str:
        return "{} {}".format(self.token_type or "Bearer", self.access_token)


def issue_token(
    settings: Settings,
    session: Optional[Any] = None,
    timeout: float = DEFAULT_TIMEOUT,
    clock: Callable[[], float] = time.time,
) -> AccessToken:
    """접근토큰을 발급받습니다."""
    post = (session or requests).post
    url = settings.base_url + TOKEN_PATH
    data = {
        "grant_type": "client_credentials",
        "appkey": settings.app_key,
        "appsecretkey": settings.app_secret,
        "scope": "oob",
    }
    try:
        response = post(url, data=data, headers=_FORM_HEADERS, timeout=timeout)
    except requests.RequestException as exc:
        raise AuthError(
            "토큰 발급 요청에 실패했습니다 (네트워크 오류: {}).".format(type(exc).__name__)
        ) from exc

    secrets = (settings.app_key, settings.app_secret)
    if not 200 <= response.status_code < 300:
        raise AuthError(
            "토큰 발급이 거절되었습니다 (HTTP {}): {}".format(
                response.status_code, _redact(response.text, secrets)
            )
        )
    try:
        payload = response.json()
    except ValueError as exc:
        raise AuthError("토큰 응답이 JSON 형식이 아닙니다.") from exc
    if not isinstance(payload, dict) or not payload.get("access_token"):
        raise AuthError("토큰 응답에 access_token 이 없습니다.")

    expires_in = _parse_int(payload.get("expires_in", payload.get("expire_in")))
    return AccessToken(
        access_token=str(payload["access_token"]),
        token_type=str(payload.get("token_type") or "Bearer"),
        expires_in=expires_in,
        scope=payload.get("scope"),
        issued_at=clock(),
    )


def revoke_token(
    settings: Settings,
    token: str,
    session: Optional[Any] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """접근토큰을 폐기합니다. 서버가 돌려준 JSON(``code``, ``message``)을 그대로 반환합니다.

    응답의 성공 코드 값은 공식 명세에 나와 있지 않아 해석하지 않습니다.
    """
    post = (session or requests).post
    url = settings.base_url + REVOKE_PATH
    data = {
        "appkey": settings.app_key,
        "appsecretkey": settings.app_secret,
        "token_type_hint": "access_token",
        "token": token,
    }
    try:
        response = post(url, data=data, headers=_FORM_HEADERS, timeout=timeout)
    except requests.RequestException as exc:
        raise AuthError(
            "토큰 폐기 요청에 실패했습니다 (네트워크 오류: {}).".format(type(exc).__name__)
        ) from exc

    secrets = (settings.app_key, settings.app_secret, token)
    if not 200 <= response.status_code < 300:
        raise AuthError(
            "토큰 폐기가 거절되었습니다 (HTTP {}): {}".format(
                response.status_code, _redact(response.text, secrets)
            )
        )
    try:
        payload = response.json()
    except ValueError as exc:
        raise AuthError("토큰 폐기 응답이 JSON 형식이 아닙니다.") from exc
    return payload if isinstance(payload, dict) else {}


class TokenManager:
    """토큰을 한 번 발급받아 재사용하고, 만료가 가까워지면 다시 발급합니다."""

    def __init__(
        self,
        settings: Settings,
        session: Optional[Any] = None,
        timeout: float = DEFAULT_TIMEOUT,
        refresh_margin: float = 60.0,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._settings = settings
        self._session = session
        self._timeout = timeout
        self._refresh_margin = refresh_margin
        self._clock = clock
        self._token: Optional[AccessToken] = None

    def get_token(self) -> AccessToken:
        if self._token is None or self._token.is_expired(
            margin=self._refresh_margin, now=self._clock()
        ):
            self._token = issue_token(
                self._settings,
                session=self._session,
                timeout=self._timeout,
                clock=self._clock,
            )
        return self._token

    def invalidate(self) -> None:
        """저장된 토큰을 버립니다. 다음 ``get_token()`` 에서 새로 발급합니다."""
        self._token = None

    def revoke(self) -> Optional[Dict[str, Any]]:
        """저장된 토큰이 있으면 폐기하고, 서버 응답을 반환합니다."""
        if self._token is None:
            return None
        result = revoke_token(
            self._settings,
            self._token.access_token,
            session=self._session,
            timeout=self._timeout,
        )
        self._token = None
        return result
