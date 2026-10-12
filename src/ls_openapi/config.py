"""설정 로딩.

앱키/시크릿키는 코드에 쓰지 않고 환경변수 또는 로컬 ``.env`` 파일에서만 읽습니다.
우선순위: 환경변수 > ``.env`` 파일.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Union

from .exceptions import ConfigError

# 공식 TR 명세 JSON(servers)에 명시된 REST 서버 주소
DEFAULT_BASE_URL = "https://openapi.ls-sec.co.kr:8080"

ENV_APP_KEY = "LS_APP_KEY"
ENV_APP_SECRET = "LS_APP_SECRET"
ENV_BASE_URL = "LS_BASE_URL"

_PLACEHOLDER_PREFIX = "YOUR_"


def parse_dotenv(text: str) -> Dict[str, str]:
    """``KEY=VALUE`` 형식의 텍스트를 딕셔너리로 변환합니다.

    빈 줄과 ``#`` 으로 시작하는 줄은 무시하고, ``export `` 접두사와 값 양끝의
    같은 종류 따옴표는 제거합니다. 줄 끝 주석은 지원하지 않습니다.
    """
    values: Dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key:
            values[key] = value
    return values


@dataclass(frozen=True, repr=False)
class Settings:
    """접속에 필요한 설정. ``repr`` 에는 앱키/시크릿키가 노출되지 않습니다."""

    app_key: str
    app_secret: str
    base_url: str = DEFAULT_BASE_URL

    def __repr__(self) -> str:
        return "Settings(app_key='***', app_secret='***', base_url={!r})".format(
            self.base_url
        )

    @classmethod
    def from_env(
        cls,
        dotenv_path: Optional[Union[str, Path]] = ".env",
        environ: Optional[Mapping[str, str]] = None,
    ) -> "Settings":
        """환경변수와 ``.env`` 파일에서 설정을 읽습니다.

        ``os.environ`` 을 수정하지 않습니다. ``dotenv_path`` 가 ``None`` 이거나
        파일이 없으면 환경변수만 사용합니다.
        """
        values: Dict[str, str] = {}
        if dotenv_path is not None:
            path = Path(dotenv_path)
            if path.is_file():
                values.update(parse_dotenv(path.read_text(encoding="utf-8-sig")))

        source = os.environ if environ is None else environ
        for name in (ENV_APP_KEY, ENV_APP_SECRET, ENV_BASE_URL):
            if source.get(name):
                values[name] = source[name]

        required = (ENV_APP_KEY, ENV_APP_SECRET)
        missing: List[str] = [name for name in required if not values.get(name)]
        if missing:
            raise ConfigError(
                "다음 설정이 없습니다: {}. .env.example 을 .env 로 복사해 값을 채우거나 "
                "환경변수로 설정하세요.".format(", ".join(missing))
            )

        placeholders = [
            name for name in required if values[name].startswith(_PLACEHOLDER_PREFIX)
        ]
        if placeholders:
            raise ConfigError(
                "다음 설정이 예시 값(YOUR_...) 그대로입니다: {}. "
                "발급받은 실제 값으로 바꿔 주세요.".format(", ".join(placeholders))
            )

        base_url = values.get(ENV_BASE_URL) or DEFAULT_BASE_URL
        if not base_url.startswith(("https://", "http://")):
            raise ConfigError(
                "{} 는 http:// 또는 https:// 로 시작해야 합니다.".format(ENV_BASE_URL)
            )

        return cls(
            app_key=values[ENV_APP_KEY],
            app_secret=values[ENV_APP_SECRET],
            base_url=base_url.rstrip("/"),
        )
