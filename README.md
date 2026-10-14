# ls-openapi

LS증권 OPEN API를 처음 쓰는 Python 개발자를 위한 비공식 샘플 저장소입니다.
설치 → 인증(접근토큰 발급) → 국내선물 시세 조회까지 따라 할 수 있는 최소 기능 제품(MVP)을 목표로 합니다.

> **현재 상태: 개발 중 (인증 + 선물/옵션 현재가 `t2111` 요청까지 구현)**
> 토큰 발급·폐기는 mock 테스트와 함께 **모의투자 키로 실서버 확인**을 마쳤습니다.
> `t2111` 시세 조회와 TR 공통 호출 클라이언트는 mock 테스트까지만 검증했고 **실서버 확인 전**입니다. 응답 필드 명세는 확인되지 않아 원본 JSON을 그대로 돌려줍니다.

## 안내 사항

- 이 저장소는 LS증권과 무관한 **비공식 개인 샘플**입니다.
- 모든 API 명세의 기준은 [LS증권 OPEN API 공식 포털](https://openapi.ls-sec.co.kr/)입니다. 포털의 내용이 이 저장소와 다르면 포털이 우선합니다.
- 이 저장소는 **조회 기능만** 다룹니다. 주문 기능은 포함하지 않습니다.
- 투자 판단과 그 결과에 대한 책임은 사용자에게 있습니다. 이 코드는 투자 조언이 아닙니다.

## 기능 현황

| 기능 | 상태 |
|---|---|
| 접근토큰 발급 (`POST /oauth2/token`) | 구현됨 (mock 테스트 통과, 모의투자 키로 실서버 확인) |
| 접근토큰 폐기 (`POST /oauth2/revoke`) | 구현됨 (mock 테스트 통과, 모의투자 키로 실서버 확인) |
| TR 공통 호출 클라이언트 (헤더·InBlock·연속조회 값) | 구현됨 (개별 API는 포함하지 않음) |
| 선물/옵션 현재가 조회 (`t2111`) | 요청만 구현됨 (mock 테스트 통과, **실서버 미검증**). 제공받은 호출 샘플 기준이며 응답 필드는 해석하지 않고 원본 JSON을 그대로 반환 |
| 그 밖의 시세 (호가, 멀티 현재가, 종목코드 마스터 등) | **보류** — TR은 공식 목록에서 확인, 경로와 요청·응답 필드 명세 확인 필요 |
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

처음에는 **모의투자 앱키**로 시작하길 권장합니다(실전과 키가 별도로 발급됩니다). 실제 키로 토큰 발급·폐기를 확인하는 방법은 [docs/live-testing.md](docs/live-testing.md)에 있습니다.

## 구조

```
src/ls_openapi/
  config.py        # 환경변수/.env 에서 설정 로딩 (키는 repr 에 노출되지 않음)
  auth.py          # 접근토큰 발급·폐기, 토큰 재사용(TokenManager)
  client.py        # TR 공통 호출 (헤더, InBlock 본문, 연속조회 값)
  futureoption.py  # 선물/옵션 시세 (t2111 현재가)
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
