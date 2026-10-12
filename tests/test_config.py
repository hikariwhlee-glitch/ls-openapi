from pathlib import Path

import pytest

from ls_openapi import DEFAULT_BASE_URL, ConfigError, Settings
from ls_openapi.config import parse_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_parse_dotenv_handles_comments_quotes_and_export():
    text = """
# 주석
LS_APP_KEY=abc123
export LS_APP_SECRET="quoted-secret"
LS_BASE_URL='https://example.invalid:8080'

잘못된줄
"""
    assert parse_dotenv(text) == {
        "LS_APP_KEY": "abc123",
        "LS_APP_SECRET": "quoted-secret",
        "LS_BASE_URL": "https://example.invalid:8080",
    }


def test_from_env_reads_environment_and_uses_default_base_url():
    env = {"LS_APP_KEY": "k", "LS_APP_SECRET": "s"}
    settings = Settings.from_env(dotenv_path=None, environ=env)
    assert settings.app_key == "k"
    assert settings.app_secret == "s"
    assert settings.base_url == DEFAULT_BASE_URL


def test_from_env_reads_dotenv_file_and_environment_takes_priority(tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("LS_APP_KEY=from-file\nLS_APP_SECRET=file-secret\n", encoding="utf-8")
    env = {"LS_APP_KEY": "from-env"}
    settings = Settings.from_env(dotenv_path=dotenv, environ=env)
    assert settings.app_key == "from-env"
    assert settings.app_secret == "file-secret"


def test_from_env_works_when_dotenv_file_is_missing(tmp_path):
    env = {"LS_APP_KEY": "k", "LS_APP_SECRET": "s"}
    settings = Settings.from_env(dotenv_path=tmp_path / "nope.env", environ=env)
    assert settings.app_key == "k"


def test_missing_values_raise_config_error_naming_variables_only():
    with pytest.raises(ConfigError) as info:
        Settings.from_env(dotenv_path=None, environ={"LS_APP_KEY": "k"})
    message = str(info.value)
    assert "LS_APP_SECRET" in message
    assert "LS_APP_KEY," not in message  # 값이 있는 항목은 목록에 없다


def test_placeholder_values_are_rejected():
    env = {"LS_APP_KEY": "YOUR_APP_KEY", "LS_APP_SECRET": "real-secret"}
    with pytest.raises(ConfigError) as info:
        Settings.from_env(dotenv_path=None, environ=env)
    assert "LS_APP_KEY" in str(info.value)
    assert "real-secret" not in str(info.value)


def test_env_example_template_is_rejected_until_filled_in():
    with pytest.raises(ConfigError):
        Settings.from_env(dotenv_path=REPO_ROOT / ".env.example", environ={})


def test_base_url_trailing_slash_is_stripped_and_scheme_is_checked():
    env = {"LS_APP_KEY": "k", "LS_APP_SECRET": "s", "LS_BASE_URL": "https://example.invalid:8080/"}
    assert Settings.from_env(dotenv_path=None, environ=env).base_url == "https://example.invalid:8080"

    env["LS_BASE_URL"] = "example.invalid"
    with pytest.raises(ConfigError):
        Settings.from_env(dotenv_path=None, environ=env)


def test_repr_does_not_leak_credentials():
    settings = Settings(app_key="super-key", app_secret="super-secret")
    text = repr(settings)
    assert "super-key" not in text
    assert "super-secret" not in text
