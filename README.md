# ls-openapi

LS증권 OPEN API를 처음 쓰는 Python 개발자를 위한 비공식 샘플 저장소입니다.
설치 → 인증(접근토큰 발급) → 국내선물 시세 조회까지 따라 할 수 있는 최소 기능 제품(MVP)을 목표로 합니다.

> **현재 상태: 개발 중 (인증까지 구현)**
> 인증과 공통 HTTP 클라이언트는 mock 테스트로 검증했지만 **실서버로는 아직 확인하지 않았습니다**.
> 국내선물 시세 조회는 공식 TR 명세를 확인하지 못해 구현하지 않았습니다.

## 안내 사항

- 이 저장소는 LS증권과 무관한 **비공식 개인 샘플**입니다.
- 모든 API 명세의 기준은 [LS증권 OPEN API 공식 포털](https://openapi.ls-sec.co.kr/)입니다. 포털의 내용이 이 저장소와 다르면 포털이 우선합니다.
- 이 저장소는 **조회 기능만** 다룹니다. 주문 기능은 포함하지 않습니다.
- 투자 판단과 그 결과에 대한 책임은 사용자에게 있습니다. 이 코드는 투자 조언이 아닙니다.

## 기능 현황

| 기능 | 상태 |
|---|---|
| 접근토큰 발급 (`POST /oauth2/token`) | 구현됨 (mock 테스트 통과, 실서버 미검증) |
| 접근토큰 폐기 (`POST /oauth2/revoke`) | 구현됨 (mock 테스트 통과, 실서버 미검증) |
| TR 공통 호출 클라이언트 (헤더·InBlock·연속조회 값) | 구현됨 (개별 API는 포함하지 않음) |
| 국내선물 시세 조회 | **보류** — 공식 TR 명세(TR 코드, 경로, 요청·응답 필드) 확인 필요 |
| 주문 | 범위 제외 |

명세 확인 상태의 자세한 내용은 [docs/api-inventory.md](docs/api-inventory.md)에 있습니다.

## 시작하기

```bash
git clone https://github.com/hikariwhlee-glitch/ls-openapi.git
cd ls-openapi
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

cp .env.example .env        # 앱키/시크릿키 입력 (Windows: copy)
python examples/domestic_futureoption/01_issue_token.py
pytest                      # 실제 서버·계정 없이 실행되는 단위 테스트
```

자세한 설명은 [docs/getting-started.md](docs/getting-started.md), 문제가 생기면 [docs/troubleshooting.md](docs/troubleshooting.md)를 보세요.

## 구조

```
src/ls_openapi/
  config.py        # 환경변수/.env 에서 설정 로딩 (키는 repr 에 노출되지 않음)
  auth.py          # 접근토큰 발급·폐기, 토큰 재사용(TokenManager)
  client.py        # TR 공통 호출 (헤더, InBlock 본문, 연속조회 값)
  exceptions.py    # 예외 클래스
examples/domestic_futureoption/   # 독립 실행 예제
docs/                             # 시작하기, API 목록, 문제 해결
tests/                            # mock 응답 기반 단위 테스트
```

## 보안 원칙

- 앱키(App Key)와 앱 시크릿키(App Secret)를 코드나 저장소에 넣지 않습니다.
- 인증정보는 환경변수 또는 로컬 `.env` 파일로만 읽습니다. `.env`는 `.gitignore`에 포함되어 있습니다.
- 오류 메시지와 `repr`에는 앱키, 시크릿키, 토큰 값이 출력되지 않도록 처리했습니다.
- 키가 유출되었다면 LS증권 포털에서 사용해지 후 재등록해야 하며, 이 경우 기존 토큰은 만료됩니다.
- 단위 테스트는 실제 API 서버나 계정 없이 실행됩니다.

## 참고 자료

- [LS증권 OPEN API 포털](https://openapi.ls-sec.co.kr/)
- [시작하기 (공식)](https://openapi.ls-sec.co.kr/howto-use)
