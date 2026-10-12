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
4. **Actions 탭 → live-auth-test (수동 실행) → Run workflow**

워크플로우는 `workflow_dispatch`(수동 실행)로만 동작하며, push나 pull request로는 실행되지 않습니다. 포크한 저장소의 PR에는 시크릿이 전달되지 않습니다.

## 무엇을 확인하나

토큰을 발급받고 곧바로 폐기합니다. 화면에는 앱키, 시크릿키, 토큰 값이 출력되지 않고 아래만 출력됩니다.

| 출력 | 확인하려는 것 |
|---|---|
| 응답 필드명 | 유효기간 필드가 `expire_in`인지 `expires_in`인지 |
| `token_type`, `expires_in`, `scope` | 토큰 응답 형식 |
| 폐기 응답 `code` / `message` | 폐기 성공을 나타내는 코드 값 (공식 명세에 없음) |
| `base_url` | 어떤 주소로 호출했는지 |

결과를 공유할 때는 위 출력만 붙여 넣으면 됩니다. 키 값은 절대 붙여 넣지 마세요.

## 문제가 생기면

[troubleshooting.md](troubleshooting.md)를 보세요. 실서버 테스트가 실패하면 오류 메시지의 HTTP 상태와 서버 메시지(키는 가려져 있습니다)가 단서입니다.
