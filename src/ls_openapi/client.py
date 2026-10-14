"""TR 호출용 HTTP 클라이언트.

공식 TR 명세 JSON의 공통 규칙만 구현합니다 (업종 시세 등 REST API의 공통 헤더/본문 형식).

- 메서드: POST (명세의 기본값)
- 요청 헤더: ``content-type``, ``authorization``, ``tr_cd``, ``tr_cont``, ``tr_cont_key``,
  ``mac_address`` (법인만 필수)
- 요청 본문: ``{"<TR코드>InBlock": {...}}``
- 응답 헤더: ``tr_cd``, ``tr_cont``, ``tr_cont_key`` (연속조회 여부와 키)

이 모듈에는 개별 API(TR 코드, 경로)가 들어 있지 않습니다.
``authorization`` 의 ``Bearer`` 접두사는 토큰 응답의 ``token_type`` 값을 따르며,
실서버로 확인되기 전까지는 미검증 항목입니다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from .auth import DEFAULT_TIMEOUT, TokenManager, _redact
from .config import Settings
from .exceptions import APIError


def build_in_block(tr_cd: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """``{"<tr_cd>InBlock": fields}`` 형태의 요청 본문을 만듭니다."""
    return {"{}InBlock".format(tr_cd): dict(fields)}


@dataclass(frozen=True)
class TRResponse:
    """TR 호출 결과."""

    tr_cd: str
    body: Dict[str, Any]
    tr_cont: str = "N"
    tr_cont_key: str = ""


class LSClient:
    """토큰을 자동으로 붙여 TR 을 호출하는 클라이언트."""

    def __init__(
        self,
        settings: Settings,
        token_manager: Optional[TokenManager] = None,
        session: Optional[Any] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._settings = settings
        self._session = session
        self._timeout = timeout
        self._tokens = token_manager or TokenManager(
            settings, session=session, timeout=timeout
        )

    def post_tr(
        self,
        path: str,
        tr_cd: str,
        body: Dict[str, Any],
        *,
        tr_cont: str = "N",
        tr_cont_key: str = "",
        mac_address: Optional[str] = None,
    ) -> TRResponse:
        """``path`` 로 ``tr_cd`` 거래를 호출합니다.

        ``body`` 는 :func:`build_in_block` 으로 만든 값을 넘기면 됩니다.
        연속조회는 이전 응답의 ``tr_cont``/``tr_cont_key`` 를 그대로 넘깁니다.
        """
        token = self._tokens.get_token()
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": token.authorization_header,
            "tr_cd": tr_cd,
            "tr_cont": tr_cont,
            "tr_cont_key": tr_cont_key,
        }
        if mac_address:
            headers["mac_address"] = mac_address

        post = (self._session or requests).post
        url = self._settings.base_url + path
        try:
            response = post(url, json=body, headers=headers, timeout=self._timeout)
        except requests.RequestException as exc:
            raise APIError(
                "{} 호출에 실패했습니다 (네트워크 오류: {}).".format(
                    tr_cd, type(exc).__name__
                )
            ) from exc

        secrets = (
            self._settings.app_key,
            self._settings.app_secret,
            token.access_token,
        )
        if not 200 <= response.status_code < 300:
            raise APIError(
                "{} 호출이 거절되었습니다 (HTTP {}): {}".format(
                    tr_cd, response.status_code, _redact(response.text, secrets)
                ),
                status_code=response.status_code,
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise APIError(
                "{} 응답이 JSON 형식이 아닙니다.".format(tr_cd),
                status_code=response.status_code,
            ) from exc
        if not isinstance(payload, dict):
            raise APIError(
                "{} 응답이 JSON 객체가 아닙니다.".format(tr_cd),
                status_code=response.status_code,
            )

        return TRResponse(
            tr_cd=tr_cd,
            body=payload,
            tr_cont=response.headers.get("tr_cont", "N"),
            tr_cont_key=response.headers.get("tr_cont_key", ""),
        )
