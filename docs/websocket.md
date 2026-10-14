# 선물 실시간 시세 (WebSocket)

기준 자료: LS증권 공식 TR 가이드 JSON 버전 `20261012053652748` 및 [공식 시작하기 가이드](https://openapi.ls-sec.co.kr/howto-use). 이 구현은 KOSPI200 선물 체결 `FC9`와 호가 `FH9`를 지원합니다. 주문·계좌 이벤트 구독은 범위에 넣지 않았습니다.

## 접속과 구독 프레임

| 환경 | 주소 |
|---|---|
| 모의투자 (기본) | `wss://openapi.ls-sec.co.kr:29443/websocket` |
| 실전 | `wss://openapi.ls-sec.co.kr:9443/websocket` |

연결 후 구독 요청은 다음 JSON 구조입니다. `tr_type=3`은 등록, `tr_type=4`는 해제입니다. 토큰은 REST 헤더와 달리 JSON `header.token`에 전달합니다.

```json
{
  "header": {"token": "<access_token>", "tr_type": "3"},
  "body": {"tr_cd": "FC9", "tr_key": "A016C000"}
}
```

공식 구독 필드: `tr_cd`(String, 3), `tr_key`(String, 최대 8). 가이드는 단축코드 6자리 또는 8자리를 허용하며, 이 프로젝트의 KOSPI200 월물 예제는 사용자가 검증한 8자리 코드를 사용합니다.

## FC9 — KOSPI200 선물 체결

응답 필드는 문자열입니다.

| 필드 | 공식 명칭 | 길이 |
|---|---|---:|

## FH9 — KOSPI200 선물 호가

응답 필드는 문자열입니다.

| 필드 | 공식 명칭 | 길이 |
|---|---|---:|

## Python 예제

저장소 루트에서 모의투자로 연결합니다. 여러 월물을 지정하면 각 종목의 FC9와 FH9를 등록합니다. 실행 중 수신되는 구독 응답과 실시간 메시지를 JSON으로 출력합니다.

```bash
python examples/domestic_futureoption/04_futures_realtime.py A016C000 A0173000 A0176000 A0179000
```

실전 서버는 별도 명시해야 합니다.

```bash
python examples/domestic_futureoption/04_futures_realtime.py --live A016C000
```

`LSWebSocketClient`는 동기식이며 Ctrl+C 또는 종료 시 구독 해제(`tr_type=4`)를 보낸 뒤 소켓을 닫습니다. WebSocket 토큰을 발급받은 뒤 폐기합니다. 실전 구독·데이터 수신은 아직 검증하지 않았습니다. 내일 모의투자에서 먼저 연결 확인이 필요합니다.

