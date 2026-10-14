# ls-openapi

LS증권 OPEN API를 처음 쓰는 Python 개발자를 위한 비공식 샘플 저장소입니다.
설치, 인증, 선물/옵션 시세 조회와 명시적인 주문 요청을 기능별 TR 모듈로 제공합니다.

> **1st MVP 진행 중** — 인증과 `t2111` 시세 조회, 정상주문은 모의투자 실서버에서 확인했습니다. 정정·취소와 추가 시세 TR은 구현 또는 명세 정리 단계이며 실서버 검증 전입니다.

## 안내 사항

- LS증권과 무관한 비공식 개인 샘플입니다.
- API 명세 기준은 [LS증권 OPEN API 공식 포털](https://openapi.ls-sec.co.kr/)입니다.
- 주문 기능은 연결된 계좌에 영향을 줄 수 있습니다. 실행 전 계좌, 종목, 방향, 가격, 수량을 확인하세요.
- 이 코드는 투자 조언이 아닙니다.

## 기능 현황

| 기능 | 상태 |
|---|---|
| 접근토큰 발급·폐기 | 구현 및 모의투자 실서버 확인 |
| 선물/옵션 현재가 조회 (`t2111`) | 구현 및 현재 상장 네 월물 실서버 조회 확인 |
| 선물/옵션 호가 조회 (`t2112`) | 공식 명세 확인, 구현, 실서버 미검증 |
| 지수선물 마스터 (`t8467`) | 공식 명세 확인, 구현, 실서버 미검증 |
| 선물/옵션 정상주문 (`CFOAT00100`) | 구현 및 모의투자 주문 접수 응답 확인 |
| 선물/옵션 정정주문 (`CFOAT00200`) | 사용자 샘플·공식 가이드 기반 구현, 실서버 미검증 |
| 선물/옵션 취소주문 (`CFOAT00300`) | 사용자 샘플·공식 가이드 기반 구현, 실서버 미검증 |
| 잔고 조회 | 현재 브랜치 범위에서 제외 |
| WebSocket 선물 체결·호가 (`FC9`, `FH9`) | 구현 및 모의투자 실서버 검증 대기 (실전은 `--live` 명시 필요) |

`t2111`의 공식 필드 목록은 [응답 필드 문서](docs/t2111-fields.md), 추가 시세 TR은 [시세 문서](docs/market-data.md), 주문은 [주문 문서](docs/orders.md), 전체 명세 현황은 [API 목록](docs/api-inventory.md)을 참고하세요. 코딩 규약은 [docs/coding-conventions.md](docs/coding-conventions.md)입니다.

## 시작하기

```bash
git clone https://github.com/hikariwhlee-glitch/ls-openapi.git
cd ls-openapi
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .

cp .env.example .env        # 앱키/시크릿키 입력 (Windows: copy)
python examples/domestic_futureoption/01_issue_token.py
```

자세한 설명은 [docs/getting-started.md](docs/getting-started.md), 문제 해결은 [docs/troubleshooting.md](docs/troubleshooting.md)를 보세요. 시작 단계에서는 모의투자 앱키 사용을 권장합니다.

## WebSocket 실시간 시세\n\n[사용 가이드](docs/websocket.md)를 참고하세요. `websocket-client` 의존성을 사용하며, 모의투자 연결을 기본값으로 합니다.\n\n```bash\npython examples/domestic_futureoption/04_futures_realtime.py A016C000 A0173000 A0176000 A0179000\n```\n\n실전 서버는 `--live`를 명시해야 접속됩니다. 실시간 시세 수신은 구독이며 주문을 전송하지 않습니다.\n\n## 구조

```
src/ls_openapi/
  auth.py
  client.py
  tr/
    market_data/
      t2111.py      # 현재가
      t2112.py      # 호가
      t8467.py      # 지수선물 마스터\n  websocket.py      # 실시간 FC9/FH9 구독
    orders/
      CFOAT00100.py # 신규 주문
      CFOAT00200.py # 정정
      CFOAT00300.py # 취소
examples/domestic_futureoption/
docs/
```

## 보안

- 앱키, 시크릿키, 토큰을 코드나 저장소에 넣지 않습니다.
- 인증정보는 환경변수 또는 로컬 `.env`에서 읽습니다. `.env`는 `.gitignore`에 포함되어 있습니다.
- 오류 메시지와 객체 표현에 인증정보가 노출되지 않도록 합니다.

## 참고 자료

- [LS증권 OPEN API 포털](https://openapi.ls-sec.co.kr/)
- [시작하기 (공식)](https://openapi.ls-sec.co.kr/howto-use)
