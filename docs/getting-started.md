# 시작하기

설치부터 접근토큰 발급까지 따라 하는 안내입니다. 국내선물 시세 조회는 공식 TR 명세 확인 후 추가됩니다 ([api-inventory.md](api-inventory.md) 참고).

## 1. LS증권 OPEN API 신청

공식 포털 안내([시작하기](https://openapi.ls-sec.co.kr/howto-use), [이용안내](https://openapi.ls-sec.co.kr/about-openapi)) 기준입니다. 화면은 바뀔 수 있으니 포털 내용이 우선합니다.

1. LS증권 계좌가 필요합니다. OPEN API는 계좌를 보유한 개인/법인 고객에게 제공됩니다.
2. OPEN API 신청은 **xingAPI 사용등록을 한 뒤**에 할 수 있습니다.
3. 홈페이지 **고객센터 > 매매시스템 > API > 사용등록/해지**에서 API 구분을 `OPEN API`로 선택해 신청합니다.
4. 신청 후 같은 화면에서 계좌번호와 계좌비밀번호로 조회하면 **앱키(App Key)** 와 **앱 시크릿키(App Secret)** 를 확인할 수 있습니다.
5. 모의투자는 별도로 신청하며 앱키도 별도로 발급됩니다. 실전 키와 모의 키를 섞어 쓰지 마세요.

> 앱키와 시크릿키는 비밀번호처럼 다루세요. 유출되었다면 사용해지 후 재등록해야 하고, 이때 기존에 발급된 토큰은 만료됩니다.

## 2. 설치

Python 3.9 이상이 필요합니다.

```bash
git clone https://github.com/hikariwhlee-glitch/ls-openapi.git
cd ls-openapi

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

## 3. 인증정보 설정

```bash
cp .env.example .env             # Windows: copy .env.example .env
```

`.env`를 열어 발급받은 값으로 바꿉니다.

```
LS_APP_KEY=발급받은_앱키
LS_APP_SECRET=발급받은_시크릿키
```

- `.env`는 `.gitignore`에 포함되어 있어 커밋되지 않습니다. 그래도 파일을 다른 사람에게 보내거나 공유하지 마세요.
- 같은 이름의 환경변수가 이미 설정되어 있으면 환경변수가 `.env`보다 우선합니다.
- 값이 `YOUR_`로 시작하는 예시 그대로이면 실행 시 안내 메시지와 함께 중단됩니다.

## 4. 접근토큰 발급 해보기

저장소 루트에서 실행합니다.

```bash
python examples/domestic_futureoption/01_issue_token.py
```

성공하면 다음과 같이 나옵니다. 토큰 값 자체는 화면에 출력하지 않습니다.

```
토큰 발급 성공
  token_type : Bearer
  토큰 길이  : ...자 (값은 출력하지 않습니다)
  유효기간   : ...초
```

실패하면 [troubleshooting.md](troubleshooting.md)를 확인하세요.

## 5. 코드에서 사용하기

```python
from ls_openapi import Settings, TokenManager

settings = Settings.from_env()
tokens = TokenManager(settings)

token = tokens.get_token()      # 처음에는 발급, 이후에는 재사용 (만료 임박 시 재발급)
print(token.authorization_header[:6])  # 'Bearer' — 전체 토큰은 출력하지 마세요

tokens.revoke()                 # 더 이상 쓰지 않을 때 폐기
```

## 6. 테스트 실행

```bash
pytest
```

단위 테스트는 가짜(mock) HTTP 응답만 사용합니다. 실제 서버 접속이나 계정이 필요 없고, 앱키/시크릿키도 필요하지 않습니다.

## 다음 단계

국내선물 시세 조회 예제는 공식 TR 명세(TR 코드, 경로, 요청·응답 필드)를 확인한 뒤 `examples/domestic_futureoption/`에 추가됩니다.
