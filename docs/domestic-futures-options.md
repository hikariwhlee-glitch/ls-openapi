# 국내 선물·옵션 API 명세

- 공식 가이드 버전: `20261012053652748`
- 생성 시각(UTC): `2026-10-15T05:45:12+00:00`
- API 그룹: 7개
- TR: 91개
- 서버: `[{"protocol": "REST", "url": "https://openapi.ls-sec.co.kr:8080", "contentType": "application/json; charset=UTF-8"}, {"protocol": "WEBSOCKET", "url": "wss://openapi.ls-sec.co.kr:9443", "simulationUrl": "wss://openapi.ls-sec.co.kr:29443", "contentType": "application/json; charset=UTF-8"}]`
- 전역 기본값: `{"method": "POST", "fieldRequired": true}`
- 원본: [https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true](https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true)

> 공식 가이드 JSON에서 국내 `선물/옵션` 카테고리 전체를 추출했습니다. JSON 스냅샷에는 선택된 API의 전체 구조를 보존합니다.

## [선물/옵션] 계좌

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/accno`
- 설명: 주간/야간 선물옵션 계좌별 거래내역 및 잔고 등 계좌에 관련된 서비스를 확인할 수 있습니다.

### CFOAQ00600 — 선물옵션 계좌 주문체결내역 조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ00600InBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ00600InBlock1.QrySrtDt` | String | 8 |  |
| `CFOAQ00600InBlock1.QryEndDt` | String | 8 |  |
| `CFOAQ00600InBlock1.FnoClssCode` | String | 2 | 00@전체<br>11@선물<br>12@옵션 |
| `CFOAQ00600InBlock1.PrdgrpCode` | String | 2 | 00:전체<br>01:주가지수<br>02:개별주식<br>03:가공채권<br>04:통화<br>05:상품<br>06:금리 |
| `CFOAQ00600InBlock1.PrdtExecTpCode` | String | 1 | 0:전체<br>1:체결<br>2:미체결 |
| `CFOAQ00600InBlock1.StnlnSeqTp` | String | 1 | 3:역순<br>4:정순 |
| `CFOAQ00600InBlock1.CommdaCode` | String | 2 | 99 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ00600OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ00600OutBlock1.AcntNo` | String | 20 |  |
| `CFOAQ00600OutBlock1.InptPwd` | String | 8 |  |
| `CFOAQ00600OutBlock1.QrySrtDt` | String | 8 |  |
| `CFOAQ00600OutBlock1.QryEndDt` | String | 8 |  |
| `CFOAQ00600OutBlock1.FnoClssCode` | String | 2 |  |
| `CFOAQ00600OutBlock1.PrdgrpCode` | String | 2 |  |
| `CFOAQ00600OutBlock1.PrdtExecTpCode` | String | 1 |  |
| `CFOAQ00600OutBlock1.StnlnSeqTp` | String | 1 |  |
| `CFOAQ00600OutBlock1.CommdaCode` | String | 2 |  |
| `CFOAQ00600OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAQ00600OutBlock2.AcntNm` | String | 40 |  |
| `CFOAQ00600OutBlock2.FutsOrdQty` | Number | 16 |  |
| `CFOAQ00600OutBlock2.FutsExecQty` | Number | 16 |  |
| `CFOAQ00600OutBlock2.OptOrdQty` | Number | 16 |  |
| `CFOAQ00600OutBlock2.OptExecQty` | Number | 16 |  |
| `CFOAQ00600OutBlock3.OrdDt` | String | 8 |  |
| `CFOAQ00600OutBlock3.OrdNo` | Number | 10 |  |
| `CFOAQ00600OutBlock3.OrgOrdNo` | Number | 10 |  |
| `CFOAQ00600OutBlock3.OrdTime` | String | 9 |  |
| `CFOAQ00600OutBlock3.FnoIsuNo` | String | 12 |  |
| `CFOAQ00600OutBlock3.IsuNm` | String | 40 |  |
| `CFOAQ00600OutBlock3.BnsTpNm` | String | 10 |  |
| `CFOAQ00600OutBlock3.MrcTpNm` | String | 10 |  |
| `CFOAQ00600OutBlock3.FnoOrdprcPtnCode` | String | 2 |  |
| `CFOAQ00600OutBlock3.FnoOrdprcPtnNm` | String | 40 |  |
| `CFOAQ00600OutBlock3.OrdPrc` | Number | 13.2 |  |
| `CFOAQ00600OutBlock3.OrdQty` | Number | 16 |  |
| `CFOAQ00600OutBlock3.OrdTpNm` | String | 10 |  |
| `CFOAQ00600OutBlock3.ExecTpNm` | String | 10 |  |
| `CFOAQ00600OutBlock3.ExecPrc` | Number | 13.2 |  |
| `CFOAQ00600OutBlock3.ExecQty` | Number | 16 |  |
| `CFOAQ00600OutBlock3.CtrctTime` | String | 9 |  |
| `CFOAQ00600OutBlock3.CtrctNo` | Number | 10 |  |
| `CFOAQ00600OutBlock3.ExecNo` | Number | 10 |  |
| `CFOAQ00600OutBlock3.BnsplAmt` | Number | 16 |  |
| `CFOAQ00600OutBlock3.UnercQty` | Number | 16 |  |
| `CFOAQ00600OutBlock3.UserId` | String | 16 |  |
| `CFOAQ00600OutBlock3.CommdaCode` | String | 2 |  |
| `CFOAQ00600OutBlock3.CommdaCodeNm` | String | 40 |  |

### CFOAQ50600 — 선물옵션 계좌잔고 및 평가현황3

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ50600InBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ50600InBlock1.OrdDt` | String | 8 |  |
| `CFOAQ50600InBlock1.BalEvalTp` | String | 1 | 0@기본설정<br>1@이동평균법<br>2@선입선출법 |
| `CFOAQ50600InBlock1.FutsPrcEvalTp` | String | 1 | 1@당초가<br>2@전일종가 |
| `CFOAQ50600InBlock1.LqdtQtyQryTp` | String | 1 | 1@청산수량산출 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ50600OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ50600OutBlock1.LqdtQtyQryTp` | String | 1 |  |
| `CFOAQ50600OutBlock1.FutsPrcEvalTp` | String | 1 |  |
| `CFOAQ50600OutBlock1.BalEvalTp` | String | 1 |  |
| `CFOAQ50600OutBlock1.OrdDt` | String | 8 |  |
| `CFOAQ50600OutBlock1.InptPwd` | String | 8 |  |
| `CFOAQ50600OutBlock1.AcntNo` | String | 20 |  |
| `CFOAQ50600OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAQ50600OutBlock2.EvalRat` | String | 7.2 |  |
| `CFOAQ50600OutBlock2.BaseEvalAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.NetPnlAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.TotPnlAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.OptBnsAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.FutsAdjstDfamt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.OptBnsplAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.OptEvalAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.OptEvalPnlAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.FutsEvalPnlAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.RcvblOdpnt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.RcvblAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.CmsnAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.MnyAddMgn` | Number | 16 |  |
| `CFOAQ50600OutBlock2.AddMgnTotamt` | Number | 15 |  |
| `CFOAQ50600OutBlock2.MnyMaintMgn` | Number | 16 |  |
| `CFOAQ50600OutBlock2.MtmgnTotamt` | Number | 15 |  |
| `CFOAQ50600OutBlock2.MnyCsgnMgn` | Number | 16 |  |
| `CFOAQ50600OutBlock2.CsgnMgnTotamt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.OrdAbleTotAmt` | Number | 15 |  |
| `CFOAQ50600OutBlock2.PsnOutAbleSubstAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.PsnOutAbleCurAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.PsnOutAbleTotAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.FcurrSubstAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.DpstgSubst` | Number | 16 |  |
| `CFOAQ50600OutBlock2.DpstgMny` | Number | 16 |  |
| `CFOAQ50600OutBlock2.DpsamtTotamt` | Number | 16 |  |
| `CFOAQ50600OutBlock2.MnyEvalDpstgAmt` | Number | 15 |  |
| `CFOAQ50600OutBlock2.EvalDpsamtTotamt` | Number | 15 |  |
| `CFOAQ50600OutBlock2.AcntNm` | String | 40 |  |
| `CFOAQ50600OutBlock2.AcntEvalRat` | String | 7.2 |  |
| `CFOAQ50600OutBlock3.FnoIsuNo` | Number | 12 |  |
| `CFOAQ50600OutBlock3.BnsplAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock3.LqdtAbleQty` | Number | 16 |  |
| `CFOAQ50600OutBlock3.EvalRat` | String | 7.2 |  |
| `CFOAQ50600OutBlock3.EvalPnl` | Number | 16 |  |
| `CFOAQ50600OutBlock3.EvalAmt` | Number | 16 |  |
| `CFOAQ50600OutBlock3.FnoCmpPrc` | String | 27.8 |  |
| `CFOAQ50600OutBlock3.PnlRat` | String | 18.6 |  |
| `CFOAQ50600OutBlock3.FnoNowPrc` | String | 27.8 |  |
| `CFOAQ50600OutBlock3.FnoAvrPrc` | String | 19.8 |  |
| `CFOAQ50600OutBlock3.UnsttQty` | Number | 16 |  |
| `CFOAQ50600OutBlock3.BnsTpNm` | String | 10 |  |
| `CFOAQ50600OutBlock3.BnsTpCode` | String | 1 |  |
| `CFOAQ50600OutBlock3.IsuNm` | String | 40 |  |

### CFOAQ10100 — 선물옵션 주문가능수량조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ10100InBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ10100InBlock1.QryTp` | String | 1 | 1@일반<br>2@금액<br>3@비율 |
| `CFOAQ10100InBlock1.OrdAmt` | Number | 16 |  |
| `CFOAQ10100InBlock1.RatVal` | Number | 19.8 | 0 |
| `CFOAQ10100InBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAQ10100InBlock1.BnsTpCode` | String | 1 | 1@매도<br>2@매수 |
| `CFOAQ10100InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAQ10100InBlock1.FnoOrdprcPtnCode` | String | 2 | 00@지정가<br>03@시장가<br>05@조건부지정가<br>06@최유리지정가 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAQ10100OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAQ10100OutBlock1.AcntNo` | String | 20 |  |
| `CFOAQ10100OutBlock1.Pwd` | String | 8 |  |
| `CFOAQ10100OutBlock1.QryTp` | String | 1 |  |
| `CFOAQ10100OutBlock1.OrdAmt` | Number | 16 |  |
| `CFOAQ10100OutBlock1.RatVal` | Number | 19.8 |  |
| `CFOAQ10100OutBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAQ10100OutBlock1.BnsTpCode` | String | 1 |  |
| `CFOAQ10100OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAQ10100OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CFOAQ10100OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAQ10100OutBlock2.AcntNm` | String | 40 |  |
| `CFOAQ10100OutBlock2.QryDt` | String | 8 |  |
| `CFOAQ10100OutBlock2.FnoNowPrc` | Number | 27.8 |  |
| `CFOAQ10100OutBlock2.OrdAbleQty` | Number | 16 |  |
| `CFOAQ10100OutBlock2.NewOrdAbleQty` | Number | 16 |  |
| `CFOAQ10100OutBlock2.LqdtOrdAbleQty` | Number | 16 |  |
| `CFOAQ10100OutBlock2.UsePreargMgn` | Number | 16 |  |
| `CFOAQ10100OutBlock2.UsePreargMnyMgn` | Number | 16 |  |
| `CFOAQ10100OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOAQ10100OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |

### CFOBQ10500 — 선물옵션 계좌예탁금증거금조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOBQ10500InBlock1.RecCnt` | Number | 5 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOBQ10500OutBlock1.RecCnt` | Number | 5 |  |
| `CFOBQ10500OutBlock1.AcntNo` | String | 20 |  |
| `CFOBQ10500OutBlock1.Pwd` | String | 8 |  |
| `CFOBQ10500OutBlock2.RecCnt` | Number | 5 |  |
| `CFOBQ10500OutBlock2.AcntNm` | String | 40 |  |
| `CFOBQ10500OutBlock2.DpsamtTotamt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.Dps` | Number | 16 |  |
| `CFOBQ10500OutBlock2.SubstAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FilupDpsamtTotamt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FilupDps` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FutsPnlAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.WthdwAbleAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.PsnOutAbleCurAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.PsnOutAbleSubstAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.Mgn` | Number | 16 |  |
| `CFOBQ10500OutBlock2.MnyMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.AddMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock2.MnyAddMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock2.AmtPrdayChckInAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FnoPrdaySubstSellAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FnoCrdaySubstSellAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FnoPrdayFdamt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FnoCrdayFdamt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FcurrSubstAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock2.FnoAcntAfmgnNm` | String | 20 |  |
| `CFOBQ10500OutBlock3.PdGrpCodeNm` | String | 20 |  |
| `CFOBQ10500OutBlock3.NetRiskMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.PrcMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.SprdMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.PrcFlctMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.MinMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.OrdMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.OptNetBuyAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.CsgnMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.MaintMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.FutsBuyExecAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.FutsSellExecAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.OptBuyExecAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.OptSellExecAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.FutsPnlAmt` | Number | 16 |  |
| `CFOBQ10500OutBlock3.TotRiskCsgnMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.UndCsgnMgn` | Number | 16 |  |
| `CFOBQ10500OutBlock3.MgnRdctAmt` | Number | 16 |  |

### CFOEQ11100 — 선물옵션가정산예탁금상세

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOEQ11100InBlock1.RecCnt` | Number | 5 |  |
| `CFOEQ11100InBlock1.BnsDt` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOEQ11100OutBlock1.RecCnt` | Number | 5 |  |
| `CFOEQ11100OutBlock1.AcntNo` | String | 20 |  |
| `CFOEQ11100OutBlock1.Pwd` | String | 8 |  |
| `CFOEQ11100OutBlock1.BnsDt` | String | 8 |  |
| `CFOEQ11100OutBlock2.RecCnt` | Number | 5 |  |
| `CFOEQ11100OutBlock2.AcntNm` | String | 40 |  |
| `CFOEQ11100OutBlock2.OpnmkDpsamtTotamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OpnmkDps` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OpnmkMnyrclAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OpnmkSubstAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.TotAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.Dps` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyrclAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.SubstDsgnAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.CsgnMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyCsgnMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MaintMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyMaintMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyoutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.SubstOutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.AddMgnOcrTpCode` | String | 1 |  |
| `CFOEQ11100OutBlock2.AddMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MnyAddMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayTotAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayDps` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyrclAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdaySubstAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayCsgnMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyCsgnMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMaintMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyMaintMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayOutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyoutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdaySubstOutAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayOrdAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyOrdAbleAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayAddMgnTp` | String | 1 |  |
| `CFOEQ11100OutBlock2.NtdayAddMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdayMnyAddMgn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.NtdaySettAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.EvalDpsamtTotamt` | Number | 15 |  |
| `CFOEQ11100OutBlock2.MnyEvalDpstgAmt` | Number | 15 |  |
| `CFOEQ11100OutBlock2.DpsamtUtlfeeGivPrergAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.TaxAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.CsgnMgnrat` | Number | 7.2 |  |
| `CFOEQ11100OutBlock2.CsgnMnyMgnrat` | Number | 7.2 |  |
| `CFOEQ11100OutBlock2.DpstgTotamtLackAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.DpstgMnyLackAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.RealInAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.InAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OutAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsAdjstDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsThdayDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsUpdtDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsLastSettDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSettDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBuyAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSellAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptXrcDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptAsgnDfamt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.RealGdsUndAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.RealGdsUndAsgnAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.RealGdsUndXrcAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.CmsnAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsCmsn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptCmsn` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsCtrctQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsCtrctAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptCtrctQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptCtrctAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsBuyUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsBuyUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsSellUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsSellUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBuyUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBuyUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSellUnsttQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSellUnsttAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsBuyctrQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsBuyctrAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsSlctrQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsSlctrAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBuyctrQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBuyctrAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSlctrQty` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptSlctrAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsBnsplAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptBnsplAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsEvalPnlAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptEvalPnlAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.FutsEvalAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.OptEvalAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MktEndAfMnyInAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MktEndAfMnyOutAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MktEndAfSubstDsgnAmt` | Number | 16 |  |
| `CFOEQ11100OutBlock2.MktEndAfSubstAbndAmt` | Number | 16 |  |

### CFOEQ82600 — 선물옵션 일별 계좌손익내역

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOEQ82600InBlock1.RecCnt` | Number | 5 |  |
| `CFOEQ82600InBlock1.QrySrtDt` | String | 8 |  |
| `CFOEQ82600InBlock1.QryEndDt` | String | 8 |  |
| `CFOEQ82600InBlock1.QryTp` | String | 1 | 1@일자별<br>2@월별<br>3@주간별 |
| `CFOEQ82600InBlock1.StnlnSeqTp` | String | 1 | 1@순<br>2@역순 |
| `CFOEQ82600InBlock1.FnoBalEvalTpCode` | String | 1 | 0:계좌에 따라 다르며 기본적으로는 선입선출<br>1:이동평균<br>2:선입선출 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOEQ82600OutBlock1.RecCnt` | Number | 5 |  |
| `CFOEQ82600OutBlock1.AcntNo` | String | 20 |  |
| `CFOEQ82600OutBlock1.Pwd` | String | 8 |  |
| `CFOEQ82600OutBlock1.QrySrtDt` | String | 8 |  |
| `CFOEQ82600OutBlock1.QryEndDt` | String | 8 |  |
| `CFOEQ82600OutBlock1.QryTp` | String | 1 |  |
| `CFOEQ82600OutBlock1.StnlnSeqTp` | String | 1 |  |
| `CFOEQ82600OutBlock1.FnoBalEvalTpCode` | String | 1 |  |
| `CFOEQ82600OutBlock2.RecCnt` | Number | 5 |  |
| `CFOEQ82600OutBlock2.FutsAdjstDfamt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.OptBnsplAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.FnoCmsnAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.PnlSumAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.MnyinSumAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.MnyoutSumAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock2.AcntNm` | String | 40 |  |
| `CFOEQ82600OutBlock3.QryDt` | String | 8 |  |
| `CFOEQ82600OutBlock3.DpstgTotamt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.DpstgMny` | Number | 16 |  |
| `CFOEQ82600OutBlock3.FnoMgn` | Number | 16 |  |
| `CFOEQ82600OutBlock3.FutsPnlAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.OptBsnPnlAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.OptEvalPnlAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.CmsnAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.SumAmt1` | Number | 16 |  |
| `CFOEQ82600OutBlock3.SumAmt2` | Number | 16 |  |
| `CFOEQ82600OutBlock3.PnlSumAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.FutsBuyAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.FutsSellAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.OptBuyAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.OptSellAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.InAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.OutAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.EvalAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.AddupEvalAmt` | Number | 16 |  |
| `CFOEQ82600OutBlock3.Amt2` | Number | 16 |  |

### CFOFQ02400 — 계좌 미결제 약정현황(평균가)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOFQ02400InBlock1.RecCnt` | Number | 5 |  |
| `CFOFQ02400InBlock1.RegMktCode` | String | 2 | 99@전체<br>40@KOSPI<br>20@KOSDAQ<br>10@KSE<br>50@KOFEX |
| `CFOFQ02400InBlock1.BuyDt` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOFQ02400OutBlock1.RecCnt` | Number | 5 |  |
| `CFOFQ02400OutBlock1.AcntNo` | String | 20 |  |
| `CFOFQ02400OutBlock1.Pwd` | String | 8 |  |
| `CFOFQ02400OutBlock1.RegMktCode` | String | 2 |  |
| `CFOFQ02400OutBlock1.BuyDt` | String | 8 |  |
| `CFOFQ02400OutBlock2.RecCnt` | Number | 5 |  |
| `CFOFQ02400OutBlock2.AcntNm` | String | 40 |  |
| `CFOFQ02400OutBlock2.FutsCtrctQty` | Number | 16 |  |
| `CFOFQ02400OutBlock2.OptCtrctQty` | Number | 16 |  |
| `CFOFQ02400OutBlock2.CtrctQty` | Number | 16 |  |
| `CFOFQ02400OutBlock2.FutsCtrctAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.FutsBuyctrAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.FutsSlctrAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.CalloptCtrctAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.CallBuyAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.CallSellAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.PutoptCtrctAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.PutBuyAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.PutSellAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.AllCtrctAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.BuyctrAsmAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.SlctrAsmAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock2.FutsPnlSum` | Number | 16 |  |
| `CFOFQ02400OutBlock2.OptPnlSum` | Number | 16 |  |
| `CFOFQ02400OutBlock2.AllPnlSum` | Number | 16 |  |
| `CFOFQ02400OutBlock3.FnoClssCode` | String | 1 |  |
| `CFOFQ02400OutBlock3.FutsSellQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.FutsSellPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock3.FutsBuyQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.FutsBuyPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock3.CallSellQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.CallSellPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock3.CallBuyQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.CallBuyPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock3.PutSellQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.PutSellPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock3.PutBuyQty` | Number | 16 |  |
| `CFOFQ02400OutBlock3.PutBuyPnl` | Number | 16 |  |
| `CFOFQ02400OutBlock4.IsuNo` | String | 12 |  |
| `CFOFQ02400OutBlock4.IsuNm` | String | 40 |  |
| `CFOFQ02400OutBlock4.BnsTpCode` | String | 1 |  |
| `CFOFQ02400OutBlock4.BnsTpNm` | String | 10 |  |
| `CFOFQ02400OutBlock4.BalQty` | Number | 16 |  |
| `CFOFQ02400OutBlock4.FnoAvrPrc` | Number | 19.8 |  |
| `CFOFQ02400OutBlock4.BgnAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock4.ThdayLqdtQty` | Number | 16 |  |
| `CFOFQ02400OutBlock4.Curprc` | Number | 13.2 |  |
| `CFOFQ02400OutBlock4.EvalAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock4.EvalPnlAmt` | Number | 16 |  |
| `CFOFQ02400OutBlock4.EvalErnrat` | Number | 12.6 |  |

### t0434 — 선물/옵션체결/미체결

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t0434InBlock.expcode` | String | 8 |  |
| `t0434InBlock.chegb` | String | 1 | 0;전체<br>1:체결<br>2:미체결 |
| `t0434InBlock.sortgb` | String | 1 | 1:주문번호 역순<br>2:주문번호 순 |
| `t0434InBlock.cts_ordno` | String | 7 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_ordno 값으로 설정 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t0434OutBlock.cts_ordno` | String | 7 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_ordno 필드에 넣어준다. |
| `t0434OutBlock1.ordno` | Number | 7 |  |
| `t0434OutBlock1.orgordno` | Number | 7 |  |
| `t0434OutBlock1.medosu` | String | 10 |  |
| `t0434OutBlock1.ordgb` | String | 20 |  |
| `t0434OutBlock1.qty` | Number | 9 |  |
| `t0434OutBlock1.price` | Number | 9.2 |  |
| `t0434OutBlock1.cheqty` | Number | 9 |  |
| `t0434OutBlock1.cheprice` | Number | 9.2 |  |
| `t0434OutBlock1.ordrem` | Number | 9 |  |
| `t0434OutBlock1.status` | String | 10 |  |
| `t0434OutBlock1.ordtime` | String | 8 |  |
| `t0434OutBlock1.ordermtd` | String | 10 |  |
| `t0434OutBlock1.expcode` | String | 8 |  |
| `t0434OutBlock1.rtcode` | String | 3 |  |
| `t0434OutBlock1.sysprocseq` | Number | 10 |  |
| `t0434OutBlock1.hogatype` | String | 1 |  |

### t0441 — 선물/옵션잔고평가(이동평균)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t0441InBlock.cts_expcode` | String | 8 |  |
| `t0441InBlock.cts_medocd` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t0441OutBlock.tdtsunik` | Number | 18 |  |
| `t0441OutBlock.cts_expcode` | String | 8 |  |
| `t0441OutBlock.cts_medocd` | String | 1 |  |
| `t0441OutBlock.tappamt` | Number | 18 |  |
| `t0441OutBlock.tsunik` | Number | 18 |  |
| `t0441OutBlock1.expcode` | String | 8 |  |
| `t0441OutBlock1.medosu` | String | 4 |  |
| `t0441OutBlock1.jqty` | Number | 10 |  |
| `t0441OutBlock1.cqty` | Number | 10 |  |
| `t0441OutBlock1.pamt` | Number | 10.2 |  |
| `t0441OutBlock1.mamt` | Number | 18 |  |
| `t0441OutBlock1.medocd` | String | 1 |  |
| `t0441OutBlock1.dtsunik` | Number | 18 |  |
| `t0441OutBlock1.sysprocseq` | Number | 10 |  |
| `t0441OutBlock1.price` | Number | 9.2 |  |
| `t0441OutBlock1.appamt` | Number | 18 |  |
| `t0441OutBlock1.dtsunik1` | Number | 18 |  |
| `t0441OutBlock1.sunikrt` | Number | 10.2 |  |

### CCENQ10100 — KRX야간파생 주문가능수량 조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ10100InBlock1.RecCnt` | Number | 5 |  |
| `CCENQ10100InBlock1.QryTp` | String | 1 | 1:일반<br>2:금액<br>3:비율 |
| `CCENQ10100InBlock1.OrdAmt` | Number | 16 | 조회구분이 2일경우만 사용, 그외 0 |
| `CCENQ10100InBlock1.RatVal` | Number | 19.8 | 조회구분이 3일경우만 사용, 그외 0 |
| `CCENQ10100InBlock1.FnoIsuNo` | String | 12 |  |
| `CCENQ10100InBlock1.BnsTpCode` | String | 1 | 1:매도<br>2:매수 |
| `CCENQ10100InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENQ10100InBlock1.FnoOrdprcPtnCode` | String | 2 | 00:지정가<br>03:시장가<br>05:조건부지정가<br>06:최유리지정가 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ10100OutBlock1.RecCnt` | Number | 5 |  |
| `CCENQ10100OutBlock1.AcntNo` | String | 20 |  |
| `CCENQ10100OutBlock1.Pwd` | String | 8 |  |
| `CCENQ10100OutBlock1.QryTp` | String | 1 |  |
| `CCENQ10100OutBlock1.OrdAmt` | Number | 16 |  |
| `CCENQ10100OutBlock1.RatVal` | Number | 19.8 |  |
| `CCENQ10100OutBlock1.FnoIsuNo` | String | 12 |  |
| `CCENQ10100OutBlock1.BnsTpCode` | String | 1 |  |
| `CCENQ10100OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENQ10100OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CCENQ10100OutBlock2.RecCnt` | Number | 5 |  |
| `CCENQ10100OutBlock2.AcntNm` | String | 40 |  |
| `CCENQ10100OutBlock2.QryDt` | String | 8 |  |
| `CCENQ10100OutBlock2.FnoNowPrc` | Number | 27.8 |  |
| `CCENQ10100OutBlock2.OrdAbleQty` | Number | 16 |  |
| `CCENQ10100OutBlock2.NewOrdAbleQty` | Number | 16 |  |
| `CCENQ10100OutBlock2.LqdtOrdAbleQty` | Number | 16 |  |
| `CCENQ10100OutBlock2.UsePreargMgn` | Number | 16 |  |
| `CCENQ10100OutBlock2.UsePreargMnyMgn` | Number | 16 |  |
| `CCENQ10100OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CCENQ10100OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |

### CCENQ30100 — KRX야간파생 주문/체결내역 조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ30100InBlock1.RecCnt` | String | 5 |  |
| `CCENQ30100InBlock1.AcntNo` | String | 20 |  |
| `CCENQ30100InBlock1.InptPwd` | String | 8 |  |
| `CCENQ30100InBlock1.QrySrtDt` | String | 8 |  |
| `CCENQ30100InBlock1.QryEndDt` | String | 8 |  |
| `CCENQ30100InBlock1.FnoClssCode` | String | 2 |  |
| `CCENQ30100InBlock1.PrdgrpCode` | String | 2 |  |
| `CCENQ30100InBlock1.PrdtExecTpCode` | String | 1 |  |
| `CCENQ30100InBlock1.StnlnSeqTp` | String | 1 |  |
| `CCENQ30100InBlock1.MktTpCode` | String | 1 |  |
| `CCENQ30100InBlock1.CommdaCode` | String | 2 |  |
| `CCENQ30100InBlock1.FnoIsuNo` | String | 12 |  |
| `CCENQ30100InBlock1.FnoTrdPtnCode` | String | 2 |  |
| `CCENQ30100InBlock1.GrpId` | String | 20 |  |
| `CCENQ30100InBlock1.UserId` | String | 16 |  |
| `CCENQ30100InBlock1.SrtOrdNo2` | String | 10 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ30100OutBlock1.RecCnt` | String | 5 |  |
| `CCENQ30100OutBlock1.AcntNo` | String | 20 |  |
| `CCENQ30100OutBlock1.InptPwd` | String | 8 |  |
| `CCENQ30100OutBlock1.QrySrtDt` | String | 8 |  |
| `CCENQ30100OutBlock1.QryEndDt` | String | 8 |  |
| `CCENQ30100OutBlock1.FnoClssCode` | String | 2 |  |
| `CCENQ30100OutBlock1.PrdgrpCode` | String | 2 |  |
| `CCENQ30100OutBlock1.PrdtExecTpCode` | String | 1 |  |
| `CCENQ30100OutBlock1.StnlnSeqTp` | String | 1 |  |
| `CCENQ30100OutBlock1.MktTpCode` | String | 1 |  |
| `CCENQ30100OutBlock1.CommdaCode` | String | 2 |  |
| `CCENQ30100OutBlock1.FnoIsuNo` | String | 12 |  |
| `CCENQ30100OutBlock1.FnoTrdPtnCode` | String | 2 |  |
| `CCENQ30100OutBlock1.GrpId` | String | 20 |  |
| `CCENQ30100OutBlock1.UserId` | String | 16 |  |
| `CCENQ30100OutBlock1.SrtOrdNo2` | String | 10 |  |
| `CCENQ30100OutBlock2.RecCnt` | String | 5 |  |
| `CCENQ30100OutBlock2.AcntNm` | String | 40 |  |
| `CCENQ30100OutBlock2.FutsOrdQty` | String | 16 |  |
| `CCENQ30100OutBlock2.FutsExecQty` | String | 16 |  |
| `CCENQ30100OutBlock2.OptOrdQty` | String | 16 |  |
| `CCENQ30100OutBlock2.OptExecQty` | String | 16 |  |
| `CCENQ30100OutBlock3.OrdDt` | String | 8 |  |
| `CCENQ30100OutBlock3.OrdNo` | String | 10 |  |
| `CCENQ30100OutBlock3.OrgOrdNo` | String | 10 |  |
| `CCENQ30100OutBlock3.OrdTime` | String | 9 |  |
| `CCENQ30100OutBlock3.FnoIsuNo` | String | 12 |  |
| `CCENQ30100OutBlock3.IsuNm` | String | 40 |  |
| `CCENQ30100OutBlock3.BnsTpNm` | String | 10 |  |
| `CCENQ30100OutBlock3.MrcTpNm` | String | 10 |  |
| `CCENQ30100OutBlock3.FnoOrdprcPtnCode` | String | 2 |  |
| `CCENQ30100OutBlock3.FnoOrdprcPtnNm` | String | 40 |  |
| `CCENQ30100OutBlock3.FnoOrdPrc` | String | 27.8 |  |
| `CCENQ30100OutBlock3.OrdQty` | String | 16 |  |
| `CCENQ30100OutBlock3.OrdTpNm` | String | 10 |  |
| `CCENQ30100OutBlock3.ExecTpNm` | String | 10 |  |
| `CCENQ30100OutBlock3.FnoExecPrc` | String | 27.8 |  |
| `CCENQ30100OutBlock3.ExecQty` | String | 16 |  |
| `CCENQ30100OutBlock3.CtrctTime` | String | 9 |  |
| `CCENQ30100OutBlock3.CtrctNo` | String | 10 |  |
| `CCENQ30100OutBlock3.ExecNo` | String | 10 |  |
| `CCENQ30100OutBlock3.BnsplAmt` | String | 16 |  |
| `CCENQ30100OutBlock3.UnercQty` | String | 16 |  |
| `CCENQ30100OutBlock3.UserId` | String | 16 |  |
| `CCENQ30100OutBlock3.MktClssCodeNm` | String | 40 |  |
| `CCENQ30100OutBlock3.CommdaCode` | String | 2 |  |
| `CCENQ30100OutBlock3.CommdaCodeNm` | String | 40 |  |
| `CCENQ30100OutBlock3.IpAddr` | String | 16 |  |
| `CCENQ30100OutBlock3.TrdPtnTpNm` | String | 20 |  |
| `CCENQ30100OutBlock3.GrpId` | String | 20 |  |

### CCENQ90200 — KRX야간파생 잔고조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ90200InBlock1.RecCnt` | Number | 5 | 1 |
| `CCENQ90200InBlock1.BalEvalTp` | String | 1 | 0:기본설정<br> 1:이동평균법<br> 2:선입선출법 |
| `CCENQ90200InBlock1.FutsPrcEvalTp` | String | 1 | 1:당초가<br> 2:전일종가 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENQ90200OutBlock1.RecCnt` | Number | 5 |  |
| `CCENQ90200OutBlock1.AcntNo` | String | 20 |  |
| `CCENQ90200OutBlock1.InptPwd` | String | 8 |  |
| `CCENQ90200OutBlock1.BalEvalTp` | String | 1 |  |
| `CCENQ90200OutBlock1.FutsPrcEvalTp` | String | 1 |  |
| `CCENQ90200OutBlock2.RecCnt` | String | 5 |  |
| `CCENQ90200OutBlock2.AcntNm` | String | 40 |  |
| `CCENQ90200OutBlock2.EvalDpsamtTotamt` | Number | 15 |  |
| `CCENQ90200OutBlock2.MnyEvalDpstgAmt` | Number | 15 |  |
| `CCENQ90200OutBlock2.DpsamtTotamt` | Number | 16 |  |
| `CCENQ90200OutBlock2.DpstgMny` | Number | 16 |  |
| `CCENQ90200OutBlock2.DpstgSubst` | Number | 16 |  |
| `CCENQ90200OutBlock2.PsnOutAbleTotAmt` | Number | 15 |  |
| `CCENQ90200OutBlock2.PsnOutAbleCurAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.PsnOutAbleSubstAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.OrdAbleTotAmt` | Number | 15 |  |
| `CCENQ90200OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.CsgnMgnTotamt` | Number | 16 |  |
| `CCENQ90200OutBlock2.MnyCsgnMgn` | Number | 16 |  |
| `CCENQ90200OutBlock2.MtmgnTotamt` | Number | 15 |  |
| `CCENQ90200OutBlock2.MnyMaintMgn` | Number | 16 |  |
| `CCENQ90200OutBlock2.EvalAmtSum` | Number | 17 |  |
| `CCENQ90200OutBlock2.RcvblOdpnt` | Number | 16 |  |
| `CCENQ90200OutBlock2.AddMgnTotamt` | Number | 15 |  |
| `CCENQ90200OutBlock2.EvalPnlSum` | Number | 15 |  |
| `CCENQ90200OutBlock2.RcvblAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.MnyAddMgn` | Number | 16 |  |
| `CCENQ90200OutBlock2.FutsEvalPnlAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.OptEvalPnlAmt` | Number | 16 |  |
| `CCENQ90200OutBlock2.OptEvalAmt` | Number | 16 |  |
| `CCENQ90200OutBlock3.FnoIsuNo` | String | 12 |  |
| `CCENQ90200OutBlock3.IsuNm` | String | 40 |  |
| `CCENQ90200OutBlock3.BnsTpCode` | String | 1 |  |
| `CCENQ90200OutBlock3.BnsTpNm` | String | 10 |  |
| `CCENQ90200OutBlock3.UnsttQty` | Number | 16 |  |
| `CCENQ90200OutBlock3.FnoAvrPrc` | Number | 198 |  |
| `CCENQ90200OutBlock3.FnoNowPrc` | Number | 278 |  |
| `CCENQ90200OutBlock3.FnoCmpPrc` | Number | 278 |  |
| `CCENQ90200OutBlock3.EvalPnl` | Number | 16 |  |
| `CCENQ90200OutBlock3.PnlRat` | Number | 186 |  |
| `CCENQ90200OutBlock3.FnoTrdUnitAmt` | Number | 198 |  |
| `CCENQ90200OutBlock3.EvalAmt` | Number | 16 |  |
| `CCENQ90200OutBlock3.EvalRat` | Number | 72 |  |
| `CCENQ90200OutBlock3.BnsplAmt` | Number | 16 |  |

### FOCCQ33700 — 선물옵션 기간별 계좌 수익률 현황

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `FOCCQ33700InBlock1.QrySrtDt` | String | 8 |  |
| `FOCCQ33700InBlock1.QryEndDt` | String | 8 |  |
| `FOCCQ33700InBlock1.QryTp` | String | 1 | 1.평균예탁자산기준<br>2.투입자산기준(기초자산+입출금액)<br>3.투입자산기준(기초자산+입금액) |
| `FOCCQ33700InBlock1.BaseAmtTp` | String | 1 | 1@평균예탁자산기준<br>2@투입자산기준(기초자산+입출금액)<br>3@투입자산기준(기초자산+입금액) |
| `FOCCQ33700InBlock1.QryTermTp` | String | 1 |  |
| `FOCCQ33700InBlock1.PnlCalcTpCode` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `FOCCQ33700OutBlock1.RecCnt` | Number | 5 |  |
| `FOCCQ33700OutBlock1.AcntNo` | String | 20 |  |
| `FOCCQ33700OutBlock1.Pwd` | String | 8 |  |
| `FOCCQ33700OutBlock1.QrySrtDt` | String | 8 |  |
| `FOCCQ33700OutBlock1.QryEndDt` | String | 8 |  |
| `FOCCQ33700OutBlock1.QryTp` | String | 1 |  |
| `FOCCQ33700OutBlock1.BaseAmtTp` | String | 1 |  |
| `FOCCQ33700OutBlock1.QryTermTp` | String | 1 |  |
| `FOCCQ33700OutBlock1.PnlCalcTpCode` | String | 1 |  |
| `FOCCQ33700OutBlock2.RecCnt` | Number | 5 |  |
| `FOCCQ33700OutBlock2.AcntNm` | String | 40 |  |
| `FOCCQ33700OutBlock2.InAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.OutAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.FnoCtrctAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.InvstPramtAvrbalAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.FutsAdjstDfamt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.OptBsnPnlAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.OptEvalPnlAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.InvstPlAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock2.ErnRat` | Number | 12.6 |  |
| `FOCCQ33700OutBlock3.TrdDt` | String | 8 |  |
| `FOCCQ33700OutBlock3.FdDpsastAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.EotDpsastAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.InAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.OutAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.InvstAvrbalPramt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.InvstPlAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.Ernrat` | Number | 12.6 |  |
| `FOCCQ33700OutBlock3.FnoCtrctAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.Trnrat` | Number | 12.6 |  |
| `FOCCQ33700OutBlock3.FutsAdjstDfamt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.OptBsnPnlAmt` | Number | 16 |  |
| `FOCCQ33700OutBlock3.OptEvalPnlAmt` | Number | 16 |  |

### CFOBQ10800 — 선물옵션 옵션매도시 주문증거금조회(옵션매도시 1계약당 주문증거금)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOBQ10800InBlock1.SpclDtPtnCode` | String | 3 | 기본 공백, 단, 위클리옵션은 월요일 "MON" , 목요일 "THR" |
| `CFOBQ10800InBlock1.SettWklyCnt` | String | 2 | 기본 공백, 단, 위클리옵션은 해당 주물 "W1", "W3", "W4" |
| `CFOBQ10800InBlock1.DueYymm` | String | 6 | 예)2023년 05월물 <br>단, 위클리옵션은 공백 |
| `CFOBQ10800InBlock1.IsuSmclssCode` | String | 3 | 501@코스피200<br>505@미니코스피200<br>506@코스닥150<br>509@위클리 ( 월, 목 무관 )<br>5AF@위클리 ( 월, 목 무관 ) |
| `CFOBQ10800InBlock1.IsuMdclssCode` | String | 2 | 00@전체<br>01@주가지수<br>02@개별주식<br>03@가공채권<br>04@통화<br>05@상품<br>06@금리<br>10@FLEX |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOBQ10800OutBlock1.SpclDtPtnCode` | String | 3 |  |
| `CFOBQ10800OutBlock1.RecCnt` | Number | 5 |  |
| `CFOBQ10800OutBlock1.IsuMdclssCode` | String | 2 |  |
| `CFOBQ10800OutBlock1.IsuSmclssCode` | String | 3 |  |
| `CFOBQ10800OutBlock1.DueYymm` | String | 6 |  |
| `CFOBQ10800OutBlock1.SettWklyCnt` | String | 2 |  |
| `CFOBQ10800OutBlock2.ElwXrcPrc` | Number | 13.2 |  |
| `CFOBQ10800OutBlock2.FnoIsuNo` | String | 12 |  |
| `CFOBQ10800OutBlock2.HanglIsuNm1` | String | 40 |  |
| `CFOBQ10800OutBlock2.TpNm1` | String | 40 |  |
| `CFOBQ10800OutBlock2.UpOptRegulThrprc` | Number | 27.8 |  |
| `CFOBQ10800OutBlock2.Thrprc1` | Number | 19.8 |  |
| `CFOBQ10800OutBlock2.BasePrc1` | Number | 13.2 |  |
| `CFOBQ10800OutBlock2.OrdMgn1` | Number | 16 |  |
| `CFOBQ10800OutBlock2.FnoIsuNo0` | String | 12 |  |
| `CFOBQ10800OutBlock2.HanglIsuNm2` | String | 40 |  |
| `CFOBQ10800OutBlock2.TpNm2` | String | 40 |  |
| `CFOBQ10800OutBlock2.DownOptRegulThrprc` | Number | 27.8 |  |
| `CFOBQ10800OutBlock2.Thrprc2` | Number | 19.8 |  |
| `CFOBQ10800OutBlock2.BasePrc2` | Number | 13.2 |  |
| `CFOBQ10800OutBlock2.OrdMgn2` | Number | 16 |  |

## [선물/옵션] 기타

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/etc`
- 설명: 파생증거금율에 대해 확인할 수 있습니다.

### MMDAQ91200 — 파생상품증거금율조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `MMDAQ91200InBlock1.IsuLgclssCode` | String | 2 |  |
| `MMDAQ91200InBlock1.IsuMdclssCode` | String | 2 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `MMDAQ91200OutBlock1.RecCnt` | Number | 5 |  |
| `MMDAQ91200OutBlock1.IsuLgclssCode` | String | 2 |  |
| `MMDAQ91200OutBlock1.IsuMdclssCode` | String | 2 |  |
| `MMDAQ91200OutBlock2.IsuSmclssCode` | String | 3 |  |
| `MMDAQ91200OutBlock2.IsuMdclssCode` | String | 2 |  |
| `MMDAQ91200OutBlock2.IsuLrgMdclssNm` | String | 40 |  |
| `MMDAQ91200OutBlock2.IsuLrgMidSmclssNm` | String | 40 |  |
| `MMDAQ91200OutBlock2.ShtnHanglIsuNm` | String | 40 |  |
| `MMDAQ91200OutBlock2.CsgnMgnrt` | Number | 26.9 |  |
| `MMDAQ91200OutBlock2.MaintMgnrt` | Number | 26.9 |  |
| `MMDAQ91200OutBlock2.MnyMgnrt` | Number | 26.9 |  |
| `MMDAQ91200OutBlock2.RmndDays` | Number | 6 |  |
| `MMDAQ91200OutBlock2.OnePrcntrOrdMgn` | Number | 17 |  |

## [선물/옵션] 시세

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/market-data`
- 설명: 주간/야간 선물옵션 종목별 시세 및 미결제약정 등시세관련 데이터를 확인할 수 있습니다.

### t2111 — 선물/옵션현재가(시세)조회

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2111InBlock.focode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2111OutBlock.hname` | String | 20 |  |
| `t2111OutBlock.price` | Number | 9.2 |  |
| `t2111OutBlock.sign` | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `t2111OutBlock.change` | Number | 9.2 |  |
| `t2111OutBlock.jnilclose` | Number | 9.2 |  |
| `t2111OutBlock.diff` | Number | 6.2 |  |
| `t2111OutBlock.volume` | Number | 12 |  |
| `t2111OutBlock.value` | Number | 12 |  |
| `t2111OutBlock.mgjv` | Number | 8 |  |
| `t2111OutBlock.mgjvdiff` | Number | 8 |  |
| `t2111OutBlock.open` | Number | 9.2 |  |
| `t2111OutBlock.high` | Number | 9.2 |  |
| `t2111OutBlock.low` | Number | 9.2 |  |
| `t2111OutBlock.uplmtprice` | Number | 9.2 |  |
| `t2111OutBlock.dnlmtprice` | Number | 9.2 |  |
| `t2111OutBlock.high52w` | Number | 9.2 |  |
| `t2111OutBlock.low52w` | Number | 9.2 |  |
| `t2111OutBlock.basis` | Number | 9.2 |  |
| `t2111OutBlock.recprice` | Number | 9.2 |  |
| `t2111OutBlock.theoryprice` | Number | 9.2 |  |
| `t2111OutBlock.glyl` | Number | 6.3 |  |
| `t2111OutBlock.cbhprice` | Number | 9.2 |  |
| `t2111OutBlock.cblprice` | Number | 9.2 |  |
| `t2111OutBlock.lastmonth` | String | 8 |  |
| `t2111OutBlock.jandatecnt` | Number | 8 |  |
| `t2111OutBlock.pricejisu` | Number | 9.2 |  |
| `t2111OutBlock.jisusign` | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `t2111OutBlock.jisuchange` | Number | 9.2 |  |
| `t2111OutBlock.jisudiff` | Number | 6.2 |  |
| `t2111OutBlock.kospijisu` | Number | 9.2 |  |
| `t2111OutBlock.kospisign` | String | 1 | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| `t2111OutBlock.kospichange` | Number | 9.2 |  |
| `t2111OutBlock.kospidiff` | Number | 6.2 |  |
| `t2111OutBlock.listhprice` | Number | 9.2 |  |
| `t2111OutBlock.listlprice` | Number | 9.2 |  |
| `t2111OutBlock.delt` | Number | 6.4 |  |
| `t2111OutBlock.gama` | Number | 6.4 |  |
| `t2111OutBlock.ceta` | Number | 6.4 |  |
| `t2111OutBlock.vega` | Number | 6.4 |  |
| `t2111OutBlock.rhox` | Number | 6.4 |  |
| `t2111OutBlock.gmprice` | Number | 9.2 |  |
| `t2111OutBlock.gmsign` | String | 1 |  |
| `t2111OutBlock.gmchange` | Number | 9.2 |  |
| `t2111OutBlock.gmdiff` | Number | 6.2 |  |
| `t2111OutBlock.theorypriceg` | Number | 9.2 |  |
| `t2111OutBlock.histimpv` | Number | 6.2 |  |
| `t2111OutBlock.impv` | Number | 6.2 |  |
| `t2111OutBlock.sbasis` | Number | 9.2 |  |
| `t2111OutBlock.ibasis` | Number | 9.2 |  |
| `t2111OutBlock.gmfutcode` | String | 8 |  |
| `t2111OutBlock.actprice` | Number | 6.2 |  |
| `t2111OutBlock.greeks_time` | String | 6 |  |
| `t2111OutBlock.greeks_confirm` | String | 8 |  |
| `t2111OutBlock.danhochk` | String | 1 |  |
| `t2111OutBlock.yeprice` | Number | 9.2 |  |
| `t2111OutBlock.jnilysign` | String | 1 |  |
| `t2111OutBlock.jnilychange` | Number | 9.2 |  |
| `t2111OutBlock.jnilydrate` | Number | 6.2 |  |
| `t2111OutBlock.alloc_gubun` | String | 1 |  |
| `t2111OutBlock.bjandatecnt` | Number | 8 |  |
| `t2111OutBlock.focode` | String | 8 |  |
| `t2111OutBlock.dy_gubun` | String | 1 |  |
| `t2111OutBlock.dy_uplmtprice` | Number | 9.2 |  |
| `t2111OutBlock.dy_dnlmtprice` | Number | 9.2 |  |
| `t2111OutBlock.updnstep_gubun` | String | 1 |  |
| `t2111OutBlock.upstep` | String | 2 |  |
| `t2111OutBlock.dnstep` | String | 2 |  |
| `t2111OutBlock.uplmtprice_3rd` | Number | 9.2 |  |
| `t2111OutBlock.dnlmtprice_3rd` | Number | 9.2 |  |
| `t2111OutBlock.expct_ccls_q` | Number | 9 |  |

### t2112 — 선물/옵션현재가호가조회

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2112InBlock.shcode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2112OutBlock.hname` | String | 20 |  |
| `t2112OutBlock.price` | Number | 9.2 |  |
| `t2112OutBlock.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2112OutBlock.change` | Number | 9.2 |  |
| `t2112OutBlock.diff` | Number | 6.2 |  |
| `t2112OutBlock.volume` | Number | 12 |  |
| `t2112OutBlock.stimeqrt` | Number | 6.2 |  |
| `t2112OutBlock.jnilclose` | Number | 9.2 |  |
| `t2112OutBlock.offerho1` | Number | 9.2 |  |
| `t2112OutBlock.bidho1` | Number | 9.2 |  |
| `t2112OutBlock.offerrem1` | Number | 8 |  |
| `t2112OutBlock.bidrem1` | Number | 8 |  |
| `t2112OutBlock.dcnt1` | Number | 8 |  |
| `t2112OutBlock.scnt1` | Number | 8 |  |
| `t2112OutBlock.offerho2` | Number | 9.2 |  |
| `t2112OutBlock.bidho2` | Number | 9.2 |  |
| `t2112OutBlock.offerrem2` | Number | 8 |  |
| `t2112OutBlock.bidrem2` | Number | 8 |  |
| `t2112OutBlock.dcnt2` | Number | 8 |  |
| `t2112OutBlock.scnt2` | Number | 8 |  |
| `t2112OutBlock.offerho3` | Number | 9.2 |  |
| `t2112OutBlock.bidho3` | Number | 9.2 |  |
| `t2112OutBlock.offerrem3` | Number | 8 |  |
| `t2112OutBlock.bidrem3` | Number | 8 |  |
| `t2112OutBlock.dcnt3` | Number | 8 |  |
| `t2112OutBlock.scnt3` | Number | 8 |  |
| `t2112OutBlock.offerho4` | Number | 9.2 |  |
| `t2112OutBlock.bidho4` | Number | 9.2 |  |
| `t2112OutBlock.offerrem4` | Number | 8 |  |
| `t2112OutBlock.bidrem4` | Number | 8 |  |
| `t2112OutBlock.dcnt4` | Number | 8 |  |
| `t2112OutBlock.scnt4` | Number | 8 |  |
| `t2112OutBlock.offerho5` | Number | 9.2 |  |
| `t2112OutBlock.bidho5` | Number | 9.2 |  |
| `t2112OutBlock.offerrem5` | Number | 8 |  |
| `t2112OutBlock.bidrem5` | Number | 8 |  |
| `t2112OutBlock.dcnt5` | Number | 8 |  |
| `t2112OutBlock.scnt5` | Number | 8 |  |
| `t2112OutBlock.dvol` | Number | 8 |  |
| `t2112OutBlock.svol` | Number | 8 |  |
| `t2112OutBlock.toffernum` | Number | 8 |  |
| `t2112OutBlock.tbidnum` | Number | 8 |  |
| `t2112OutBlock.time` | String | 6 |  |
| `t2112OutBlock.shcode` | String | 8 |  |

### t2106 — 선물/옵션현재가시세메모

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2106InBlock.code` | String | 8 |  |
| `t2106InBlock.nrec` | String | 2 | t2106InBlock1 의 개수 |
| `t2106InBlock1.indx` | String | 1 | t2106InBlock1 의 Occurs 순서(0부터 시작) |
| `t2106InBlock1.gubn` | String | 1 | 1:시세<br>2:최고저가<br>3:Pivot<br>4:이동평균선 |
| `t2106InBlock1.dat1` | String | 1 | 1:시가<br>2:고가<br>3:저가<br>4:가중평균가 |
| `t2106InBlock1.dat2` | String | 8 | 1:당일<br>2:전일 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2106OutBlock.nrec` | String | 2 | t2106OutBlock1 의 개수 |
| `t2106OutBlock1.indx` | String | 1 | t2106InBlock1 의 indx와 동일 |
| `t2106OutBlock1.gubn` | String | 1 | 1:시세<br>2:최고저가<br>3:Pivot<br>4:이동평균선<br>t2106InBlock1의 gubn과 동일 |
| `t2106OutBlock1.vals` | String | 8 |  |

### t2212 — 선물옵션시간대별체결조회

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2212InBlock.focode` | String | 8 |  |
| `t2212InBlock.cvolume` | Number | 12 | 체결수량 >= cvolume |
| `t2212InBlock.stime` | String | 4 | 체결시간 >= stime(hhmm) |
| `t2212InBlock.etime` | String | 4 | 체결시간 <= etime(hhmm) |
| `t2212InBlock.cts_time` | String | 10 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2212OutBlock.cts_time` | String | 10 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| `t2212OutBlock1.chetime` | String | 10 |  |
| `t2212OutBlock1.price` | Number | 9.2 |  |
| `t2212OutBlock1.sign` | String | 1 |  |
| `t2212OutBlock1.change` | Number | 9.2 |  |
| `t2212OutBlock1.cvolume` | Number | 8 |  |
| `t2212OutBlock1.chdegree` | Number | 8.2 |  |
| `t2212OutBlock1.offerho` | Number | 9.2 |  |
| `t2212OutBlock1.bidho` | Number | 9.2 |  |
| `t2212OutBlock1.volume` | Number | 12 |  |
| `t2212OutBlock1.openyak` | Number | 8 |  |
| `t2212OutBlock1.jnilopenupdn` | Number | 8 |  |
| `t2212OutBlock1.ibasis` | Number | 9.2 |  |
| `t2212OutBlock1.sbasis` | Number | 9.2 |  |
| `t2212OutBlock1.kasis` | Number | 6.2 |  |
| `t2212OutBlock1.value` | Number | 12 |  |
| `t2212OutBlock1.j_openupdn` | Number | 8 |  |
| `t2212OutBlock1.n_msvolume` | Number | 12 |  |
| `t2212OutBlock1.n_mdvolume` | Number | 12 |  |
| `t2212OutBlock1.s_msvolume` | Number | 12 |  |
| `t2212OutBlock1.n_mschecnt` | Number | 8 |  |
| `t2212OutBlock1.n_mdchecnt` | Number | 8 |  |
| `t2212OutBlock1.s_mschecnt` | Number | 8 |  |

### t2214 — 기간별주가

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2214InBlock.shcode` | String | 8 |  |
| `t2214InBlock.futcheck` | String | 1 | 0:default<br>1:최근월물만연결 |
| `t2214InBlock.date` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정 |
| `t2214InBlock.cts_code` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_code 값으로 설정 |
| `t2214InBlock.lastdate` | String | 8 |  |
| `t2214InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2214OutBlock.date` | String | 8 | 연속조회키<br>연속 조회시 이 값을 InBlock의 date 필드에 넣어준다. |
| `t2214OutBlock.cts_code` | String | 8 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_code 필드에 넣어준다. |
| `t2214OutBlock.lastdate` | String | 8 |  |
| `t2214OutBlock.nowfutyn` | String | 1 |  |
| `t2214OutBlock1.date` | String | 8 |  |
| `t2214OutBlock1.open` | Number | 9.2 |  |
| `t2214OutBlock1.high` | Number | 9.2 |  |
| `t2214OutBlock1.low` | Number | 9.2 |  |
| `t2214OutBlock1.close` | Number | 9.2 |  |
| `t2214OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2214OutBlock1.change` | Number | 9.2 |  |
| `t2214OutBlock1.diff` | Number | 6.2 |  |
| `t2214OutBlock1.volume` | Number | 12 |  |
| `t2214OutBlock1.diff_vol` | Number | 10.2 |  |
| `t2214OutBlock1.openyak` | Number | 8 |  |
| `t2214OutBlock1.openyakupdn` | Number | 8 |  |
| `t2214OutBlock1.value` | Number | 12 |  |

### t2210 — 선물옵션시간대별체결조회(단일출력용)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2210InBlock.focode` | String | 8 |  |
| `t2210InBlock.cvolume` | Number | 12 | 체결수량 >= cvolume |
| `t2210InBlock.stime` | String | 4 | 체결시간 >= stime(hhmm) |
| `t2210InBlock.etime` | String | 4 | 체결시간 <= etime(hhmm) |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2210OutBlock.mdvolume` | Number | 8 |  |
| `t2210OutBlock.mdchecnt` | Number | 8 |  |
| `t2210OutBlock.msvolume` | Number | 8 |  |
| `t2210OutBlock.mschecnt` | Number | 8 |  |

### t2301 — 옵션전광판

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2301InBlock.yyyymm` | String | 6 | ex) 미니,정규 : '200604'<br>    위클리 : 'W1    ' |
| `t2301InBlock.gubun` | String | 1 | M: 미니<br>G: 정규<br>W: 위클리 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2301OutBlock.histimpv` | Number | 4 |  |
| `t2301OutBlock.jandatecnt` | Number | 4 |  |
| `t2301OutBlock.cimpv` | Number | 6.3 |  |
| `t2301OutBlock.pimpv` | Number | 6.3 |  |
| `t2301OutBlock.gmprice` | Number | 6.2 |  |
| `t2301OutBlock.gmsign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2301OutBlock.gmchange` | Number | 6.2 |  |
| `t2301OutBlock.gmdiff` | Number | 6.2 |  |
| `t2301OutBlock.gmvolume` | Number | 12 |  |
| `t2301OutBlock.gmshcode` | String | 8 |  |
| `t2301OutBlock1.actprice` | Number | 6.2 |  |
| `t2301OutBlock1.optcode` | String | 8 |  |
| `t2301OutBlock1.price` | Number | 6.2 |  |
| `t2301OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2301OutBlock1.change` | Number | 6.2 |  |
| `t2301OutBlock1.diff` | Number | 6.2 |  |
| `t2301OutBlock1.volume` | Number | 12 |  |
| `t2301OutBlock1.iv` | Number | 6.2 |  |
| `t2301OutBlock1.mgjv` | Number | 12 |  |
| `t2301OutBlock1.mgjvupdn` | Number | 12 |  |
| `t2301OutBlock1.offerho1` | Number | 6.2 |  |
| `t2301OutBlock1.bidho1` | Number | 6.2 |  |
| `t2301OutBlock1.cvolume` | Number | 12 |  |
| `t2301OutBlock1.delt` | Number | 6.4 |  |
| `t2301OutBlock1.gama` | Number | 6.4 |  |
| `t2301OutBlock1.vega` | Number | 6.4 |  |
| `t2301OutBlock1.ceta` | Number | 6.4 |  |
| `t2301OutBlock1.rhox` | Number | 6.4 |  |
| `t2301OutBlock1.theoryprice` | Number | 6.2 |  |
| `t2301OutBlock1.impv` | Number | 6.2 |  |
| `t2301OutBlock1.timevl` | Number | 6.2 |  |
| `t2301OutBlock1.jvolume` | Number | 12 |  |
| `t2301OutBlock1.parpl` | Number | 12 |  |
| `t2301OutBlock1.jngo` | Number | 6 |  |
| `t2301OutBlock1.offerrem1` | Number | 12 |  |
| `t2301OutBlock1.bidrem1` | Number | 12 |  |
| `t2301OutBlock1.open` | Number | 6.2 |  |
| `t2301OutBlock1.high` | Number | 6.2 |  |
| `t2301OutBlock1.low` | Number | 6.2 |  |
| `t2301OutBlock1.atmgubun` | String | 1 | 0:선물<br>1:ATM<br>2:ITM<br>3:OTM |
| `t2301OutBlock1.jisuconv` | Number | 10.2 |  |
| `t2301OutBlock1.value` | Number | 12 |  |
| `t2301OutBlock2.actprice` | Number | 6.2 |  |
| `t2301OutBlock2.optcode` | String | 8 |  |
| `t2301OutBlock2.price` | Number | 6.2 |  |
| `t2301OutBlock2.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2301OutBlock2.change` | Number | 6.2 |  |
| `t2301OutBlock2.diff` | Number | 6.2 |  |
| `t2301OutBlock2.volume` | Number | 12 |  |
| `t2301OutBlock2.iv` | Number | 6.2 |  |
| `t2301OutBlock2.mgjv` | Number | 12 |  |
| `t2301OutBlock2.mgjvupdn` | Number | 12 |  |
| `t2301OutBlock2.offerho1` | Number | 6.2 |  |
| `t2301OutBlock2.bidho1` | Number | 6.2 |  |
| `t2301OutBlock2.cvolume` | Number | 12 |  |
| `t2301OutBlock2.delt` | Number | 6.4 |  |
| `t2301OutBlock2.gama` | Number | 6.4 |  |
| `t2301OutBlock2.vega` | Number | 6.4 |  |
| `t2301OutBlock2.ceta` | Number | 6.4 |  |
| `t2301OutBlock2.rhox` | Number | 6.4 |  |
| `t2301OutBlock2.theoryprice` | Number | 6.2 |  |
| `t2301OutBlock2.impv` | Number | 6.2 |  |
| `t2301OutBlock2.timevl` | Number | 6.2 |  |
| `t2301OutBlock2.jvolume` | Number | 12 |  |
| `t2301OutBlock2.parpl` | Number | 12 |  |
| `t2301OutBlock2.jngo` | Number | 6 |  |
| `t2301OutBlock2.offerrem1` | Number | 12 |  |
| `t2301OutBlock2.bidrem1` | Number | 12 |  |
| `t2301OutBlock2.open` | Number | 6.2 |  |
| `t2301OutBlock2.high` | Number | 6.2 |  |
| `t2301OutBlock2.low` | Number | 6.2 |  |
| `t2301OutBlock2.atmgubun` | String | 1 | 0:선물<br>1:ATM<br>2:ITM<br>3:OTM |
| `t2301OutBlock2.jisuconv` | Number | 10.2 |  |
| `t2301OutBlock2.value` | Number | 12 |  |

### t2407 — 선물옵션호가잔량비율챠트

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2407InBlock.focode` | String | 8 |  |
| `t2407InBlock.bgubun` | String | 1 | 0:30초<br>1:분 |
| `t2407InBlock.nmin` | Number | 2 | bgubun = 1 인 경우 N분 입력값 |
| `t2407InBlock.etime` | String | 4 | etime 이전 시간대를 조회함 |
| `t2407InBlock.hgubun` | String | 1 | 0@총 호가잔량<br>1@1차 호가잔량<br>2@2차 호가잔량<br>3@3차 호가잔량<br>4@4차 호가잔량<br>5@5차 호가잔량 |
| `t2407InBlock.cnt` | Number | 3 |  |
| `t2407InBlock.cts_time` | String | 6 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2407OutBlock.mdvolume` | Number | 12 |  |
| `t2407OutBlock.mdchecnt` | Number | 8 |  |
| `t2407OutBlock.msvolume` | Number | 12 |  |
| `t2407OutBlock.mschecnt` | Number | 8 |  |
| `t2407OutBlock.cts_time` | String | 6 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| `t2407OutBlock1.time` | String | 6 |  |
| `t2407OutBlock1.price` | Number | 9.2 |  |
| `t2407OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2407OutBlock1.change` | Number | 9.2 |  |
| `t2407OutBlock1.volume` | Number | 12 |  |
| `t2407OutBlock1.cvolume` | Number | 8 |  |
| `t2407OutBlock1.offerho1` | Number | 9.2 |  |
| `t2407OutBlock1.bidho1` | Number | 9.2 |  |
| `t2407OutBlock1.offerrem` | Number | 8 |  |
| `t2407OutBlock1.bidrem` | Number | 8 |  |
| `t2407OutBlock1.offercnt` | Number | 8 |  |
| `t2407OutBlock1.bidcnt` | Number | 8 |  |
| `t2407OutBlock1.c_offerrem` | Number | 8 |  |
| `t2407OutBlock1.c_bidrem` | Number | 8 |  |
| `t2407OutBlock1.c_offercnt` | Number | 8 |  |
| `t2407OutBlock1.c_bidcnt` | Number | 8 |  |
| `t2407OutBlock1.r_bidrem` | Number | 6.2 |  |
| `t2407OutBlock1.r_bidcnt` | Number | 6.2 |  |
| `t2407OutBlock1.r_sign` | String | 1 | 2:매수수량비율 > 100<br>5:매수수량비율 <= 100 |
| `t2407OutBlock1.date` | Object | 8 |  |

### t2424 — 미결제약정추이

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2424InBlock.focode` | String | 8 |  |
| `t2424InBlock.bdgubun` | String | 1 | 0:30초<br>1:분<br>2:일 |
| `t2424InBlock.nmin` | Number | 3 | t2424InBlock.bdgubun 이 1인 경우 N분 |
| `t2424InBlock.tcgubun` | String | 1 | 0:전체<br>1:당일 |
| `t2424InBlock.cnt` | Number | 4 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2424OutBlock.price` | Number | 9.2 |  |
| `t2424OutBlock.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t2424OutBlock.change` | Number | 9.2 |  |
| `t2424OutBlock.diff` | Number | 6.2 |  |
| `t2424OutBlock.cvolume` | Number | 8 |  |
| `t2424OutBlock.volume` | Number | 15 |  |
| `t2424OutBlock.openyak` | Number | 8 |  |
| `t2424OutBlock1.dt` | String | 14 |  |
| `t2424OutBlock1.open` | Number | 9.2 |  |
| `t2424OutBlock1.high` | Number | 9.2 |  |
| `t2424OutBlock1.low` | Number | 9.2 |  |
| `t2424OutBlock1.close` | Number | 9.2 |  |
| `t2424OutBlock1.openopenyak` | Number | 8 |  |
| `t2424OutBlock1.highopenyak` | Number | 8 |  |
| `t2424OutBlock1.lowopenyak` | Number | 8 |  |
| `t2424OutBlock1.closeopenyak` | Number | 8 |  |
| `t2424OutBlock1.openupdn` | Number | 8 |  |

### t2522 — 주식선물기초자산조회

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2522InBlock.dummy` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2522OutBlock.cnt` | Number | 5 |  |
| `t2522OutBlock1.bsc_asts_nm` | String | 40 |  |
| `t2522OutBlock1.bsc_asts_is_cd` | String | 6 |  |
| `t2522OutBlock1.bsc_asts_id` | String | 3 |  |
| `t2522OutBlock1.nmc_is_shrt_cd` | String | 8 |  |

### t8401 — 주식선물마스터조회(API용)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8401OutBlock.hname` | String | 20 |  |
| `t8401OutBlock.shcode` | String | 8 |  |
| `t8401OutBlock.expcode` | String | 12 |  |
| `t8401OutBlock.basecode` | String | 9 |  |

### t8402 — 주식선물현재가조회(API용)

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8402InBlock.focode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8402OutBlock.hname` | String | 20 |  |
| `t8402OutBlock.price` | Number | 8 |  |
| `t8402OutBlock.sign` | String | 1 |  |
| `t8402OutBlock.change` | Number | 8 |  |
| `t8402OutBlock.jnilclose` | Number | 8 |  |
| `t8402OutBlock.diff` | Number | 6.2 |  |
| `t8402OutBlock.volume` | Number | 12 |  |
| `t8402OutBlock.stimeqrt` | Number | 6.2 |  |
| `t8402OutBlock.value` | Number | 12 |  |
| `t8402OutBlock.mgjv` | Number | 8 |  |
| `t8402OutBlock.mgjvdiff` | Number | 8 |  |
| `t8402OutBlock.open` | Number | 8 |  |
| `t8402OutBlock.high` | Number | 8 |  |
| `t8402OutBlock.low` | Number | 8 |  |
| `t8402OutBlock.uplmtprice` | Number | 8 |  |
| `t8402OutBlock.dnlmtprice` | Number | 8 |  |
| `t8402OutBlock.high52w` | Number | 8 |  |
| `t8402OutBlock.low52w` | Number | 8 |  |
| `t8402OutBlock.basis` | Number | 6.2 |  |
| `t8402OutBlock.recprice` | Number | 8 |  |
| `t8402OutBlock.theoryprice` | Number | 8 |  |
| `t8402OutBlock.glyl` | Number | 6.3 |  |
| `t8402OutBlock.lastmonth` | String | 8 |  |
| `t8402OutBlock.jandatecnt` | Number | 8 |  |
| `t8402OutBlock.pricejisu` | Number | 10.2 |  |
| `t8402OutBlock.jisusign` | String | 1 |  |
| `t8402OutBlock.jisuchange` | Number | 10.2 |  |
| `t8402OutBlock.jisudiff` | Number | 6.2 |  |
| `t8402OutBlock.kospijisu` | Number | 10.2 |  |
| `t8402OutBlock.kospisign` | String | 1 |  |
| `t8402OutBlock.kospichange` | Number | 10.2 |  |
| `t8402OutBlock.kospidiff` | Number | 6.2 |  |
| `t8402OutBlock.listhprice` | Number | 8 |  |
| `t8402OutBlock.listlprice` | Number | 8 |  |
| `t8402OutBlock.delt` | Number | 6.4 |  |
| `t8402OutBlock.gama` | Number | 6.4 |  |
| `t8402OutBlock.ceta` | Number | 6.4 |  |
| `t8402OutBlock.vega` | Number | 6.4 |  |
| `t8402OutBlock.rhox` | Number | 6.4 |  |
| `t8402OutBlock.gmprice` | Number | 8 |  |
| `t8402OutBlock.gmsign` | String | 1 |  |
| `t8402OutBlock.gmchange` | Number | 8 |  |
| `t8402OutBlock.gmdiff` | Number | 6.2 |  |
| `t8402OutBlock.theorypriceg` | Number | 8 |  |
| `t8402OutBlock.histimpv` | Number | 6.2 |  |
| `t8402OutBlock.impv` | Number | 6.2 |  |
| `t8402OutBlock.sbasis` | Number | 8 |  |
| `t8402OutBlock.ibasis` | Number | 8 |  |
| `t8402OutBlock.gmfutcode` | String | 8 |  |
| `t8402OutBlock.actprice` | Number | 8 |  |
| `t8402OutBlock.shcode` | String | 6 |  |
| `t8402OutBlock.basehname` | String | 20 |  |
| `t8402OutBlock.baseprice` | Number | 8 |  |
| `t8402OutBlock.basesign` | String | 1 |  |
| `t8402OutBlock.basechange` | Number | 8 |  |
| `t8402OutBlock.basediff` | Number | 6.2 |  |
| `t8402OutBlock.basevol` | Number | 12 |  |
| `t8402OutBlock.baseprevol` | Number | 12 |  |
| `t8402OutBlock.basebidprc` | Number | 9 |  |
| `t8402OutBlock.baseaskprc` | Number | 9 |  |
| `t8402OutBlock.basefornetbid` | Number | 12 |  |
| `t8402OutBlock.prodgrp` | String | 20 |  |
| `t8402OutBlock.mulcnt` | Number | 12.8 |  |
| `t8402OutBlock.danhochk` | String | 1 |  |
| `t8402OutBlock.yeprice` | Number | 8 |  |
| `t8402OutBlock.jnilysign` | String | 1 |  |
| `t8402OutBlock.jnilychange` | Number | 8 |  |
| `t8402OutBlock.jnilydrate` | Number | 6.2 |  |

### t8403 — 주식선물호가조회(API용)

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8403InBlock.shcode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8403OutBlock.hname` | String | 20 |  |
| `t8403OutBlock.price` | Number | 8 |  |
| `t8403OutBlock.sign` | String | 1 |  |
| `t8403OutBlock.change` | Number | 8 |  |
| `t8403OutBlock.diff` | Number | 6.2 |  |
| `t8403OutBlock.volume` | Number | 12 |  |
| `t8403OutBlock.stimeqrt` | Number | 6.2 |  |
| `t8403OutBlock.jnilclose` | Number | 8 |  |
| `t8403OutBlock.offerho1` | Number | 8 |  |
| `t8403OutBlock.bidho1` | Number | 8 |  |
| `t8403OutBlock.offerrem1` | Number | 8 |  |
| `t8403OutBlock.bidrem1` | Number | 8 |  |
| `t8403OutBlock.dcnt1` | Number | 8 |  |
| `t8403OutBlock.scnt1` | Number | 8 |  |
| `t8403OutBlock.offerho2` | Number | 8 |  |
| `t8403OutBlock.bidho2` | Number | 8 |  |
| `t8403OutBlock.offerrem2` | Number | 8 |  |
| `t8403OutBlock.bidrem2` | Number | 8 |  |
| `t8403OutBlock.dcnt2` | Number | 8 |  |
| `t8403OutBlock.scnt2` | Number | 8 |  |
| `t8403OutBlock.offerho3` | Number | 8 |  |
| `t8403OutBlock.bidho3` | Number | 8 |  |
| `t8403OutBlock.offerrem3` | Number | 8 |  |
| `t8403OutBlock.bidrem3` | Number | 8 |  |
| `t8403OutBlock.dcnt3` | Number | 8 |  |
| `t8403OutBlock.scnt3` | Number | 8 |  |
| `t8403OutBlock.offerho4` | Number | 8 |  |
| `t8403OutBlock.bidho4` | Number | 8 |  |
| `t8403OutBlock.offerrem4` | Number | 8 |  |
| `t8403OutBlock.bidrem4` | Number | 8 |  |
| `t8403OutBlock.dcnt4` | Number | 8 |  |
| `t8403OutBlock.scnt4` | Number | 8 |  |
| `t8403OutBlock.offerho5` | Number | 8 |  |
| `t8403OutBlock.bidho5` | Number | 8 |  |
| `t8403OutBlock.offerrem5` | Number | 8 |  |
| `t8403OutBlock.bidrem5` | Number | 8 |  |
| `t8403OutBlock.dcnt5` | Number | 8 |  |
| `t8403OutBlock.scnt5` | Number | 8 |  |
| `t8403OutBlock.offerho6` | Number | 8 |  |
| `t8403OutBlock.bidho6` | Number | 8 |  |
| `t8403OutBlock.offerrem6` | Number | 8 |  |
| `t8403OutBlock.bidrem6` | Number | 8 |  |
| `t8403OutBlock.dcnt6` | Number | 8 |  |
| `t8403OutBlock.scnt6` | Number | 8 |  |
| `t8403OutBlock.offerho7` | Number | 8 |  |
| `t8403OutBlock.bidho7` | Number | 8 |  |
| `t8403OutBlock.offerrem7` | Number | 8 |  |
| `t8403OutBlock.bidrem7` | Number | 8 |  |
| `t8403OutBlock.dcnt7` | Number | 8 |  |
| `t8403OutBlock.scnt7` | Number | 8 |  |
| `t8403OutBlock.offerho8` | Number | 8 |  |
| `t8403OutBlock.bidho8` | Number | 8 |  |
| `t8403OutBlock.offerrem8` | Number | 8 |  |
| `t8403OutBlock.bidrem8` | Number | 8 |  |
| `t8403OutBlock.dcnt8` | Number | 8 |  |
| `t8403OutBlock.scnt8` | Number | 8 |  |
| `t8403OutBlock.offerho9` | Number | 8 |  |
| `t8403OutBlock.bidho9` | Number | 8 |  |
| `t8403OutBlock.offerrem9` | Number | 8 |  |
| `t8403OutBlock.bidrem9` | Number | 8 |  |
| `t8403OutBlock.dcnt9` | Number | 8 |  |
| `t8403OutBlock.scnt9` | Number | 8 |  |
| `t8403OutBlock.offerho10` | Number | 8 |  |
| `t8403OutBlock.bidho10` | Number | 8 |  |
| `t8403OutBlock.offerrem10` | Number | 8 |  |
| `t8403OutBlock.bidrem10` | Number | 8 |  |
| `t8403OutBlock.dcnt10` | Number | 8 |  |
| `t8403OutBlock.scnt10` | Number | 8 |  |
| `t8403OutBlock.dvol` | Number | 8 |  |
| `t8403OutBlock.svol` | Number | 8 |  |
| `t8403OutBlock.toffernum` | Number | 8 |  |
| `t8403OutBlock.tbidnum` | Number | 8 |  |
| `t8403OutBlock.time` | String | 6 |  |
| `t8403OutBlock.shcode` | String | 6 |  |

### t8404 — 주식선물시간대별체결조회(API용)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8404InBlock.focode` | String | 8 |  |
| `t8404InBlock.cvolume` | Number | 12 | 거래량 > 특이거래량 |
| `t8404InBlock.stime` | String | 4 | 장시작시간 이후 |
| `t8404InBlock.etime` | String | 4 | 장종료시간 이전 |
| `t8404InBlock.cts_time` | String | 10 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8404OutBlock.cts_time` | String | 10 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| `t8404OutBlock1.chetime` | String | 10 |  |
| `t8404OutBlock1.price` | Number | 8 |  |
| `t8404OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t8404OutBlock1.change` | Number | 8 |  |
| `t8404OutBlock1.cvolume` | Number | 8 |  |
| `t8404OutBlock1.chdegree` | Number | 8.2 |  |
| `t8404OutBlock1.offerho` | Number | 8 |  |
| `t8404OutBlock1.bidho` | Number | 8 |  |
| `t8404OutBlock1.volume` | Number | 12 |  |
| `t8404OutBlock1.openyak` | Number | 8 |  |
| `t8404OutBlock1.jnilopenupdn` | Number | 8 |  |
| `t8404OutBlock1.ibasis` | Number | 8 |  |
| `t8404OutBlock1.sbasis` | Number | 8 |  |
| `t8404OutBlock1.kasis` | Number | 6.2 |  |
| `t8404OutBlock1.value` | Number | 12 |  |
| `t8404OutBlock1.j_openupdn` | Number | 8 |  |
| `t8404OutBlock1.n_msvolume` | Number | 12 |  |
| `t8404OutBlock1.n_mdvolume` | Number | 12 |  |
| `t8404OutBlock1.s_msvolume` | Number | 12 |  |
| `t8404OutBlock1.n_mschecnt` | Number | 8 |  |
| `t8404OutBlock1.n_mdchecnt` | Number | 8 |  |
| `t8404OutBlock1.s_mschecnt` | Number | 8 |  |

### t8405 — 주식선물기간별주가(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8405InBlock.shcode` | String | 8 |  |
| `t8405InBlock.futcheck` | String | 1 | 0:default<br>1:최근월물만연결 |
| `t8405InBlock.date` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정 |
| `t8405InBlock.cts_code` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_code 값으로 설정 |
| `t8405InBlock.lastdate` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 lastdate 값으로 설정 |
| `t8405InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8405OutBlock.date` | String | 8 | 연속조회키<br>연속 조회시 이 값을 InBlock의 date 필드에 넣어준다. |
| `t8405OutBlock.cts_code` | String | 8 | 연속조회키<br>연속 조회시 이 값을 InBlock의 cts_code 필드에 넣어준다. |
| `t8405OutBlock.lastdate` | String | 8 | 연속조회키<br>연속 조회시 이 값을 InBlock의 lastdate 필드에 넣어준다. |
| `t8405OutBlock.nowfutyn` | String | 1 |  |
| `t8405OutBlock1.date` | String | 8 |  |
| `t8405OutBlock1.open` | Number | 8 |  |
| `t8405OutBlock1.high` | Number | 8 |  |
| `t8405OutBlock1.low` | Number | 8 |  |
| `t8405OutBlock1.close` | Number | 8 |  |
| `t8405OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t8405OutBlock1.change` | Number | 8 |  |
| `t8405OutBlock1.diff` | Number | 6.2 |  |
| `t8405OutBlock1.volume` | Number | 12 |  |
| `t8405OutBlock1.diff_vol` | Number | 10.2 |  |
| `t8405OutBlock1.openyak` | Number | 8 |  |
| `t8405OutBlock1.openyakupdn` | Number | 8 |  |
| `t8405OutBlock1.value` | Number | 12 |  |

### t8406 — 주식선물틱분별체결조회(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8406InBlock.focode` | String | 8 |  |
| `t8406InBlock.cgubun` | String | 1 | T:틱차트<br>B:분차트 |
| `t8406InBlock.bgubun` | Object | 3 | 차트구분이 'B'일때만 체크<br>0: 30초<br>0초과 : n분 |
| `t8406InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8406OutBlock1.chetime` | String | 10 |  |
| `t8406OutBlock1.price` | Number | 8 |  |
| `t8406OutBlock1.sign` | String | 1 | 1:상한<br>2:상승<br>3:보합<br>4:하한<br>5:하락 |
| `t8406OutBlock1.change` | Number | 8 |  |
| `t8406OutBlock1.open` | Number | 8 |  |
| `t8406OutBlock1.high` | Number | 8 |  |
| `t8406OutBlock1.low` | Number | 8 |  |
| `t8406OutBlock1.volume` | Number | 12 |  |
| `t8406OutBlock1.value` | Number | 12 |  |
| `t8406OutBlock1.openyak` | Number | 8 |  |
| `t8406OutBlock1.openupdn` | Number | 8 |  |
| `t8406OutBlock1.cvolume` | Number | 8 |  |
| `t8406OutBlock1.s_mschecnt` | Number | 8 |  |
| `t8406OutBlock1.s_mdchecnt` | Number | 8 |  |
| `t8406OutBlock1.ss_mschecnt` | Number | 8 |  |
| `t8406OutBlock1.s_mschevol` | Number | 12 |  |
| `t8406OutBlock1.s_mdchevol` | Number | 12 |  |
| `t8406OutBlock1.ss_mschevol` | Number | 12 |  |
| `t8406OutBlock1.chdegvol` | Number | 8.2 |  |
| `t8406OutBlock1.chdegcnt` | Number | 8.2 |  |

### t8426 — 상품선물마스터조회(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8426InBlock.dummy` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8426OutBlock.hname` | String | 20 |  |
| `t8426OutBlock.shcode` | String | 8 |  |
| `t8426OutBlock.expcode` | String | 12 |  |

### t8427 — 과거데이터시간대별조회

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8427InBlock.fo_gbn` | String | 1 | F:선물<br>O:옵션 |
| `t8427InBlock.yyyy` | String | 4 | YYYY |
| `t8427InBlock.mm` | String | 2 | MM |
| `t8427InBlock.cp_gbn` | String | 1 | 2:콜<br>3:풋 |
| `t8427InBlock.actprice` | Number | 6.2 |  |
| `t8427InBlock.focode` | String | 8 |  |
| `t8427InBlock.dt_gbn` | String | 1 | D:일<br>M:분 |
| `t8427InBlock.min_term` | String | 2 |  |
| `t8427InBlock.date` | String | 8 | 다음 조회시 OutBlock의 date 값 입력<br>처음 조회시 Space |
| `t8427InBlock.time` | String | 6 | 다음 조회시 OutBlock의 time 값 입력<br>처음 조회시 Space |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8427OutBlock.focode` | String | 8 |  |
| `t8427OutBlock.date` | String | 8 |  |
| `t8427OutBlock.time` | String | 6 |  |
| `t8427OutBlock1.date` | String | 8 |  |
| `t8427OutBlock1.time` | String | 6 |  |
| `t8427OutBlock1.open` | Number | 6.2 |  |
| `t8427OutBlock1.high` | Number | 6.2 |  |
| `t8427OutBlock1.low` | Number | 6.2 |  |
| `t8427OutBlock1.close` | Number | 6.2 |  |
| `t8427OutBlock1.sign` | String | 1 |  |
| `t8427OutBlock1.change` | Number | 6.2 |  |
| `t8427OutBlock1.diff` | Number | 6.2 |  |
| `t8427OutBlock1.volume` | Number | 12 |  |
| `t8427OutBlock1.diff_vol` | Number | 10.2 |  |
| `t8427OutBlock1.openyak` | Number | 8 |  |
| `t8427OutBlock1.openyakupdn` | Number | 8 |  |
| `t8427OutBlock1.value` | Number | 12 |  |

### t8467 — 지수선물마스터조회API용

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8467InBlock.gubun` | String | 1 | V:변동성지수선물<br>S:섹터지수선물<br>Q:코스닥150지수선물<br>그 이외의 값은 코스피200지수선물 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8467OutBlock.hname` | String | 20 |  |
| `t8467OutBlock.shcode` | String | 8 |  |
| `t8467OutBlock.expcode` | String | 12 |  |
| `t8467OutBlock.uplmtprice` | Number | 9.2 |  |
| `t8467OutBlock.dnlmtprice` | Number | 9.2 |  |
| `t8467OutBlock.jnilclose` | Number | 9.2 |  |
| `t8467OutBlock.jnilhigh` | Number | 9.2 |  |
| `t8467OutBlock.jnillow` | Number | 9.2 |  |
| `t8467OutBlock.recprice` | Number | 9.2 |  |

### t8433 — 지수옵션마스터조회API용

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8433InBlock.dummy` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8433OutBlock.hname` | String | 20 |  |
| `t8433OutBlock.shcode` | String | 8 |  |
| `t8433OutBlock.expcode` | String | 12 |  |
| `t8433OutBlock.hprice` | Number | 6.2 |  |
| `t8433OutBlock.lprice` | Number | 6.2 |  |
| `t8433OutBlock.jnilclose` | Number | 6.2 |  |
| `t8433OutBlock.jnilhigh` | Number | 6.2 |  |
| `t8433OutBlock.jnillow` | Number | 6.2 |  |
| `t8433OutBlock.recprice` | Number | 6.2 |  |

### t8434 — 선물/옵션멀티현재가조회

- 초당 호출 제한: 3

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8434InBlock.qrycnt` | Number | 3 | 최대50개까지 |
| `t8434InBlock.focode` | String | 400 | 구분자 없이 종목코드를 붙여서 입력 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8434OutBlock1.hname` | String | 20 |  |
| `t8434OutBlock1.price` | Number | 6.2 |  |
| `t8434OutBlock1.sign` | String | 1 |  |
| `t8434OutBlock1.change` | Number | 6.2 |  |
| `t8434OutBlock1.diff` | Number | 6.2 |  |
| `t8434OutBlock1.volume` | Number | 12 |  |
| `t8434OutBlock1.checnt` | Number | 8 |  |
| `t8434OutBlock1.focode` | String | 8 |  |

### t8435 — 파생종목마스터조회API용

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8435InBlock.gubun` | String | 2 | MF : 미니선물<br>MO : 미니옵션<br>WK : 코스피200위클리옵션<br>SF : 코스닥150선물<br>QW : 코스닥150위클리옵션 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8435OutBlock.hname` | String | 20 |  |
| `t8435OutBlock.shcode` | String | 8 |  |
| `t8435OutBlock.expcode` | String | 12 |  |
| `t8435OutBlock.uplmtprice` | Number | 6.2 |  |
| `t8435OutBlock.dnlmtprice` | Number | 6.2 |  |
| `t8435OutBlock.jnilclose` | Number | 6.2 |  |
| `t8435OutBlock.jnilhigh` | Number | 6.2 |  |
| `t8435OutBlock.jnillow` | Number | 6.2 |  |
| `t8435OutBlock.recprice` | Number | 6.2 |  |

### t9943 — 지수선물마스터조회API용

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t9943InBlock.gubun` | String | 1 | V:변동성지수선물<br>S:섹터지수선물<br>그 이외의 값은 코스피200지수선물 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t9943OutBlock.hname` | String | 20 |  |
| `t9943OutBlock.shcode` | String | 8 |  |
| `t9943OutBlock.expcode` | String | 12 |  |

### t9944 — 지수옵션마스터조회API용

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t9944InBlock.dummy` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t9944OutBlock.hname` | String | 20 |  |
| `t9944OutBlock.shcode` | String | 8 |  |
| `t9944OutBlock.expcode` | String | 12 |  |

### t8455 — KRX야간파생 마스터조회(API용)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8455InBlock.gubun` | String | 2 | - 선물 gubun<br>NFU : KOSPI200선물<br>NMF : 미니선물<br>NQF : 코스닥150선물<br>NCF : 상품선물<br>- 옵션 gubun<br>NOP : KOSPI200옵션<br>NMO : 미니옵션<br>NQO : 코스닥150옵션<br>NWO : 위클리옵션 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8455OutBlock.hname` | String | 20 |  |
| `t8455OutBlock.shcode` | String | 8 |  |
| `t8455OutBlock.expcode` | String | 12 |  |
| `t8455OutBlock.tradeunit` | Number | 21.8 |  |
| `t8455OutBlock.atmgb` | String | 1 |  |

### t8456 — KRX야간파생 시세조회(API용)

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8456InBlock.focode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8456OutBlock.hname` | String | 20 |  |
| `t8456OutBlock.price` | Number | 6.2 |  |
| `t8456OutBlock.sign` | String | 1 |  |
| `t8456OutBlock.change` | Number | 6.2 |  |
| `t8456OutBlock.jnilclose` | Number | 6.2 |  |
| `t8456OutBlock.diff` | Number | 6.2 |  |
| `t8456OutBlock.volume` | Number | 12 |  |
| `t8456OutBlock.value` | Number | 12 |  |
| `t8456OutBlock.open` | Number | 6.2 |  |
| `t8456OutBlock.high` | Number | 6.2 |  |
| `t8456OutBlock.low` | Number | 6.2 |  |
| `t8456OutBlock.recprice` | Number | 6.2 |  |
| `t8456OutBlock.theoryprice` | Number | 6.2 |  |
| `t8456OutBlock.actprice` | Number | 6.2 |  |
| `t8456OutBlock.impv` | Number | 6.2 |  |
| `t8456OutBlock.timevl` | Number | 6.2 |  |
| `t8456OutBlock.kospijisu` | Number | 6.2 |  |
| `t8456OutBlock.kospisign` | String | 1 |  |
| `t8456OutBlock.kospichange` | Number | 6.2 |  |
| `t8456OutBlock.kospidiff` | Number | 6.2 |  |
| `t8456OutBlock.cmeprice` | Number | 6.2 |  |
| `t8456OutBlock.cmesign` | String | 1 |  |
| `t8456OutBlock.cmechange` | Number | 6.2 |  |
| `t8456OutBlock.cmediff` | Number | 6.2 |  |
| `t8456OutBlock.cmefocode` | String | 8 |  |
| `t8456OutBlock.uplmtprice` | Number | 6.2 |  |
| `t8456OutBlock.dnlmtprice` | Number | 6.2 |  |
| `t8456OutBlock.focode` | String | 8 |  |
| `t8456OutBlock.yeprice` | Number | 6.2 |  |
| `t8456OutBlock.ysign` | String | 1 |  |
| `t8456OutBlock.ychange` | Number | 6.2 |  |
| `t8456OutBlock.ydiff` | Number | 6.2 |  |
| `t8456OutBlock.danhochk` | String | 1 |  |
| `t8456OutBlock.jnilvolume` | Number | 12 |  |
| `t8456OutBlock.jnilvalue` | Number | 12 |  |
| `t8456OutBlock.uplmtprice_3rd` | Number | 6.2 |  |
| `t8456OutBlock.dnlmtprice_3rd` | Number | 6.2 |  |
| `t8456OutBlock.ndv_uplmtprice` | Number | 6.2 |  |
| `t8456OutBlock.ndv_dnlmtprice` | Number | 6.2 |  |
| `t8456OutBlock.ndv_rt_uplmtprice` | Number | 6.2 |  |
| `t8456OutBlock.ndv_rt_dnlmtprice` | Number | 6.2 |  |

### t8457 — KRX야간파생 호가조회(API용)

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8457InBlock.shcode` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8457OutBlock.hname` | String | 20 |  |
| `t8457OutBlock.price` | Number | 6.2 |  |
| `t8457OutBlock.sign` | String | 1 |  |
| `t8457OutBlock.change` | Number | 6.2 |  |
| `t8457OutBlock.diff` | Number | 6.2 |  |
| `t8457OutBlock.volume` | Number | 12 |  |
| `t8457OutBlock.jnilclose` | Number | 6.2 |  |
| `t8457OutBlock.offerho1` | Number | 6.2 |  |
| `t8457OutBlock.bidho1` | Number | 6.2 |  |
| `t8457OutBlock.offerrem1` | Number | 8 |  |
| `t8457OutBlock.bidrem1` | Number | 8 |  |
| `t8457OutBlock.dcnt1` | Number | 8 |  |
| `t8457OutBlock.scnt1` | Number | 8 |  |
| `t8457OutBlock.offerho2` | Number | 6.2 |  |
| `t8457OutBlock.bidho2` | Number | 6.2 |  |
| `t8457OutBlock.offerrem2` | Number | 8 |  |
| `t8457OutBlock.bidrem2` | Number | 8 |  |
| `t8457OutBlock.dcnt2` | Number | 8 |  |
| `t8457OutBlock.scnt2` | Number | 8 |  |
| `t8457OutBlock.offerho3` | Number | 6.2 |  |
| `t8457OutBlock.bidho3` | Number | 6.2 |  |
| `t8457OutBlock.offerrem3` | Number | 8 |  |
| `t8457OutBlock.bidrem3` | Number | 8 |  |
| `t8457OutBlock.dcnt3` | Number | 8 |  |
| `t8457OutBlock.scnt3` | Number | 8 |  |
| `t8457OutBlock.offerho4` | Number | 6.2 |  |
| `t8457OutBlock.bidho4` | Number | 6.2 |  |
| `t8457OutBlock.offerrem4` | Number | 8 |  |
| `t8457OutBlock.bidrem4` | Number | 8 |  |
| `t8457OutBlock.dcnt4` | Number | 8 |  |
| `t8457OutBlock.scnt4` | Number | 8 |  |
| `t8457OutBlock.offerho5` | Number | 6.2 |  |
| `t8457OutBlock.bidho5` | Number | 6.2 |  |
| `t8457OutBlock.offerrem5` | Number | 8 |  |
| `t8457OutBlock.bidrem5` | Number | 8 |  |
| `t8457OutBlock.dcnt5` | Number | 8 |  |
| `t8457OutBlock.scnt5` | Number | 8 |  |
| `t8457OutBlock.dvol` | Number | 8 |  |
| `t8457OutBlock.svol` | Number | 8 |  |
| `t8457OutBlock.toffernum` | Number | 8 |  |
| `t8457OutBlock.tbidnum` | Number | 8 |  |
| `t8457OutBlock.time` | String | 6 |  |
| `t8457OutBlock.shcode` | String | 8 |  |

### t8458 — KRX야간파생 시간대별체결(API용)

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8458InBlock.focode` | String | 8 |  |
| `t8458InBlock.cvolume` | Number | 12 |  |
| `t8458InBlock.stime` | String | 4 |  |
| `t8458InBlock.etime` | String | 4 |  |
| `t8458InBlock.cts_time` | String | 10 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8458OutBlock.cts_time` | String | 10 |  |
| `t8458OutBlock1.chetime` | String | 10 |  |
| `t8458OutBlock1.price` | Number | 6.2 |  |
| `t8458OutBlock1.sign` | String | 1 |  |
| `t8458OutBlock1.change` | Number | 6.2 |  |
| `t8458OutBlock1.cvolume` | Number | 8 |  |
| `t8458OutBlock1.chdegree` | Number | 8.2 |  |
| `t8458OutBlock1.offerho` | Number | 6.2 |  |
| `t8458OutBlock1.bidho` | Number | 6.2 |  |
| `t8458OutBlock1.volume` | Number | 12 |  |
| `t8458OutBlock1.n_msvolume` | Number | 12 |  |
| `t8458OutBlock1.n_mdvolume` | Number | 12 |  |
| `t8458OutBlock1.s_msvolume` | Number | 12 |  |
| `t8458OutBlock1.n_mschecnt` | Number | 8 |  |
| `t8458OutBlock1.n_mdchecnt` | Number | 8 |  |
| `t8458OutBlock1.s_mschecnt` | Number | 8 |  |

### t8459 — KRX야간파생 기간별주가(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8459InBlock.shcode` | String | 8 |  |
| `t8459InBlock.futcheck` | String | 1 |  |
| `t8459InBlock.date` | String | 8 |  |
| `t8459InBlock.cts_code` | String | 8 |  |
| `t8459InBlock.lastdate` | String | 8 |  |
| `t8459InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8459OutBlock.date` | String | 8 |  |
| `t8459OutBlock.cts_code` | String | 8 |  |
| `t8459OutBlock.lastdate` | String | 8 |  |
| `t8459OutBlock.nowfutyn` | String | 1 |  |
| `t8459OutBlock1.date` | String | 8 |  |
| `t8459OutBlock1.open` | Number | 6.2 |  |
| `t8459OutBlock1.high` | Number | 6.2 |  |
| `t8459OutBlock1.low` | Number | 6.2 |  |
| `t8459OutBlock1.close` | Number | 6.2 |  |
| `t8459OutBlock1.sign` | String | 1 |  |
| `t8459OutBlock1.change` | Number | 6.2 |  |
| `t8459OutBlock1.diff` | Number | 6.2 |  |
| `t8459OutBlock1.volume` | Number | 12 |  |
| `t8459OutBlock1.diff_vol` | Number | 10.2 |  |

### t8460 — KRX야간파생 옵션 전광판

- 초당 호출 제한: 2

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8460InBlock.yyyymm` | String | 6 |  |
| `t8460InBlock.gubun` | String | 1 | M:미니<br>G:원지수<br>Q:코스닥<br>W:위클리 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8460OutBlock.gmprice` | Number | 6.2 |  |
| `t8460OutBlock.gmsign` | String | 1 |  |
| `t8460OutBlock.gmchange` | Number | 6.2 |  |
| `t8460OutBlock.gmdiff` | Number | 6.2 |  |
| `t8460OutBlock.gmvolume` | Number | 12 |  |
| `t8460OutBlock.gmshcode` | String | 8 |  |
| `t8460OutBlock1.actprice` | Number | 6.2 |  |
| `t8460OutBlock1.optcode` | String | 8 |  |
| `t8460OutBlock1.price` | Number | 6.2 |  |
| `t8460OutBlock1.sign` | String | 1 |  |
| `t8460OutBlock1.change` | Number | 6.2 |  |
| `t8460OutBlock1.diff` | Number | 6.2 |  |
| `t8460OutBlock1.volume` | Number | 12 |  |
| `t8460OutBlock1.offerho1` | Number | 6.2 |  |
| `t8460OutBlock1.bidho1` | Number | 6.2 |  |
| `t8460OutBlock1.cvolume` | Number | 12 |  |
| `t8460OutBlock1.impv` | Number | 6.2 |  |
| `t8460OutBlock1.timevl` | Number | 6.2 |  |
| `t8460OutBlock1.offerrem1` | Number | 12 |  |
| `t8460OutBlock1.bidrem1` | Number | 12 |  |
| `t8460OutBlock1.open` | Number | 6.2 |  |
| `t8460OutBlock1.high` | Number | 6.2 |  |
| `t8460OutBlock1.low` | Number | 6.2 |  |
| `t8460OutBlock1.atmgubun` | String | 1 |  |
| `t8460OutBlock1.jisuconv` | Number | 10.2 |  |
| `t8460OutBlock2.actprice` | Number | 6.2 |  |
| `t8460OutBlock2.optcode` | String | 8 |  |
| `t8460OutBlock2.price` | Number | 6.2 |  |
| `t8460OutBlock2.sign` | String | 1 |  |
| `t8460OutBlock2.change` | Number | 6.2 |  |
| `t8460OutBlock2.diff` | Number | 6.2 |  |
| `t8460OutBlock2.volume` | Number | 12 |  |
| `t8460OutBlock2.offerho1` | Number | 6.2 |  |
| `t8460OutBlock2.bidho1` | Number | 6.2 |  |
| `t8460OutBlock2.cvolume` | Number | 12 |  |
| `t8460OutBlock2.impv` | Number | 6.2 |  |
| `t8460OutBlock2.timevl` | Number | 6.2 |  |
| `t8460OutBlock2.offerrem1` | Number | 12 |  |
| `t8460OutBlock2.bidrem1` | Number | 12 |  |
| `t8460OutBlock2.open` | Number | 6.2 |  |
| `t8460OutBlock2.high` | Number | 6.2 |  |
| `t8460OutBlock2.low` | Number | 6.2 |  |
| `t8460OutBlock2.atmgubun` | String | 1 |  |
| `t8460OutBlock2.jisuconv` | Number | 10.2 |  |

## [선물/옵션] 실시간 시세

- 카테고리: 선물/옵션
- 프로토콜: WEBSOCKET
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/websocket`
- 설명: 선물옵션 주문현황 및 시세, 투자정보를 실시간으로 확인할 수 있습니다.

### C01 — 선물주문체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### CD0 — 상품선물실시간상하한가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### FC9 — KOSPI200선물체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### FD0 — KOSPI200선물실시간상하한가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### FH9 — KOSPI200선물호가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### FX9 — KOSPI200선물가격제한폭확대

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### H01 — 선물주문정정취소

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### JC0 — 주식선물체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### JD0 — 주식선물실시간상하한가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### JH0 — 주식선물호가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### JX0 — 주식선물가격제한폭확대

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### O01 — 선물접수

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### OC0 — KOSPI200옵션체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### OD0 — KOSPI200옵션실시간상하한가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### OH0 — KOSPI200옵션호가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### OMG — KOSPI200옵션민감도

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### OX0 — KOSPI200옵션가격제한폭확대

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### YC3 — 상품선물예상체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### YF9 — 지수선물예상체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### YJC — 주식선물예상체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### YOC — 지수옵션예상체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DC0 — KRX야간파생 체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### O02 — KRX야간파생 선물접수

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### C02 — KRX야간파생 선물체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DH0 — KRX야간파생 호가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### H02 — KRX야간파생 선물정정취소

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DD0 — KRX야간파생 실시간상하한가

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DX0 — KRX야간파생 가격제한폭확대

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DYC — KRX야간파생 예상체결

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DBM — KRX야간파생 투자자매매현황

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

### DBT — KRX야간파생 투자자별현황

- 초당 호출 제한: -

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

## [선물/옵션] 주문

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/order`
- 설명: 주간/야간 선물옵션 주문서비스를 확인할 수 있습니다

### CFOAT00100 — 선물옵션 정상주문

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00100InBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00100InBlock1.BnsTpCode` | String | 1 | 1@매도<br>2@매수 |
| `CFOAT00100InBlock1.FnoOrdprcPtnCode` | String | 2 | 00@지정가<br>03@시장가<br>05@조건부지정가<br>06@최유리지정가<br>10@지정가(IOC)<br>20@지정가(FOK)<br>13@시장가(IOC)<br>23@시장가(FOK)<br>16@최유리지정가(IOC)<br>26@최유리지정가(FOK) |
| `CFOAT00100InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAT00100InBlock1.OrdQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00100OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAT00100OutBlock1.OrdMktCode` | String | 2 |  |
| `CFOAT00100OutBlock1.AcntNo` | String | 20 |  |
| `CFOAT00100OutBlock1.Pwd` | String | 8 |  |
| `CFOAT00100OutBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00100OutBlock1.BnsTpCode` | String | 1 |  |
| `CFOAT00100OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CFOAT00100OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CFOAT00100OutBlock1.FnoTrdPtnCode` | String | 2 |  |
| `CFOAT00100OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAT00100OutBlock1.OrdQty` | Number | 16 |  |
| `CFOAT00100OutBlock1.CommdaCode` | String | 2 |  |
| `CFOAT00100OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CFOAT00100OutBlock1.GrpId` | String | 20 |  |
| `CFOAT00100OutBlock1.OrdSeqno` | Number | 10 |  |
| `CFOAT00100OutBlock1.PtflNo` | Number | 10 |  |
| `CFOAT00100OutBlock1.BskNo` | Number | 10 |  |
| `CFOAT00100OutBlock1.TrchNo` | Number | 10 |  |
| `CFOAT00100OutBlock1.ItemNo` | Number | 16 |  |
| `CFOAT00100OutBlock1.OpDrtnNo` | String | 12 |  |
| `CFOAT00100OutBlock1.MgempNo` | String | 9 |  |
| `CFOAT00100OutBlock1.FundId` | String | 12 |  |
| `CFOAT00100OutBlock1.FundOrdNo` | Number | 10 |  |
| `CFOAT00100OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAT00100OutBlock2.OrdNo` | Number | 10 |  |
| `CFOAT00100OutBlock2.BrnNm` | String | 40 |  |
| `CFOAT00100OutBlock2.AcntNm` | String | 40 |  |
| `CFOAT00100OutBlock2.IsuNm` | String | 50 |  |
| `CFOAT00100OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOAT00100OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOAT00100OutBlock2.OrdMgn` | Number | 16 |  |
| `CFOAT00100OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CFOAT00100OutBlock2.OrdAbleQty` | Number | 16 |  |

### CFOAT00200 — 선물옵션 정정주문

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00200InBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00200InBlock1.OrgOrdNo` | Number | 10 |  |
| `CFOAT00200InBlock1.FnoOrdprcPtnCode` | String | 2 | 00@지정가<br>03@시장가<br>05@조건부지정가<br>06@최유리지정가<br>10@지정가(IOC)<br>20@지정가(FOK)<br>13@시장가(IOC)<br>23@시장가(FOK)<br>16@최유리지정가(IOC)<br>26@최유리지정가(FOK) |
| `CFOAT00200InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAT00200InBlock1.MdfyQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00200OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAT00200OutBlock1.OrdMktCode` | String | 2 |  |
| `CFOAT00200OutBlock1.AcntNo` | String | 20 |  |
| `CFOAT00200OutBlock1.Pwd` | String | 8 |  |
| `CFOAT00200OutBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00200OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CFOAT00200OutBlock1.OrgOrdNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CFOAT00200OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CFOAT00200OutBlock1.MdfyQty` | Number | 16 |  |
| `CFOAT00200OutBlock1.CommdaCode` | String | 2 |  |
| `CFOAT00200OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CFOAT00200OutBlock1.GrpId` | String | 20 |  |
| `CFOAT00200OutBlock1.OrdSeqno` | Number | 10 |  |
| `CFOAT00200OutBlock1.PtflNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.BskNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.TrchNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.ItemNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.MgempNo` | String | 9 |  |
| `CFOAT00200OutBlock1.FundId` | String | 12 |  |
| `CFOAT00200OutBlock1.FundOrgOrdNo` | Number | 10 |  |
| `CFOAT00200OutBlock1.FundOrdNo` | Number | 10 |  |
| `CFOAT00200OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAT00200OutBlock2.OrdNo` | Number | 10 |  |
| `CFOAT00200OutBlock2.BrnNm` | String | 40 |  |
| `CFOAT00200OutBlock2.AcntNm` | String | 40 |  |
| `CFOAT00200OutBlock2.IsuNm` | String | 50 |  |
| `CFOAT00200OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOAT00200OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOAT00200OutBlock2.OrdMgn` | Number | 16 |  |
| `CFOAT00200OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CFOAT00200OutBlock2.OrdAbleQty` | Number | 16 |  |

### CFOAT00300 — 선물옵션 취소주문

- 초당 호출 제한: 10

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00300InBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00300InBlock1.OrgOrdNo` | Number | 10 |  |
| `CFOAT00300InBlock1.CancQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CFOAT00300OutBlock1.RecCnt` | Number | 5 |  |
| `CFOAT00300OutBlock1.OrdMktCode` | String | 2 |  |
| `CFOAT00300OutBlock1.AcntNo` | String | 20 |  |
| `CFOAT00300OutBlock1.Pwd` | String | 8 |  |
| `CFOAT00300OutBlock1.FnoIsuNo` | String | 12 |  |
| `CFOAT00300OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CFOAT00300OutBlock1.OrgOrdNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.CancQty` | Number | 16 |  |
| `CFOAT00300OutBlock1.CommdaCode` | String | 2 |  |
| `CFOAT00300OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CFOAT00300OutBlock1.GrpId` | String | 20 |  |
| `CFOAT00300OutBlock1.OrdSeqno` | Number | 10 |  |
| `CFOAT00300OutBlock1.PtflNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.BskNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.TrchNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.ItemNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.MgempNo` | String | 9 |  |
| `CFOAT00300OutBlock1.FundId` | String | 12 |  |
| `CFOAT00300OutBlock1.FundOrgOrdNo` | Number | 10 |  |
| `CFOAT00300OutBlock1.FundOrdNo` | Number | 10 |  |
| `CFOAT00300OutBlock2.RecCnt` | Number | 5 |  |
| `CFOAT00300OutBlock2.OrdNo` | Number | 10 |  |
| `CFOAT00300OutBlock2.BrnNm` | String | 40 |  |
| `CFOAT00300OutBlock2.AcntNm` | String | 40 |  |
| `CFOAT00300OutBlock2.IsuNm` | String | 50 |  |
| `CFOAT00300OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CFOAT00300OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CFOAT00300OutBlock2.OrdMgn` | Number | 16 |  |
| `CFOAT00300OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CFOAT00300OutBlock2.OrdAbleQty` | Number | 16 |  |

### CCENT00100 — KRX야간파생 위탁 신규 주문

- 초당 호출 제한: 5

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00100InBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00100InBlock1.BnsTpCode` | String | 1 | 1:매도<br>2:매수 |
| `CCENT00100InBlock1.FnoOrdprcPtnCode` | String | 2 | 00@지정가<br>03@시장가<br>05@조건부지정가<br>06@최유리지정가<br>10@지정가(IOC)<br>20@지정가(FOK)<br>13@시장가(IOC)<br>23@시장가(FOK)<br>16@최유리지정가(IOC)<br>26@최유리지정가(FOK) |
| `CCENT00100InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENT00100InBlock1.OrdQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00100OutBlock1.RecCnt` | Number | 5 |  |
| `CCENT00100OutBlock1.OrdMktCode` | String | 2 |  |
| `CCENT00100OutBlock1.AcntNo` | String | 20 |  |
| `CCENT00100OutBlock1.Pwd` | String | 8 |  |
| `CCENT00100OutBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00100OutBlock1.BnsTpCode` | String | 1 |  |
| `CCENT00100OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CCENT00100OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CCENT00100OutBlock1.FnoTrdPtnCode` | String | 2 |  |
| `CCENT00100OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENT00100OutBlock1.OrdQty` | Number | 16 |  |
| `CCENT00100OutBlock1.CommdaCode` | String | 2 |  |
| `CCENT00100OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CCENT00100OutBlock1.GrpId` | String | 20 |  |
| `CCENT00100OutBlock1.OrdSeqno` | Number | 10 |  |
| `CCENT00100OutBlock1.PtflNo` | Number | 10 |  |
| `CCENT00100OutBlock1.BskNo` | Number | 10 |  |
| `CCENT00100OutBlock1.TrchNo` | Number | 10 |  |
| `CCENT00100OutBlock1.ItemNo` | Number | 16 |  |
| `CCENT00100OutBlock1.OpDrtnNo` | String | 12 |  |
| `CCENT00100OutBlock1.MgempNo` | String | 9 |  |
| `CCENT00100OutBlock1.FundId` | String | 12 |  |
| `CCENT00100OutBlock1.FundOrdNo` | Number | 10 |  |
| `CCENT00100OutBlock2.RecCnt` | Number | 5 |  |
| `CCENT00100OutBlock2.OrdNo` | Number | 10 |  |
| `CCENT00100OutBlock2.BrnNm` | String | 40 |  |
| `CCENT00100OutBlock2.AcntNm` | String | 40 |  |
| `CCENT00100OutBlock2.IsuNm` | String | 50 |  |
| `CCENT00100OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CCENT00100OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CCENT00100OutBlock2.OrdMgn` | Number | 16 |  |
| `CCENT00100OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CCENT00100OutBlock2.OrdAbleQty` | Number | 16 |  |

### CCENT00200 — KRX야간파생 위탁 정정 주문

- 초당 호출 제한: 5

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00200InBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00200InBlock1.OrgOrdNo` | Number | 10 |  |
| `CCENT00200InBlock1.FnoOrdprcPtnCode` | String | 2 | 00@지정가<br>03@시장가<br>05@조건부지정가<br>06@최유리지정가<br>10@지정가(IOC)<br>20@지정가(FOK)<br>13@시장가(IOC)<br>23@시장가(FOK)<br>16@최유리지정가(IOC)<br>26@최유리지정가(FOK) |
| `CCENT00200InBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENT00200InBlock1.MdfyQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00200OutBlock1.RecCnt` | Number | 5 |  |
| `CCENT00200OutBlock1.OrdMktCode` | String | 2 |  |
| `CCENT00200OutBlock1.AcntNo` | String | 20 |  |
| `CCENT00200OutBlock1.Pwd` | String | 8 |  |
| `CCENT00200OutBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00200OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CCENT00200OutBlock1.OrgOrdNo` | Number | 10 |  |
| `CCENT00200OutBlock1.FnoOrdprcPtnCode` | String | 2 |  |
| `CCENT00200OutBlock1.FnoOrdPrc` | Number | 27.8 |  |
| `CCENT00200OutBlock1.MdfyQty` | Number | 16 |  |
| `CCENT00200OutBlock1.CommdaCode` | String | 2 |  |
| `CCENT00200OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CCENT00200OutBlock1.GrpId` | String | 20 |  |
| `CCENT00200OutBlock1.OrdSeqno` | Number | 10 |  |
| `CCENT00200OutBlock1.PtflNo` | Number | 10 |  |
| `CCENT00200OutBlock1.BskNo` | Number | 10 |  |
| `CCENT00200OutBlock1.TrchNo` | Number | 10 |  |
| `CCENT00200OutBlock1.ItemNo` | Number | 10 |  |
| `CCENT00200OutBlock1.MgempNo` | String | 9 |  |
| `CCENT00200OutBlock1.FundId` | String | 12 |  |
| `CCENT00200OutBlock1.FundOrgOrdNo` | Number | 10 |  |
| `CCENT00200OutBlock1.FundOrdNo` | Number | 10 |  |
| `CCENT00200OutBlock2.RecCnt` | Number | 5 |  |
| `CCENT00200OutBlock2.OrdNo` | Number | 10 |  |
| `CCENT00200OutBlock2.BrnNm` | String | 40 |  |
| `CCENT00200OutBlock2.AcntNm` | String | 40 |  |
| `CCENT00200OutBlock2.IsuNm` | String | 50 |  |
| `CCENT00200OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CCENT00200OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CCENT00200OutBlock2.OrdMgn` | Number | 16 |  |
| `CCENT00200OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CCENT00200OutBlock2.OrdAbleQty` | Number | 16 |  |

### CCENT00300 — KRX야간파생 위탁 취소 주문

- 초당 호출 제한: 5

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00300InBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00300InBlock1.OrgOrdNo` | Number | 10 |  |
| `CCENT00300InBlock1.CancQty` | Number | 16 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `CCENT00300OutBlock1.RecCnt` | Number | 5 |  |
| `CCENT00300OutBlock1.OrdMktCode` | String | 2 |  |
| `CCENT00300OutBlock1.AcntNo` | String | 20 |  |
| `CCENT00300OutBlock1.Pwd` | String | 8 |  |
| `CCENT00300OutBlock1.FnoIsuNo` | String | 12 |  |
| `CCENT00300OutBlock1.FnoOrdPtnCode` | String | 2 |  |
| `CCENT00300OutBlock1.OrgOrdNo` | Number | 10 |  |
| `CCENT00300OutBlock1.CancQty` | Number | 16 |  |
| `CCENT00300OutBlock1.CommdaCode` | String | 2 |  |
| `CCENT00300OutBlock1.DscusBnsCmpltTime` | String | 9 |  |
| `CCENT00300OutBlock1.GrpId` | String | 20 |  |
| `CCENT00300OutBlock1.OrdSeqno` | Number | 10 |  |
| `CCENT00300OutBlock1.PtflNo` | Number | 10 |  |
| `CCENT00300OutBlock1.BskNo` | Number | 10 |  |
| `CCENT00300OutBlock1.TrchNo` | Number | 10 |  |
| `CCENT00300OutBlock1.ItemNo` | Number | 10 |  |
| `CCENT00300OutBlock1.MgempNo` | String | 9 |  |
| `CCENT00300OutBlock1.FundId` | String | 12 |  |
| `CCENT00300OutBlock1.FundOrgOrdNo` | Number | 10 |  |
| `CCENT00300OutBlock1.FundOrdNo` | Number | 10 |  |
| `CCENT00300OutBlock2.RecCnt` | Number | 5 |  |
| `CCENT00300OutBlock2.OrdNo` | Number | 10 |  |
| `CCENT00300OutBlock2.BrnNm` | String | 40 |  |
| `CCENT00300OutBlock2.AcntNm` | String | 40 |  |
| `CCENT00300OutBlock2.IsuNm` | String | 50 |  |
| `CCENT00300OutBlock2.OrdAbleAmt` | Number | 16 |  |
| `CCENT00300OutBlock2.MnyOrdAbleAmt` | Number | 16 |  |
| `CCENT00300OutBlock2.OrdMgn` | Number | 16 |  |
| `CCENT00300OutBlock2.MnyOrdMgn` | Number | 16 |  |
| `CCENT00300OutBlock2.OrdAbleQty` | Number | 16 |  |

## [선물/옵션] 차트

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/chart`
- 설명: 주간/야간 선물옵션 기간별 차트를 확인할 수 있습니다.

### t2216 — 선물옵션틱분별체결조회차트

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2216InBlock.focode` | String | 8 |  |
| `t2216InBlock.cgubun` | String | 1 | T:틱차트<br>B:분차트 |
| `t2216InBlock.bgubun` | Number | 3 | 차트구분이 'B'일때만 체크<br>0: 30초<br>0초과 : n분 |
| `t2216InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2216OutBlock1.chetime` | String | 10 |  |
| `t2216OutBlock1.price` | Number | 9.2 |  |
| `t2216OutBlock1.sign` | String | 1 |  |
| `t2216OutBlock1.change` | Number | 9.2 |  |
| `t2216OutBlock1.open` | Number | 9.2 |  |
| `t2216OutBlock1.high` | Number | 9.2 |  |
| `t2216OutBlock1.low` | Number | 9.2 |  |
| `t2216OutBlock1.volume` | Number | 12 |  |
| `t2216OutBlock1.value` | Number | 12 |  |
| `t2216OutBlock1.openyak` | Number | 8 |  |
| `t2216OutBlock1.openupdn` | Number | 8 |  |
| `t2216OutBlock1.cvolume` | Number | 8 |  |
| `t2216OutBlock1.s_mschecnt` | Number | 8 |  |
| `t2216OutBlock1.s_mdchecnt` | Number | 8 |  |
| `t2216OutBlock1.ss_mschecnt` | Number | 8 |  |
| `t2216OutBlock1.s_mschevol` | Number | 12 |  |
| `t2216OutBlock1.s_mdchevol` | Number | 12 |  |
| `t2216OutBlock1.ss_mschevol` | Number | 12 |  |
| `t2216OutBlock1.chdegvol` | Number | 8.2 |  |
| `t2216OutBlock1.chdegcnt` | Number | 8.2 |  |

### t8464 — 선물옵션차트(틱/n틱)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8464InBlock.shcode` | String | 8 |  |
| `t8464InBlock.ncnt` | Number | 4 |  |
| `t8464InBlock.qrycnt` | Number | 4 | 요청건수<br><br>압축모듈인 경우 최대 2000건까지 조회가능.<br>비압축인 경우 최대 500건까지 조회가능 |
| `t8464InBlock.nday` | String | 1 | 0:미사용 |
| `t8464InBlock.sdate` | String | 8 | 기본값 : Space<br>(edate(필수입력) 기준으로 qrycnt 만큼 조회)<br><br>조회구간을 설정하여 필터링 하고 싶은 경우 입력 |
| `t8464InBlock.stime` | String | 6 |  |
| `t8464InBlock.edate` | String | 8 | 처음조회기준일(LE)<br>처음조회일 경우 이 값 기준으로 조회<br>("99999999" 혹은 '당일') |
| `t8464InBlock.etime` | String | 6 |  |
| `t8464InBlock.cts_date` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정 |
| `t8464InBlock.cts_time` | String | 10 | N:비압축 |
| `t8464InBlock.comp_yn` | String | 1 | N:비압축 모듈<br>Y: 압 축 모듈 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8464OutBlock.shcode` | String | 8 |  |
| `t8464OutBlock.jisiga` | Number | 9.2 |  |
| `t8464OutBlock.jihigh` | Number | 9.2 |  |
| `t8464OutBlock.jilow` | Number | 9.2 |  |
| `t8464OutBlock.jiclose` | Number | 9.2 |  |
| `t8464OutBlock.jivolume` | Number | 12 |  |
| `t8464OutBlock.disiga` | Number | 9.2 |  |
| `t8464OutBlock.dihigh` | Number | 9.2 |  |
| `t8464OutBlock.dilow` | Number | 9.2 |  |
| `t8464OutBlock.diclose` | Number | 9.2 |  |
| `t8464OutBlock.highend` | Number | 9.2 |  |
| `t8464OutBlock.lowend` | Number | 9.2 |  |
| `t8464OutBlock.cts_date` | String | 8 |  |
| `t8464OutBlock.cts_time` | String | 10 |  |
| `t8464OutBlock.s_time` | String | 6 |  |
| `t8464OutBlock.e_time` | String | 6 |  |
| `t8464OutBlock.dshmin` | String | 2 |  |
| `t8464OutBlock.rec_count` | Number | 7 |  |
| `t8464OutBlock1.date` | String | 8 |  |
| `t8464OutBlock1.time` | String | 10 |  |
| `t8464OutBlock1.open` | Number | 9.2 |  |
| `t8464OutBlock1.high` | Number | 9.2 |  |
| `t8464OutBlock1.low` | Number | 9.2 |  |
| `t8464OutBlock1.close` | Number | 9.2 |  |
| `t8464OutBlock1.jdiff_vol` | Number | 12 |  |
| `t8464OutBlock1.openyak` | Number | 12 |  |

### t8465 — 선물/옵션차트(N분)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8465InBlock.shcode` | String | 8 |  |
| `t8465InBlock.ncnt` | Number | 4 | 0:30초<br>1: 1분<br>2: 2분<br>.....<br>n: n분 |
| `t8465InBlock.qrycnt` | Number | 4 | 요청건수<br><br>압축모듈인 경우 최대 2000건까지 조회가능.<br>비압축인 경우 최대 500건까지 조회가능 |
| `t8465InBlock.nday` | String | 1 | 0:미사용 |
| `t8465InBlock.sdate` | String | 8 | 기본값 : Space<br>(edate(필수입력) 기준으로 qrycnt 만큼 조회)<br><br>조회구간을 설정하여 필터링 하고 싶은 경우 입력 |
| `t8465InBlock.stime` | String | 6 |  |
| `t8465InBlock.edate` | String | 8 | 처음조회기준일(LE)<br>처음조회일 경우 이 값 기준으로 조회<br>("99999999" 혹은 '당일') |
| `t8465InBlock.etime` | String | 6 |  |
| `t8465InBlock.cts_date` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정 |
| `t8465InBlock.cts_time` | String | 10 |  |
| `t8465InBlock.comp_yn` | String | 1 | N:비압축 모듈<br>Y: 압 축 모듈 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8465OutBlock.shcode` | String | 8 |  |
| `t8465OutBlock.jisiga` | Number | 9.2 |  |
| `t8465OutBlock.jihigh` | Number | 9.2 |  |
| `t8465OutBlock.jilow` | Number | 9.2 |  |
| `t8465OutBlock.jiclose` | Number | 9.2 |  |
| `t8465OutBlock.jivolume` | Number | 12 |  |
| `t8465OutBlock.disiga` | Number | 9.2 |  |
| `t8465OutBlock.dihigh` | Number | 9.2 |  |
| `t8465OutBlock.dilow` | Number | 9.2 |  |
| `t8465OutBlock.diclose` | Number | 9.2 |  |
| `t8465OutBlock.highend` | Number | 9.2 |  |
| `t8465OutBlock.lowend` | Number | 9.2 |  |
| `t8465OutBlock.cts_date` | String | 8 |  |
| `t8465OutBlock.cts_time` | String | 10 |  |
| `t8465OutBlock.s_time` | String | 6 |  |
| `t8465OutBlock.e_time` | String | 6 |  |
| `t8465OutBlock.dshmin` | String | 2 |  |
| `t8465OutBlock.rec_count` | Number | 7 |  |
| `t8465OutBlock1.date` | String | 8 |  |
| `t8465OutBlock1.time` | String | 10 |  |
| `t8465OutBlock1.open` | Number | 9.2 |  |
| `t8465OutBlock1.high` | Number | 9.2 |  |
| `t8465OutBlock1.low` | Number | 9.2 |  |
| `t8465OutBlock1.close` | Number | 9.2 |  |
| `t8465OutBlock1.jdiff_vol` | Number | 12 |  |
| `t8465OutBlock1.value` | Number | 12 |  |
| `t8465OutBlock1.openyak` | Number | 12 |  |

### t8466 — 선물/옵션차트(일주월)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8466InBlock.shcode` | String | 8 |  |
| `t8466InBlock.gubun` | String | 1 |  |
| `t8466InBlock.qrycnt` | Number | 4 | 요청건수<br><br>압축모듈인 경우 최대 2000건까지 조회가능.<br>비압축인 경우 최대 500건까지 조회가능 |
| `t8466InBlock.sdate` | String | 8 | 기본값 : Space<br>(edate(필수입력) 기준으로 qrycnt 만큼 조회)<br><br>조회구간을 설정하여 필터링 하고 싶은 경우 입력 |
| `t8466InBlock.edate` | String | 8 | 처음조회기준일(LE)<br>처음조회일 경우 이 값 기준으로 조회<br>("99999999" 혹은 '당일') |
| `t8466InBlock.cts_date` | String | 8 | 처음 조회시는 Space<br>연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정 |
| `t8466InBlock.comp_yn` | String | 1 | N:비압축 모듈<br>Y: 압 축 모듈 |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8466OutBlock.shcode` | String | 8 |  |
| `t8466OutBlock.jisiga` | Number | 9.2 |  |
| `t8466OutBlock.jihigh` | Number | 9.2 |  |
| `t8466OutBlock.jilow` | Number | 9.2 |  |
| `t8466OutBlock.jiclose` | Number | 9.2 |  |
| `t8466OutBlock.jivolume` | Number | 12 |  |
| `t8466OutBlock.disiga` | Number | 9.2 |  |
| `t8466OutBlock.dihigh` | Number | 9.2 |  |
| `t8466OutBlock.dilow` | Number | 9.2 |  |
| `t8466OutBlock.diclose` | Number | 9.2 |  |
| `t8466OutBlock.highend` | Number | 9.2 |  |
| `t8466OutBlock.lowend` | Number | 9.2 |  |
| `t8466OutBlock.cts_date` | String | 8 |  |
| `t8466OutBlock.s_time` | String | 6 |  |
| `t8466OutBlock.e_time` | String | 6 |  |
| `t8466OutBlock.dshmin` | String | 2 |  |
| `t8466OutBlock.rec_count` | Number | 7 |  |
| `t8466OutBlock1.date` | String | 8 |  |
| `t8466OutBlock1.open` | Number | 9.2 |  |
| `t8466OutBlock1.high` | Number | 9.2 |  |
| `t8466OutBlock1.low` | Number | 9.2 |  |
| `t8466OutBlock1.close` | Number | 9.2 |  |
| `t8466OutBlock1.jdiff_vol` | Number | 12 |  |
| `t8466OutBlock1.value` | Number | 12 |  |
| `t8466OutBlock1.openyak` | Number | 12 |  |

### t8461 — KRX야간파생 틱분별조회(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8461InBlock.focode` | String | 8 |  |
| `t8461InBlock.cgubun` | String | 1 | T:틱차트<br>B:분차트 |
| `t8461InBlock.bgubun` | Number | 3 | 차트구분이 'B'일때만 체크<br>0: 30초<br>0초과 : n분 |
| `t8461InBlock.cnt` | Number | 3 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8461OutBlock1.chetime` | String | 10 |  |
| `t8461OutBlock1.price` | Number | 6.2 |  |
| `t8461OutBlock1.sign` | String | 1 |  |
| `t8461OutBlock1.change` | Number | 6.2 |  |
| `t8461OutBlock1.open` | Number | 6.2 |  |
| `t8461OutBlock1.high` | Number | 6.2 |  |
| `t8461OutBlock1.low` | Number | 6.2 |  |
| `t8461OutBlock1.volume` | Number | 12 |  |
| `t8461OutBlock1.cvolume` | Number | 8 |  |
| `t8461OutBlock1.s_mschecnt` | Number | 8 |  |
| `t8461OutBlock1.s_mdchecnt` | Number | 8 |  |
| `t8461OutBlock1.ss_mschecnt` | Number | 8 |  |
| `t8461OutBlock1.s_mschevol` | Number | 12 |  |
| `t8461OutBlock1.s_mdchevol` | Number | 12 |  |
| `t8461OutBlock1.ss_mschevol` | Number | 12 |  |
| `t8461OutBlock1.chdegvol` | Number | 8.2 |  |
| `t8461OutBlock1.chdegcnt` | Number | 8.2 |  |

## [선물/옵션] 투자자

- 카테고리: 선물/옵션
- 프로토콜: REST
- 메서드: POST
- 콘텐츠 타입: 
- 경로: `/futureoption/investor`
- 설명: 상품선물 투자자별 데이터를 확인할 수 있습니다.

### t2541 — 상품선물투자자매매동향(실시간)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2541InBlock.eitem` | String | 2 | 01@KTB<br>02@5TB<br>03@LKTB<br>04@USD<br>05@JPY<br>06@EUR<br>07@GOLD<br>08@LH<br>09@MGD |
| `t2541InBlock.market` | String | 1 | 0@선물<br>1@콜<br>2@풋 |
| `t2541InBlock.upcode` | String | 3 |  |
| `t2541InBlock.gubun1` | String | 1 |  |
| `t2541InBlock.gubun2` | String | 1 |  |
| `t2541InBlock.cts_time` | String | 8 |  |
| `t2541InBlock.cts_idx` | Number | 4 |  |
| `t2541InBlock.cnt` | Number | 4 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2541OutBlock.eitem` | String | 2 |  |
| `t2541OutBlock.sgubun` | String | 1 |  |
| `t2541OutBlock.cts_time` | String | 8 |  |
| `t2541OutBlock.tjjcode_08` | String | 4 |  |
| `t2541OutBlock.ms_08` | Number | 12 |  |
| `t2541OutBlock.md_08` | Number | 12 |  |
| `t2541OutBlock.rate_08` | Number | 12 |  |
| `t2541OutBlock.svolume_08` | Number | 12 |  |
| `t2541OutBlock.jjcode_17` | String | 4 |  |
| `t2541OutBlock.ms_17` | Number | 12 |  |
| `t2541OutBlock.md_17` | Number | 12 |  |
| `t2541OutBlock.rate_17` | Number | 12 |  |
| `t2541OutBlock.svolume_17` | Number | 12 |  |
| `t2541OutBlock.jjcode_18` | String | 4 |  |
| `t2541OutBlock.ms_18` | Number | 12 |  |
| `t2541OutBlock.md_18` | Number | 12 |  |
| `t2541OutBlock.rate_18` | Number | 12 |  |
| `t2541OutBlock.svolume_18` | Number | 12 |  |
| `t2541OutBlock.jjcode_01` | String | 4 |  |
| `t2541OutBlock.ms_01` | Number | 12 |  |
| `t2541OutBlock.md_01` | Number | 12 |  |
| `t2541OutBlock.rate_01` | Number | 12 |  |
| `t2541OutBlock.svolume_01` | Number | 12 |  |
| `t2541OutBlock.jjcode_03` | String | 4 |  |
| `t2541OutBlock.ms_03` | Number | 12 |  |
| `t2541OutBlock.md_03` | Number | 12 |  |
| `t2541OutBlock.rate_03` | Number | 12 |  |
| `t2541OutBlock.svolume_03` | Number | 12 |  |
| `t2541OutBlock.jjcode_04` | String | 4 |  |
| `t2541OutBlock.ms_04` | Number | 12 |  |
| `t2541OutBlock.md_04` | Number | 12 |  |
| `t2541OutBlock.rate_04` | Number | 12 |  |
| `t2541OutBlock.svolume_04` | Number | 12 |  |
| `t2541OutBlock.jjcode_02` | String | 4 |  |
| `t2541OutBlock.ms_02` | Number | 12 |  |
| `t2541OutBlock.md_02` | Number | 12 |  |
| `t2541OutBlock.rate_02` | Number | 12 |  |
| `t2541OutBlock.svolume_02` | Number | 12 |  |
| `t2541OutBlock.jjcode_05` | String | 4 |  |
| `t2541OutBlock.ms_05` | Number | 12 |  |
| `t2541OutBlock.md_05` | Number | 12 |  |
| `t2541OutBlock.rate_05` | Number | 12 |  |
| `t2541OutBlock.svolume_05` | Number | 12 |  |
| `t2541OutBlock.jjcode_06` | String | 4 |  |
| `t2541OutBlock.ms_06` | Number | 12 |  |
| `t2541OutBlock.md_06` | Number | 12 |  |
| `t2541OutBlock.rate_06` | Number | 12 |  |
| `t2541OutBlock.svolume_06` | Number | 12 |  |
| `t2541OutBlock.jjcode_07` | String | 4 |  |
| `t2541OutBlock.ms_07` | Number | 12 |  |
| `t2541OutBlock.md_07` | Number | 12 |  |
| `t2541OutBlock.rate_07` | Number | 12 |  |
| `t2541OutBlock.svolume_07` | Number | 12 |  |
| `t2541OutBlock.jjcode_11` | String | 4 |  |
| `t2541OutBlock.ms_11` | Number | 12 |  |
| `t2541OutBlock.md_11` | Number | 12 |  |
| `t2541OutBlock.rate_11` | Number | 12 |  |
| `t2541OutBlock.svolume_11` | Number | 12 |  |
| `t2541OutBlock.jjcode_00` | String | 4 |  |
| `t2541OutBlock.ms_00` | Number | 12 |  |
| `t2541OutBlock.md_00` | Number | 12 |  |
| `t2541OutBlock.rate_00` | Number | 12 |  |
| `t2541OutBlock.svolume_00` | Number | 12 |  |
| `t2541OutBlock1.time` | String | 8 |  |
| `t2541OutBlock1.sv_08` | Number | 12 |  |
| `t2541OutBlock1.sv_17` | Number | 12 |  |
| `t2541OutBlock1.sv_18` | Number | 12 |  |
| `t2541OutBlock1.sv_01` | Number | 12 |  |
| `t2541OutBlock1.sv_03` | Number | 12 |  |
| `t2541OutBlock1.sv_04` | Number | 12 |  |
| `t2541OutBlock1.sv_02` | Number | 12 |  |
| `t2541OutBlock1.sv_05` | Number | 12 |  |
| `t2541OutBlock1.sv_06` | Number | 12 |  |
| `t2541OutBlock1.sv_07` | Number | 12 |  |
| `t2541OutBlock1.sv_11` | Number | 12 |  |
| `t2541OutBlock1.sv_00` | Number | 12 |  |

### t2545 — 상품선물투자자매매동향(챠트용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2545InBlock.eitem` | String | 2 | 01@KTB<br>02@5TB<br>03@LKTB<br>04@USD<br>05@JPY<br>06@EUR<br>07@GOLD<br>08@LH<br>09@MGD |
| `t2545InBlock.sgubun` | String | 1 | 0@선물<br>1@콜<br>2@풋 |
| `t2545InBlock.upcode` | String | 3 |  |
| `t2545InBlock.nmin` | Object | 2 |  |
| `t2545InBlock.cnt` | Number | 3 |  |
| `t2545InBlock.bgubun` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t2545OutBlock.eitem` | String | 2 |  |
| `t2545OutBlock.sgubun` | String | 1 |  |
| `t2545OutBlock.indcode` | String | 4 |  |
| `t2545OutBlock.forcode` | String | 4 |  |
| `t2545OutBlock.syscode` | String | 4 |  |
| `t2545OutBlock.stocode` | String | 4 |  |
| `t2545OutBlock.invcode` | String | 4 |  |
| `t2545OutBlock.bancode` | String | 4 |  |
| `t2545OutBlock.inscode` | String | 4 |  |
| `t2545OutBlock.fincode` | String | 4 |  |
| `t2545OutBlock.moncode` | String | 4 |  |
| `t2545OutBlock.etccode` | String | 4 |  |
| `t2545OutBlock.natcode` | String | 4 |  |
| `t2545OutBlock.pefcode` | String | 4 |  |
| `t2545OutBlock.jisucd` | String | 8 |  |
| `t2545OutBlock.jisunm` | String | 20 |  |
| `t2545OutBlock1.date` | String | 8 |  |
| `t2545OutBlock1.time` | String | 6 |  |
| `t2545OutBlock1.datetime` | String | 14 |  |
| `t2545OutBlock1.indmsvol` | Number | 8 |  |
| `t2545OutBlock1.indmsamt` | Number | 12 |  |
| `t2545OutBlock1.formsvol` | Number | 8 |  |
| `t2545OutBlock1.formsamt` | Number | 12 |  |
| `t2545OutBlock1.sysmsvol` | Number | 8 |  |
| `t2545OutBlock1.sysmsamt` | Number | 12 |  |
| `t2545OutBlock1.stomsvol` | Number | 8 |  |
| `t2545OutBlock1.stomsamt` | Number | 12 |  |
| `t2545OutBlock1.invmsvol` | Number | 8 |  |
| `t2545OutBlock1.invmsamt` | Number | 12 |  |
| `t2545OutBlock1.banmsvol` | Number | 8 |  |
| `t2545OutBlock1.banmsamt` | Number | 12 |  |
| `t2545OutBlock1.insmsvol` | Number | 8 |  |
| `t2545OutBlock1.insmsamt` | Number | 12 |  |
| `t2545OutBlock1.finmsvol` | Number | 8 |  |
| `t2545OutBlock1.finmsamt` | Number | 12 |  |
| `t2545OutBlock1.monmsvol` | Number | 8 |  |
| `t2545OutBlock1.monmsamt` | Number | 12 |  |
| `t2545OutBlock1.etcmsvol` | Number | 8 |  |
| `t2545OutBlock1.etcmsamt` | Number | 12 |  |
| `t2545OutBlock1.natmsvol` | Number | 8 |  |
| `t2545OutBlock1.natmsamt` | Number | 12 |  |
| `t2545OutBlock1.pefmsvol` | Number | 8 |  |
| `t2545OutBlock1.pefmsamt` | Number | 12 |  |
| `t2545OutBlock1.upclose` | Number | 6.2 |  |
| `t2545OutBlock1.upcvolume` | Number | 8 |  |
| `t2545OutBlock1.upvolume` | Number | 12 |  |
| `t2545OutBlock1.upvalue` | Number | 12 |  |

### t8462 — KRX야간파생 투자자기간별(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8462InBlock.tm_rng` | String | 1 |  |
| `t8462InBlock.fot_clsf_cd` | String | 1 | F : 선물<br>C : 콜옵션<br>P : 풋옵션<br>S : 스프레드 |
| `t8462InBlock.bsc_asts_id` | String | 3 | K2I : KP200선물/옵션<br>MKI : 미니KP200선물/옵션<br>KQI : 코스닥150선물/옵션<br>WKM : 위클리옵션-월<br>WKI : 위클리옵션-목<br>BM3 : 국채3년선물<br>BMA : 국채10년선물<br>USD : 미국달러선물 |
| `t8462InBlock.gubun2` | String | 1 |  |
| `t8462InBlock.gubun3` | String | 1 |  |
| `t8462InBlock.from_date` | String | 8 |  |
| `t8462InBlock.to_date` | String | 8 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8462OutBlock.tm_rng` | String | 1 |  |
| `t8462OutBlock.fot_clsf_cd` | String | 1 |  |
| `t8462OutBlock.bsc_asts_id` | String | 3 |  |
| `t8462OutBlock1.date` | String | 8 |  |
| `t8462OutBlock1.sv_08` | Number | 12 |  |
| `t8462OutBlock1.sv_17` | Number | 12 |  |
| `t8462OutBlock1.sv_18` | Number | 12 |  |
| `t8462OutBlock1.sv_01` | Number | 12 |  |
| `t8462OutBlock1.sv_03` | Number | 12 |  |
| `t8462OutBlock1.sv_04` | Number | 12 |  |
| `t8462OutBlock1.sv_02` | Number | 12 |  |
| `t8462OutBlock1.sv_05` | Number | 12 |  |
| `t8462OutBlock1.sv_06` | Number | 12 |  |
| `t8462OutBlock1.sv_07` | Number | 12 |  |
| `t8462OutBlock1.sv_15` | Number | 12 |  |
| `t8462OutBlock1.sv_00` | Number | 12 |  |
| `t8462OutBlock1.sa_08` | Number | 12 |  |
| `t8462OutBlock1.sa_17` | Number | 12 |  |
| `t8462OutBlock1.sa_18` | Number | 12 |  |
| `t8462OutBlock1.sa_01` | Number | 12 |  |
| `t8462OutBlock1.sa_03` | Number | 12 |  |
| `t8462OutBlock1.sa_04` | Number | 12 |  |
| `t8462OutBlock1.sa_02` | Number | 12 |  |
| `t8462OutBlock1.sa_05` | Number | 12 |  |
| `t8462OutBlock1.sa_06` | Number | 12 |  |
| `t8462OutBlock1.sa_07` | Number | 12 |  |
| `t8462OutBlock1.sa_15` | Number | 12 |  |
| `t8462OutBlock1.sa_00` | Number | 12 |  |

### t8463 — KRX야간파생 투자자시간대별(API용)

- 초당 호출 제한: 1

#### 요청 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 요청 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8463InBlock.tm_rng` | String | 1 |  |
| `t8463InBlock.fot_clsf_cd` | String | 1 | F : 선물<br>C : 콜옵션<br>P : 풋옵션<br>S : 스프레드 |
| `t8463InBlock.bsc_asts_id` | String | 3 | K2I : KP200선물/옵션<br>MKI : 미니KP200선물/옵션<br>KQI : 코스닥150선물/옵션<br>WKM : 위클리옵션-월<br>WKI : 위클리옵션-목<br>BM3 : 국채3년선물<br>BMA : 국채10년선물<br>USD : 미국달러선물 |
| `t8463InBlock.cnt` | Number | 3 |  |
| `t8463InBlock.bgubun` | String | 1 |  |

#### 응답 헤더

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| 명세에 필드 없음 | | | |

#### 응답 본문

| 필드 경로 | 자료형 | 길이 | 설명 |
|---|---|---:|---|
| `t8463OutBlock.tm_rng` | String | 1 |  |
| `t8463OutBlock.fot_clsf_cd` | String | 1 |  |
| `t8463OutBlock.indcode` | String | 4 |  |
| `t8463OutBlock.forcode` | String | 4 |  |
| `t8463OutBlock.syscode` | String | 4 |  |
| `t8463OutBlock.stocode` | String | 4 |  |
| `t8463OutBlock.invcode` | String | 4 |  |
| `t8463OutBlock.bancode` | String | 4 |  |
| `t8463OutBlock.inscode` | String | 4 |  |
| `t8463OutBlock.fincode` | String | 4 |  |
| `t8463OutBlock.moncode` | String | 4 |  |
| `t8463OutBlock.etccode` | String | 4 |  |
| `t8463OutBlock.natcode` | String | 4 |  |
| `t8463OutBlock.pefcode` | String | 4 |  |
| `t8463OutBlock1.date` | String | 8 |  |
| `t8463OutBlock1.time` | String | 6 |  |
| `t8463OutBlock1.datetime` | String | 14 |  |
| `t8463OutBlock1.bsc_asts_id` | String | 3 |  |
| `t8463OutBlock1.indmsvol` | Number | 8 |  |
| `t8463OutBlock1.indmsamt` | Number | 12 |  |
| `t8463OutBlock1.formsvol` | Number | 8 |  |
| `t8463OutBlock1.formsamt` | Number | 12 |  |
| `t8463OutBlock1.sysmsvol` | Number | 8 |  |
| `t8463OutBlock1.sysmsamt` | Number | 12 |  |
| `t8463OutBlock1.stomsvol` | Number | 8 |  |
| `t8463OutBlock1.stomsamt` | Number | 12 |  |
| `t8463OutBlock1.invmsvol` | Number | 8 |  |
| `t8463OutBlock1.invmsamt` | Number | 12 |  |
| `t8463OutBlock1.banmsvol` | Number | 8 |  |
| `t8463OutBlock1.banmsamt` | Number | 12 |  |
| `t8463OutBlock1.insmsvol` | Number | 8 |  |
| `t8463OutBlock1.insmsamt` | Number | 12 |  |
| `t8463OutBlock1.finmsvol` | Number | 8 |  |
| `t8463OutBlock1.finmsamt` | Number | 12 |  |
| `t8463OutBlock1.monmsvol` | Number | 8 |  |
| `t8463OutBlock1.monmsamt` | Number | 12 |  |
| `t8463OutBlock1.etcmsvol` | Number | 8 |  |
| `t8463OutBlock1.etcmsamt` | Number | 12 |  |
| `t8463OutBlock1.natmsvol` | Number | 8 |  |
| `t8463OutBlock1.natmsamt` | Number | 12 |  |
| `t8463OutBlock1.pefmsvol` | Number | 8 |  |
| `t8463OutBlock1.pefmsamt` | Number | 12 |  |
