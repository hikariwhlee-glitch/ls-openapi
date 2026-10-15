# `t2111` 선물/옵션 현재가 응답 필드

공식 가이드 JSON 버전 `20261012053652748`의 `t2111OutBlock` 스키마를 옮겼습니다. 설명은 공식 명칭을 한국어로 그대로 기록했습니다. 숫자 자릿수 표기는 공식 JSON의 `length` 값입니다. `Number` 값의 소수점 여부는 길이 표기(예: `9.2`)를 따릅니다.

요청 블록은 `t2111InBlock.focode`(String, 8자리)이며, 8자리가 아닌 코드는 응답 오류 없이 비어 있는 시세를 돌려줄 수 있어 라이브러리 입력 단계에서 거부합니다.

| 필드 | 공식 명칭 | 자료형 | 길이 | 설명 |
|---|---|---:|---:|---|
| `hname` | 한글명 | String | 20 |  |
| `price` | 현재가 | Number | 9.2 |  |
| `sign` | 전일대비구분 | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `change` | 전일대비 | Number | 9.2 |  |
| `jnilclose` | 전일종가 | Number | 9.2 |  |
| `diff` | 등락율 | Number | 6.2 |  |
| `volume` | 거래량 | Number | 12 |  |
| `value` | 거래대금 | Number | 12 |  |
| `mgjv` | 미결제량 | Number | 8 |  |
| `mgjvdiff` | 미결제증감 | Number | 8 |  |
| `open` | 시가 | Number | 9.2 |  |
| `high` | 고가 | Number | 9.2 |  |
| `low` | 저가 | Number | 9.2 |  |
| `uplmtprice` | 상한가 | Number | 9.2 |  |
| `dnlmtprice` | 하한가 | Number | 9.2 |  |
| `high52w` | 52최고가 | Number | 9.2 |  |
| `low52w` | 52최저가 | Number | 9.2 |  |
| `basis` | 베이시스 | Number | 9.2 |  |
| `recprice` | 기준가 | Number | 9.2 |  |
| `theoryprice` | 이론가 | Number | 9.2 |  |
| `glyl` | 괴리율 | Number | 6.3 |  |
| `cbhprice` | CB상한가 | Number | 9.2 |  |
| `cblprice` | CB하한가 | Number | 9.2 |  |
| `lastmonth` | 만기일 | String | 8 |  |
| `jandatecnt` | 잔여일 | Number | 8 |  |
| `pricejisu` | 종합지수 | Number | 9.2 |  |
| `jisusign` | 종합지수전일대비구분 | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `jisuchange` | 종합지수전일대비 | Number | 9.2 |  |
| `jisudiff` | 종합지수등락율 | Number | 6.2 |  |
| `kospijisu` | KOSPI200지수 | Number | 9.2 |  |
| `kospisign` | KOSPI200전일대비구분 | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `kospichange` | KOSPI200전일대비 | Number | 9.2 |  |
| `kospidiff` | KOSPI200등락율 | Number | 6.2 |  |
| `listhprice` | 상장최고가 | Number | 9.2 |  |
| `listlprice` | 상장최저가 | Number | 9.2 |  |
| `delt` | 델타 | Number | 6.4 |  |
| `gama` | 감마 | Number | 6.4 |  |
| `ceta` | 세타 | Number | 6.4 |  |
| `vega` | 베가 | Number | 6.4 |  |
| `rhox` | 로우 | Number | 6.4 |  |
| `gmprice` | 근월물현재가 | Number | 9.2 |  |
| `gmsign` | 근월물전일대비구분 | String | 1 |  |
| `gmchange` | 근월물전일대비 | Number | 9.2 |  |
| `gmdiff` | 근월물등락율 | Number | 6.2 |  |
| `theorypriceg` | 이론가 | Number | 9.2 |  |
| `histimpv` | 역사적변동성 | Number | 6.2 |  |
| `impv` | 내재변동성 | Number | 6.2 |  |
| `sbasis` | 시장BASIS | Number | 9.2 |  |
| `ibasis` | 이론BASIS | Number | 9.2 |  |
| `gmfutcode` | 근월물종목코드 | String | 8 |  |
| `actprice` | 행사가 | Number | 6.2 |  |
| `greeks_time` | 거래소민감도수신시간 | String | 6 |  |
| `greeks_confirm` | 거래소민감도확정여부 | String | 8 |  |
| `danhochk` | 단일가호가여부 | String | 1 |  |
| `yeprice` | 예상체결가 | Number | 9.2 |  |
| `jnilysign` | 예상체결가전일종가대비구분 | String | 1 |  |
| `jnilychange` | 예상체결가전일종가대비 | Number | 9.2 |  |
| `jnilydrate` | 예상체결가전일종가등락율 | Number | 6.2 |  |
| `alloc_gubun` | 배분구분(1:배분개시2:배분해제0:미발생) | String | 1 |  |
| `bjandatecnt` | 잔여일(영업일) | Number | 8 |  |
| `focode` | 종목코드 | String | 8 |  |
| `dy_gubun` | 실시간가격제한여부(0:대상아님1:적용중2:미적용중3:일시해제) | String | 1 |  |
| `dy_uplmtprice` | 실시간상한가 | Number | 9.2 |  |
| `dy_dnlmtprice` | 실시간하한가 | Number | 9.2 |  |
| `updnstep_gubun` | 가격제한폭확대(0:미확대1:확대2:대상아님) | String | 1 |  |
| `upstep` | 상한적용단계 | String | 2 |  |
| `dnstep` | 하한적용단계 | String | 2 |  |
| `uplmtprice_3rd` | 3단계상한가 | Number | 9.2 |  |
| `dnlmtprice_3rd` | 3단계하한가 | Number | 9.2 |  |
| `expct_ccls_q` | 예상체결수량 | Number | 9 |  |

