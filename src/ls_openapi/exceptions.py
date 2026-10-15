"""ls_openapi 에서 사용하는 예외."""

from __future__ import annotations

from typing import Optional


class LSOpenAPIError(Exception):
    """이 패키지에서 발생하는 모든 예외의 부모 클래스."""


class ConfigError(LSOpenAPIError):
    """앱키/시크릿키 등 설정이 없거나 올바르지 않을 때."""


class AuthError(LSOpenAPIError):
    """접근토큰 발급·폐기에 실패했을 때."""


class APIError(LSOpenAPIError):
    """TR 호출이 HTTP 오류이거나 응답 형식이 올바르지 않을 때."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class WebSocketError(LSOpenAPIError):
    """WebSocket 연결 또는 메시지 처리에 실패했을 때."""
