# Codex에서 로컬 MCP 사용하기

## 가장 쉬운 설치 방법 (Windows)

먼저 PC에 **Python 3.10 이상**, **Codex**, 그리고 LS Open API 앱키·시크릿이 필요합니다.

1. 저장소 페이지에서 **Code → Download ZIP**을 눌러 압축을 풀거나 Git으로 저장소를 받습니다.
2. 압축을 푼 폴더에서 `setup-codex-mcp.cmd`를 더블클릭합니다.
3. 설치가 진행되면 LS 앱키와 앱시크릿을 입력합니다. 입력한 키는 화면에 표시되지 않고, Git에서 제외되는 로컬 `.env` 파일에 저장됩니다.
4. API 주소는 기본값을 그대로 쓰려면 Enter를 누릅니다. 모의투자/실전 키에 맞는 주소인지 확인하세요.
5. 설치가 끝나면 Codex를 완전히 종료한 뒤 다시 엽니다. 새 대화에서 아래처럼 사용해보세요.

```text
A016C000 현재가와 호가를 조회해줘.
```

설치 스크립트가 가상환경 생성, MCP 패키지 설치, Codex 등록을 처리합니다. 내부적으로 Codex CLI의 등록 명령을 실행하지만, **사용자는 설치 후 터미널에서 명령을 입력할 필요가 없습니다.** 서버는 Codex가 요청할 때 PC에서 실행되는 stdio 프로세스이며, 클라우드 서버나 외부 포트를 사용하지 않습니다.

## 제공 도구

- `get_futures_quote(instrument_code)`: 현재가 (`t2111`)
- `get_futures_orderbook(instrument_code)`: 호가 (`t2112`)
- `get_account_balance()`: 잔고·보유 포지션 (`t0441`)
- `get_futures_tick_chart(instrument_code, count, interval, end_date, compressed)`: 틱/분 차트 (`t8464`)

주문·정정·취소 도구는 포함하지 않습니다. 잔고 조회 결과는 Codex 대화에 전달되므로 신뢰할 수 있는 로컬 Codex 환경에서만 연결하세요.

## 문제가 생기면

- `python`이 없거나 버전이 낮다는 메시지: Python 3.10 이상을 설치하고 설치 파일을 다시 실행합니다.
- `codex`를 찾지 못한다는 메시지: Codex를 설치하거나 Codex CLI가 PATH에서 실행되는지 확인합니다.
- API 인증 오류: 저장소의 `.env`에 키와 주소가 맞게 저장됐는지 확인합니다. 모의투자와 실전은 발급한 키에 맞는 설정을 사용하세요.
- Codex에서 도구가 안 보임: Codex를 완전히 종료한 뒤 다시 열고 새 대화를 시작합니다.

직접 설정해야 하는 경우에는 Codex CLI의 `codex mcp add`로 stdio 서버를 등록할 수 있습니다. Codex의 전역 설정 파일은 `~/.codex/config.toml`입니다.
