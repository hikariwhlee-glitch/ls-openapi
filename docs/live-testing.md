# 실서버(모의투자) 테스트

기본 `pytest`는 가짜 응답만 쓰는 단위 테스트입니다. 이 문서는 **실제 앱키로 토큰 발급·폐기를 확인**하는 방법입니다.

> **모의투자 키로 먼저 테스트하세요.** 모의투자는 앱키/시크릿키가 실전과 다르게 발급됩니다 (공식 [이용안내](https://openapi.ls-sec.co.kr/about-openapi)). 실전 키와 모의 키를 섞지 마세요.

## 먼저 알아둘 점: 모의투자 REST 주소

공식 이용안내와 TR 명세 JSON에는 **모의투자용 REST 주소가 명시되어 있지 않습니다.** (WebSocket만 모의투자 주소 `wss://openapi.ls-sec.co.kr:29443`가 명시되어 있습니다.) 2026-10-12에 모의투자 키로 실행한 결과, 기본 주소(`https://openapi.ls-sec.co.kr:8080`)에서 토큰 발급·폐기가 성공했습니다(1회 관측). 따라서 `LS_BASE_URL`은 보통 지정하지 않아도 됩니다.

- 기본값으로 먼저 실행해 보세요.
- 4xx 오류가 나면 먼저 키(모의/실전 구분, 앞뒤 공백)를 확인하세요. 그래도 해결되지 않으면 포털 안내나 고객센터에서 REST 주소를 확인한 뒤 `LS_BASE_URL`로 지정합니다. 주소를 추측해서 넣지 마세요.

## 방법 1. 내 PC에서 실행 (가장 단순)

`.env`에 모의투자 앱키/시크릿키를 넣고 (`.env`는 커밋되지 않습니다) 저장소 루트에서 실행합니다.

```bash
LS_LIVE_TEST=1 pytest -s tests/live            # macOS / Linux
```

```powershell
$env:LS_LIVE_TEST="1"; pytest -s tests/live    # Windows PowerShell
```

## 방법 2. GitHub Actions에서 수동 실행

키가 저장소 코드에 남지 않고 GitHub에 암호화되어 저장됩니다.

1. 저장소 **Settings → Secrets and variables → Actions → New repository secret**
   - `LS_APP_KEY`: 모의투자 앱키
   - `LS_APP_SECRET`: 모의투자 시크릿키
2. (권장) **Settings → Environments → New environment**에서 `live-test` 환경을 만들고 **Required reviewers**에 본인을 지정합니다. 실행 전에 승인이 필요해집니다.
3. (선택) 모의투자 REST 주소가 다르다고 확인된 경우에만 **Settings → Secrets and variables → Actions → Variables**에 `LS_BASE_URL`을 등록합니다.
4. (시세 조회 테스트용) 같은 Variables 화면에 `LS_FOCODE`를 등록합니다. 조회할 선물/옵션 종목코드이며 비밀값이 아니라서 시크릿이 아닌 변수로 둡니다. 등록하지 않으면 시세 조회 테스트만 건너뜁니다.
   - `focode`는 **8자리**로 실서버 확인했습니다. 5자리 `A016C`는 오류 없이 응답해도 OutBlock의 종목코드가 비어 있고 값이 0이므로 유효 조회로 세지 않습니다.
   - 쉼표로 여러 8자리 코드를 넣으면 토큰 하나로 차례로 조회합니다(호출 사이 1.1초 간격). 등록한 모든 코드에 대해 `rsp_cd=00000`이고 반환 `focode`가 요청과 일치해야 테스트가 통과합니다.
   - 2026-10-14 Actions 재실행에서 현재 상장 네 월물 `A016C000`, `A0173000`, `A0176000`, `A0179000`이 모두 유효한 응답을 반환했습니다. 네 코드는 `LS_FOCODE` Actions 변수에 저장되어 있습니다.
5. **Actions 탭 → live-auth-test (수동 실행) → Run workflow**

워크플로우는 `workflow_dispatch`(수동 실행)로만 동작하며, push나 pull request로는 실행되지 않습니다. 포크한 저장소의 PR에는 시크릿이 전달되지 않습니다.

## 무엇을 확인하나

테스트는 두 개입니다. 화면에는 앱키, 시크릿키, 토큰 값이 출력되지 않습니다.

**1. 발급 → 폐기** (`tests/live/test_live_auth.py`): 발급과 폐기가 각각 동작하는지 확인하려고 발급 직후 폐기합니다. 이 토큰은 다른 호출에 쓰지 않습니다.

| 출력 | 확인하려는 것 |
|---|---|
| 응답 필드명 | 유효기간 필드가 `expire_in`인지 `expires_in`인지 |
| `token_type`, `expires_in`, `scope` | 토큰 응답 형식 |
| 폐기 응답 `code` / `message` | 폐기 성공을 나타내는 코드 값 |
| `base_url` | 어떤 주소로 호출했는지 |

**2. 발급 → 선물/옵션 현재가(t2111) 조회 → 폐기** (`tests/live/test_live_futures.py`): 토큰 하나로 시세를 조회한 뒤 마지막에 폐기합니다. `LS_FOCODE`가 필요합니다.

| 출력 | 확인하려는 것 |
|---|---|
| `[조회] 응답 tr_cd`, `tr_cont`, `tr_cont_key` | 응답 헤더 형식 |
| `[응답] 최상위 키`, 블록 이름과 필드 이름·값 | 공식 샘플에 없는 응답(OutBlock) 구조. 값은 공개 시세 데이터입니다 |
| 조회 실패 시 오류 메시지 | `Bearer` 접두사, 종목코드 형식 등의 문제 (HTTP 상태와 서버 메시지) |
| `[폐기] code/message` | 조회 후 폐기도 정상인지 |

결과를 공유할 때는 위 출력만 붙여 넣으면 됩니다. 키 값은 절대 붙여 넣지 마세요.

## 문제가 생기면

[troubleshooting.md](troubleshooting.md)를 보세요. 실서버 테스트가 실패하면 오류 메시지의 HTTP 상태와 서버 메시지(키는 가려져 있습니다)가 단서입니다.

## 실전 계좌 잔고 조회 (`CFOAQ50600`)

이 TR은 모의투자에서 `rsp_cd=01900`(해당업무 미제공)이라 실전 키로만 확인할 수 있습니다. 모의투자 키와 섞이지 않도록 별도 워크플로 `live-balance-real.yml`을 씁니다.

1. Settings > Environments 에서 `live-real` 환경을 만들고, Required reviewers 와 배포 가능 브랜치를 제한합니다.
2. 그 환경의 Secrets 에 **실전** `LS_APP_KEY`, `LS_APP_SECRET` 을 등록합니다. 저장소 단위 시크릿(모의투자)은 건드리지 않습니다.
3. Actions > live-balance-real 에서 `confirm` 에 `REAL` 을 입력해 실행합니다. 잔고 조회 한 건만 실행하고 주문은 나가지 않습니다.
4. 공개 로그에는 응답코드와 필드 이름만 남습니다. 확인을 마치면 환경의 실전 키는 지우거나 필요 시에만 두세요.
