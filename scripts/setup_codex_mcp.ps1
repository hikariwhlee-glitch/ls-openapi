#requires -Version 5.1
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$logDirectory = Join-Path $env:LOCALAPPDATA "LSOpenAPI"
$logPath = Join-Path $logDirectory "setup.log"
$transcriptStarted = $false
$failure = $null
try { New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null; Start-Transcript -Path $logPath -Append -Force | Out-Null; $transcriptStarted = $true } catch { Write-Warning "상세 로그 파일을 만들지 못했습니다: $($_.Exception.Message)" }
function Write-Step([int]$Number, [string]$Message) { Write-Host ""; Write-Host "[$Number/6] $Message" -ForegroundColor Cyan }
function ConvertFrom-SecureInput([Security.SecureString]$Value) { $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value); try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) } }
function Set-EnvValue([string]$Text, [string]$Name, [string]$Value) {
    $escaped = $Value.Replace('"', ([char]92 + '"'))
    $line = $Name + '="' + $escaped + '"'
    $pattern = "(?m)^$([regex]::Escape($Name))=.*$"
    if ($Text -match $pattern) { return [regex]::Replace($Text, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $line }) }
    return ($Text.TrimEnd() + [Environment]::NewLine + $line + [Environment]::NewLine)
}
try {
    $repoRoot = Split-Path -Parent $PSScriptRoot; $venvPath = Join-Path $repoRoot ".venv"; $pythonExe = Join-Path $venvPath "Scripts\python.exe"; $envPath = Join-Path $repoRoot ".env"; $serverName = "ls-openapi-local"
    Write-Host "LS 국내선물옵션 MCP 설치를 시작합니다." -ForegroundColor Green; Write-Host "설치 중 API 조회나 주문은 실행하지 않습니다."; Write-Host "상세 로그: $logPath"
    Write-Step 1 "Python 3.10 이상을 확인합니다."
    $systemPython = Get-Command python -ErrorAction SilentlyContinue
    if (-not $systemPython) { throw "Python 3.10 이상이 필요합니다. python.org에서 설치한 뒤 다시 실행하세요." }
    $versionText = & $systemPython.Source -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($LASTEXITCODE -ne 0 -or [version]$versionText -lt [version]"3.10") { throw "Python 3.10 이상이 필요합니다. 감지된 버전: $versionText" }
    Write-Host "Python $versionText 확인 완료."
    Write-Step 2 "Python 가상환경을 준비합니다."
    if (-not (Test-Path -LiteralPath $pythonExe)) { & $systemPython.Source -m venv $venvPath; if ($LASTEXITCODE -ne 0) { throw "Python 가상환경을 만들지 못했습니다." } } else { Write-Host "기존 가상환경을 사용합니다." }
    Write-Step 3 "MCP 패키지를 설치합니다. 다운로드 진행률이 표시됩니다."
    & $pythonExe -m pip install --disable-pip-version-check -e ($repoRoot + "[mcp]")
    if ($LASTEXITCODE -ne 0) { throw "패키지 설치에 실패했습니다. 위 pip 오류와 인터넷 연결을 확인하세요." }
    Write-Step 4 "API 키와 주소를 설정합니다."
    if (Test-Path -LiteralPath $envPath) { $envText = [IO.File]::ReadAllText($envPath) } else { $examplePath = Join-Path $repoRoot ".env.example"; if (-not (Test-Path -LiteralPath $examplePath)) { throw ".env.example 파일을 찾을 수 없습니다." }; $envText = [IO.File]::ReadAllText($examplePath) }
    $hasKeys = ($envText -match '(?m)^LS_APP_KEY=.+$') -and ($envText -match '(?m)^LS_APP_SECRET=.+$'); $keepKeys = $false
    if ($hasKeys) { $answer = Read-Host "기존 .env의 API 키를 그대로 사용할까요? [Y/n]"; $keepKeys = [string]::IsNullOrWhiteSpace($answer) -or $answer -match '^(y|yes)$' }
    if (-not $keepKeys) {
        Write-Host "앱키와 앱시크릿 입력 문자는 표시되지 않습니다."
        $keySecure = Read-Host "LS 앱키 입력" -AsSecureString; $secretSecure = Read-Host "LS 앱시크릿 입력" -AsSecureString
        $appKey = ConvertFrom-SecureInput $keySecure; $appSecret = ConvertFrom-SecureInput $secretSecure
        if ([string]::IsNullOrWhiteSpace($appKey) -or [string]::IsNullOrWhiteSpace($appSecret)) { throw "앱키와 앱시크릿을 모두 입력해야 합니다." }
        $envText = Set-EnvValue $envText "LS_APP_KEY" $appKey; $envText = Set-EnvValue $envText "LS_APP_SECRET" $appSecret; $appKey = $null; $appSecret = $null
    }
    $baseUrl = "https://openapi.ls-sec.co.kr:8080"
    if ($envText -match '(?m)^LS_BASE_URL=(.*)$') { $candidate = $Matches[1].Trim().Trim('"'); if ($candidate) { $baseUrl = $candidate } }
    $inputUrl = Read-Host "LS API 주소 [$baseUrl] (기본 주소를 쓰려면 Enter)"; if (-not [string]::IsNullOrWhiteSpace($inputUrl)) { $baseUrl = $inputUrl }
    $envText = Set-EnvValue $envText "LS_BASE_URL" $baseUrl; [IO.File]::WriteAllText($envPath, $envText, [Text.UTF8Encoding]::new($false)); Write-Host "키 설정을 .env에 저장했습니다. 키 값은 로그에 출력하지 않습니다."
    Write-Step 5 "Codex CLI와 기존 MCP 등록을 확인합니다."
    $codexCommand = Get-Command codex -ErrorAction SilentlyContinue
    if (-not $codexCommand) {
        Write-Host "Codex CLI가 없습니다. npm으로 공식 Codex CLI를 설치합니다." -ForegroundColor Yellow
        $npmCommand = Get-Command npm -ErrorAction SilentlyContinue
        if (-not $npmCommand) { throw "Codex CLI 설치에 필요한 npm을 찾지 못했습니다. Node.js LTS를 설치한 뒤 다시 실행하세요." }
        & $npmCommand.Source install --global @openai/codex@latest
        if ($LASTEXITCODE -ne 0) { throw "Codex CLI 설치 실패 (npm 종료 코드: $LASTEXITCODE). 인터넷 연결과 Node.js/npm 설치를 확인한 뒤 다시 실행하세요." }
        $npmPrefix = (& $npmCommand.Source config get prefix 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($npmPrefix)) { $env:PATH = $npmPrefix + ";" + $env:PATH }
        $codexCommand = Get-Command codex -ErrorAction SilentlyContinue
        if (-not $codexCommand -and -not [string]::IsNullOrWhiteSpace($npmPrefix)) {
            $codexShim = Join-Path $npmPrefix "codex.cmd"
            if (Test-Path -LiteralPath $codexShim) { $codexCommand = Get-Command $codexShim -ErrorAction SilentlyContinue }
        }
        if (-not $codexCommand) { throw "Codex CLI는 설치됐지만 현재 터미널에서 찾지 못했습니다. 새 CMD 창을 열고 다시 실행하세요." }
        Write-Host "Codex CLI 설치 확인 완료."
    }
    $existing = & $codexCommand.Source mcp list 2>&1 | Out-String; if ($LASTEXITCODE -ne 0) { throw "Codex CLI에서 MCP 등록 목록을 읽지 못했습니다." }
    $register = $true
    if ($existing -match [regex]::Escape($serverName)) {
        $answer = Read-Host "기존 '$serverName' 등록을 새 경로로 갱신할까요? [y/N]"
        if ($answer -notmatch '^(y|yes)$') { $register = $false; Write-Host "기존 MCP 등록을 유지합니다." } else { & $codexCommand.Source mcp remove $serverName; if ($LASTEXITCODE -ne 0) { throw "기존 MCP 등록을 제거하지 못했습니다." } }
    }
    if ($register) { Write-Step 6 "Codex에 MCP 서버를 등록합니다."; & $codexCommand.Source mcp add $serverName --env "LS_OPENAPI_ENV_FILE=$envPath" -- $pythonExe -m ls_openapi.mcp_server; if ($LASTEXITCODE -ne 0) { throw "Codex에 MCP 서버를 등록하지 못했습니다." } } else { Write-Step 6 "기존 MCP 등록을 유지합니다." }
    Write-Host ""; Write-Host "설치와 Codex 등록이 완료됐습니다." -ForegroundColor Green; Write-Host "Codex를 완전히 종료한 뒤 다시 열고 새 대화에서 시세 조회 도구를 사용해보세요."; Write-Host "주문 도구는 등록되지 않습니다."
} catch { $failure = $_.Exception.Message; Write-Host ""; Write-Host "설치에 실패했습니다: $failure" -ForegroundColor Red; Write-Host "상세 로그: $logPath" -ForegroundColor Yellow } finally { if ($transcriptStarted) { Stop-Transcript | Out-Null } }
if ($failure) { exit 1 }; exit 0
