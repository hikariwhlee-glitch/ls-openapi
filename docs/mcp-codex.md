# Codex에서 로컬 MCP 서버 사용하기

이 서버는 Codex가 필요할 때 사용자 PC에서 프로세스로 실행하는 **stdio MCP 서버**입니다. 클라우드 서버나 외부 포트는 열지 않습니다.

## 제공하는 도구

- `get_futures_quote(instrument_code)`: 선물·옵션 현재가 (`t2111`)
- `get_futures_orderbook(instrument_code)`: 선물·옵션 호가 (`t2112`)
- `get_account_balance()`: 계좌 잔고·보유 포지션 (`t0441`)
- `get_futures_tick_chart(instrument_code, count, interval, end_date, compressed)`: 틱/분 차트 (`t8464`)

주문, 정정, 취소 도구는 노출하지 않습니다. 계좌 잔고 도구의 결과는 Codex에 전달되므로 신뢰할 수 있는 로컬 Codex 환경에서만 연결하세요.

## 1. 설치

저장소 루트에서 PowerShell을 열고 실행합니다.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[mcp]"
Copy-Item .env.example .env
```

저장소 루트의 `.env`에 모의투자 또는 실계좌 API 키를 입력합니다.

```dotenv
LS_APP_KEY=발급받은_앱키
LS_APP_SECRET=발급받은_앱시크릿
LS_BASE_URL=https://openapi.ls-sec.co.kr:8080
```

`.env`는 Git에서 제외됩니다. 키를 저장소에 커밋하거나 Codex 설정 파일에 직접 적지 마세요. 모의/실전 키와 API 주소를 올바르게 짝지어 설정하세요.

## 2. Codex 설정

Codex CLI의 `~/.codex/config.toml`에 아래 항목을 추가합니다. Windows에서는 보통 `C:\Users\<사용자명>\.codex\config.toml`입니다. `cwd`와 `command`는 실제 저장소 경로에 맞게 바꿉니다.

```toml
[mcp_servers.ls_openapi]
command = "C:\\path\\to\\ls-openapi\\.venv\\Scripts\\python.exe"
args = ["-m", "ls_openapi.mcp_server"]
cwd = "C:\\path\\to\\ls-openapi"
startup_timeout_sec = 20
```

설정을 저장한 뒤 Codex를 다시 시작하거나 MCP 서버를 새로고침합니다. Codex CLI를 쓴다면 `codex mcp list`에서 `ls_openapi`가 등록됐는지 확인할 수 있습니다. MCP 도구 목록에서 위 4개 도구가 보여야 합니다.

## 3. 호출 예시

Codex에 다음처럼 요청할 수 있습니다.

- “A016C000 현재가와 호가를 조회해줘.”
- “선물옵션 계좌 잔고를 요약해줘.”
- “A016C000의 최근 100개 1분 차트를 가져와줘.”

계좌 조회 결과는 계좌 정보이므로 대화 내용이나 Codex 실행 기록에 포함될 수 있습니다. 이 MCP 서버는 로컬에서 실행되지만, 연결된 클라이언트가 결과를 어떻게 보관하는지는 해당 클라이언트 설정에 따릅니다.

## 문제 해결

- 서버 시작 오류: `cwd`가 저장소 루트인지, 지정한 `command`의 Python에 `pip install -e ".[mcp]"`를 실행했는지 확인합니다.
- API 인증 오류: `.env` 파일 위치와 앱 키/시크릿, `LS_BASE_URL`이 모의투자/실전 환경과 일치하는지 확인합니다.
- Codex가 도구를 찾지 못함: `config.toml`의 경로와 TOML 문법을 확인하고 Codex를 다시 시작합니다.
