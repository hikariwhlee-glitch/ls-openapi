"""LS증권 OPEN API 비공식 샘플 라이브러리."""

from .auth import AccessToken, TokenManager, issue_token, revoke_token
from .client import LSClient, TRResponse, build_in_block
from .config import DEFAULT_BASE_URL, Settings
from .exceptions import (
    APIError,
    AuthError,
    ConfigError,
    LSOpenAPIError,
)
from .tr.account.CFOAQ50600 import fetch_account_balance
from .tr.market_data.t2111 import fetch_current_price
from .tr.orders.CFOAT00100 import submit_futures_option_order

__version__ = "0.1.0"

__all__ = [
    "APIError",
    "AccessToken",
    "AuthError",
    "ConfigError",
    "DEFAULT_BASE_URL",
    "LSClient",
    "LSOpenAPIError",
    "Settings",
    "TRResponse",
    "TokenManager",
    "build_in_block",
    "fetch_account_balance",
    "fetch_current_price",
    "issue_token",
    "revoke_token",
    "submit_futures_option_order",
]
