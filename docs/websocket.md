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

공식 구독 필드: `tr_cd`(String, 3), `tr_key`(String, 8; 명세 설명은 단축코드 6자리 또는 8자리 허용). 프로젝트 구현은 현재 확인된 KOSPI200 월물 8자리 코드를 받습니다.

## FC9 — KOSPI200 선물 체결

응답 필드는 공식 명세상 모두 String입니다.

| 필드 | 공식 명칭 | 길이 |
|---|---|---:|
| `chetime` | 체결시간 | 6 |
| `sign` | 전일대비구분 | 1 |
| `change` | 전일대비 | 9.2 |
| `drate` | 등락율 | 6.2 |
| `price` | 현재가 | 9.2 |
| `open` | 시가 | 9.2 |
| `high` | 고가 | 9.2 |
| `low` | 저가 | 9.2 |
| `cgubun` | 체결구분 | 1 |
| `cvolume` | 체결량 | 6 |
| `volume` | 누적거래량 | 12 |
| `value` | 누적거래대금 | 12 |
| `mdvolume` | 매도누적체결량 | 12 |
| `mdchecnt` | 매도누적체결건수 | 8 |
| `msvolume` | 매수누적체결량 | 12 |
| `mschecnt` | 매수누적체결건수 | 8 |
| `cpower` | 체결강도 | 9.2 |
| `offerho1` | 매도호가1 | 9.2 |
| `bidho1` | 매수호가1 | 9.2 |
| `openyak` | 미결제약정수량 | 8 |
| `k200jisu` | KOSPI200지수 | 9.2 |
| `theoryprice` | 이론가 | 9.2 |
| `kasis` | 괴리율 | 6.2 |
| `sbasis` | 시장BASIS | 9.2 |
| `ibasis` | 이론BASIS | 9.2 |
| `openyakcha` | 미결제약정증감 | 8 |
| `jgubun` | 장운영정보 | 2 |
| `jnilvolume` | 전일동시간대거래량 | 12 |
| `futcode` | 단축코드 | 8 |

## FH9 — KOSPI200 선물 호가

응답 필드는 공식 명세상 모두 String입니다.

| 필드 | 공식 명칭 | 길이 |
|---|---|---:|
| `hotime` | 호가시간 | 6 |
| `offerho1` | 매도호가1 | 9.2 |
| `bidho1` | 매수호가1 | 9.2 |
| `offerrem1` | 매도호가수량1 | 6 |
| `bidrem1` | 매수호가수량1 | 6 |
| `offercnt1` | 매도호가건수1 | 5 |
| `bidcnt1` | 매수호가건수1 | 5 |
| `offerho2` | 매도호가2 | 9.2 |
| `bidho2` | 매수호가2 | 9.2 |
| `offerrem2` | 매도호가수량2 | 6 |
| `bidrem2` | 매수호가수량2 | 6 |
| `offercnt2` | 매도호가건수2 | 5 |
| `bidcnt2` | 매수호가건수2 | 5 |
| `offerho3` | 매도호가3 | 9.2 |
| `bidho3` | 매수호가3 | 9.2 |
| `offerrem3` | 매도호가수량3 | 6 |
| `bidrem3` | 매수호가수량3 | 6 |
| `offercnt3` | 매도호가건수3 | 5 |
| `bidcnt3` | 매수호가건수3 | 5 |
| `offerho4` | 매도호가4 | 9.2 |
| `bidho4` | 매수호가4 | 9.2 |
| `offerrem4` | 매도호가수량4 | 6 |
| `bidrem4` | 매수호가수량4 | 6 |
| `offercnt4` | 매도호가건수4 | 5 |
| `bidcnt4` | 매수호가건수4 | 5 |
| `offerho5` | 매도호가5 | 9.2 |
| `bidho5` | 매수호가5 | 9.2 |
| `offerrem5` | 매도호가수량5 | 6 |
| `bidrem5` | 매수호가수량5 | 6 |
| `offercnt5` | 매도호가건수5 | 5 |
| `bidcnt5` | 매수호가건수5 | 5 |
| `totofferrem` | 매도호가총수량 | 6 |
| `totbidrem` | 매수호가총수량 | 6 |
| `totoffercnt` | 매도호가총건수 | 5 |
| `totbidcnt` | 매수호가총건수 | 5 |
| `futcode` | 단축코드 | 8 |
| `danhochk` | 단일가호가여부 | 1 |
| `alloc_gubun` | 배분적용구분 | 1 |

## Python 예제

저장소 루트에서 모의투자로 연결합니다. 여러 월물을 지정하면 각 종목의 FC9와 FH9를 등록합니다. 실행 중 수신되는 구독 응답과 실시간 메시지를 JSON으로 출력합니다.

```bash
python examples/domestic_futureoption/04_futures_realtime.py A016C000 A0173000 A0176000 A0179000
```

실전 서버는 별도 명시해야 합니다.

```bash
python examples/domestic_futureoption/04_futures_realtime.py --live A016C000
```

`LSWebSocketClient`는 동기식이며 Ctrl+C 또는 종료 시 구독 해제(`tr_type=4`)를 보낸 뒤 소켓을 닫습니다. WebSocket 토큰을 발급받은 뒤 폐기합니다. 모의투자·실전 구독 및 데이터 수신은 아직 검증하지 않았습니다.

