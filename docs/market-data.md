# 시세 TR 가이드

공식 LS증권 TR 가이드 JSON 버전 `20261012053652748` 기준입니다. 엔드포인트는 `POST /futureoption/market-data`이며, 원본 응답은 `TRResponse.body`로 반환합니다.

## `t2112` — 선물/옵션 현재가 호가 조회

호출 제한은 초당 10회입니다. 입력 코드 필드는 `shcode`(String, 8자리)입니다.

### 응답 블록 `t2112OutBlock`

| 필드 | 공식 명칭 | 자료형 | 길이 |
|---|---|---:|---:|
| `hname` | 종목명 | String | 20 |
| `price` | 현재가 | Number | 9.2 |
| `sign` | 전일대비구분 | String | 1 |
| `change` | 전일대비 | Number | 9.2 |
| `diff` | 등락율 | Number | 6.2 |
| `volume` | 거래량 | Number | 12 |
| `stimeqrt` | 거래량전일동시간비율 | Number | 6.2 |
| `jnilclose` | 전일종가 | Number | 9.2 |
| `offerho1` | 매도호가1 | Number | 9.2 |
| `bidho1` | 매수호가1 | Number | 9.2 |
| `offerrem1` | 매도호가수량1 | Number | 8 |
| `bidrem1` | 매수호가수량1 | Number | 8 |
| `dcnt1` | 매도호가건수1 | Number | 8 |
| `scnt1` | 매수호가건수1 | Number | 8 |
| `offerho2` | 매도호가2 | Number | 9.2 |
| `bidho2` | 매수호가2 | Number | 9.2 |
| `offerrem2` | 매도호가수량2 | Number | 8 |
| `bidrem2` | 매수호가수량2 | Number | 8 |
| `dcnt2` | 매도호가건수2 | Number | 8 |
| `scnt2` | 매수호가건수2 | Number | 8 |
| `offerho3` | 매도호가3 | Number | 9.2 |
| `bidho3` | 매수호가3 | Number | 9.2 |
| `offerrem3` | 매도호가수량3 | Number | 8 |
| `bidrem3` | 매수호가수량3 | Number | 8 |
| `dcnt3` | 매도호가건수3 | Number | 8 |
| `scnt3` | 매수호가건수3 | Number | 8 |
| `offerho4` | 매도호가4 | Number | 9.2 |
| `bidho4` | 매수호가4 | Number | 9.2 |
| `offerrem4` | 매도호가수량4 | Number | 8 |
| `bidrem4` | 매수호가수량4 | Number | 8 |
| `dcnt4` | 매도호가건수4 | Number | 8 |
| `scnt4` | 매수호가건수4 | Number | 8 |
| `offerho5` | 매도호가5 | Number | 9.2 |
| `bidho5` | 매수호가5 | Number | 9.2 |
| `offerrem5` | 매도호가수량5 | Number | 8 |
| `bidrem5` | 매수호가수량5 | Number | 8 |
| `dcnt5` | 매도호가건수5 | Number | 8 |
| `scnt5` | 매수호가건수5 | Number | 8 |
| `dvol` | 매도호가총수량 | Number | 8 |
| `svol` | 매수호가총수량 | Number | 8 |
| `toffernum` | 총매도호가건수 | Number | 8 |
| `tbidnum` | 총매수호가건수 | Number | 8 |
| `time` | 수신시간 | String | 6 |
| `shcode` | 단축코드 | String | 8 |

`sign` 값은 `1` 상한, `2` 상승, `3` 보합, `4` 하한, `5` 하락입니다. 호가 레벨 1~5는 `offerho`/`bidho` 가격, `offerrem`/`bidrem` 잔량, `dcnt`/`scnt` 건수로 제공됩니다.

## `t8467` — 지수선물 마스터 조회

호출 제한은 초당 2회입니다. 일반 코스피200 지수선물은 `gubun`을 빈 값 또는 `V`, `S`, `Q` 이외 값으로 요청합니다. 공식 설명은 `V`=변동성지수선물, `S`=섹터지수선물, `Q`=코스닥150지수선물, 그 외=코스피200지수선물입니다. 응답은 `t8467OutBlock` 배열이며 종목명·단축코드·확장코드·가격제한 및 기준 가격을 포함합니다.

| 필드 | 공식 명칭 | 자료형 | 길이 |
|---|---|---:|---:|
| `hname` | 종목명 | String | 20 |
| `shcode` | 단축코드 | String | 8 |
| `expcode` | 확장코드 | String | 12 |
| `uplmtprice` | 상한가 | Number | 9.2 |
| `dnlmtprice` | 하한가 | Number | 9.2 |
| `jnilclose` | 전일종가 | Number | 9.2 |
| `jnilhigh` | 전일고가 | Number | 9.2 |
| `jnillow` | 전일저가 | Number | 9.2 |
| `recprice` | 기준가 | Number | 9.2 |

### 사용 예

```python
quote = fetch_orderbook(client, "A016C000")
print(quote.body)

contracts = fetch_index_futures_master(client)
print(contracts.body)
```

이 예시는 이미 인증된 `LSClient`를 사용합니다. 함수들은 서버의 원본 응답을 반환하며 아직 실서버 호출 검증 전입니다.

## 종목코드 선택 참고

- `t2111` 현재가와 `t2112` 호가 요청 필드는 각각 `focode`와 `shcode`이며 둘 다 공식 길이는 8자리입니다. 현재 코드는 대/소문자와 숫자를 포함할 수 있습니다.
- KOSPI200 지수선물 월물 코드는 `t8467` 마스터로 조회하는 방향이 맞습니다. 응답 목록은 실서버에서 아직 확인하지 않았습니다.
- `t8435`는 별도 TR로, 공식 구분값은 `MF` 미니선물, `MO` 미니옵션, `WK` KOSPI200 위클리옵션, `SF` 코스닥150선물, `QW` 코스닥150 위클리옵션입니다. 따라서 일반 KOSPI200 월물 코드 조회용으로 선택하지 않았습니다.
- 이 문서는 공식 스키마를 옮긴 것이며, `t2112`와 `t8467` 실서버 호출 및 응답은 미검증입니다.

