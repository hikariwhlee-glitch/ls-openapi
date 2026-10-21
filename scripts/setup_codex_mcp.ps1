#requires -Version 5.1
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $repoRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"
$envPath = Join-Path $repoRoot ".env"
$serverName = "ls-openapi-local"

function ConvertFrom-SecureInput {
    param([Parameter(Mandatory = $true)][Security.SecureString]$Value)
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

function Set-EnvValue {
    param([string]$Text, [string]$Name, [string]$Value)
    $escaped = $Value.Replace('"', '\"')
    $line = "$Name=`"$escaped`""
    $pattern = "(?m)^$([regex]::Escape($Name))=.*$"
    if ($Text -match $pattern) {
        return [regex]::Replace($Text, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $line })
    }
    return ($Text.TrimEnd() + "`r`n" + $line + "`r`n")
}

Write-Host "LS 국내선물옵션 MCP 로컬 설치를 시작합니다."
Write-Host "진행 중 API 조회나 주문은 실행하지 않습니다."

$systemPython = Get-Command python -ErrorAction SilentlyContinue
if (-not $systemPython) {
    throw "Python 3.10 이상이 필요합니다. python.org에서 Python을 설치한 뒤 다시 실행하세요."
}
$versionText = & $systemPython.Source -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($LASTEXITCODE -ne 0 -or [version]$versionText -lt [version]"3.10") {
    throw "Python 3.10 이상이 필요합니다. 감지된 버전: $versionText"
}

if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Host "가상환경을 만듭니다..."
    & $systemPython.Source -m venv $venvPath
    if ($LASTEXITCODE -ne 0) { throw "Python 가상환경을 만들지 못했습니다." }
}

Write-Host "MCP 패키지를 설치합니다..."
& $pythonExe -m pip install --disable-pip-version-check -e "$repoRoot[ mcp ]"
if ($LASTEXITCODE -ne 0) {
    # PowerShell treats brackets in a quoted argument literally; use pip's canonical extras syntax.
    & $pythonExe -m pip install --disable-pip-version-check -e "$repoRoot" "mcp[cli]>=1.28,<2"
    if ($LASTEXITCODE -ne 0) { throw "패키지 설치에 실패했습니다. 인터넷 연결을 확인하고 다시 실행하세요." }
}

if (Test-Path -LiteralPath $envPath) {
    $envText = [System.IO.File]::ReadAllText($envPath)
}
else {
    $examplePath = Join-Path $repoRoot ".env.example"
    if (-not (Test-Path -LiteralPath $examplePath)) { throw ".env.example 파일을 찾을 수 없습니다." }
    $envText = [System.IO.File]::ReadAllText($examplePath)
}

$hasKeys = ($envText -match '(?m)^LS_APP_KEY=.+$') -and ($envText -match '(?m)^LS_APP_SECRET=.+$')
$keepKeys = $false
if ($hasKeys) {
    $answer = Read-Host "기존 .env의 API 키를 그대로 사용할까요? [Y/n]"
    $keepKeys = [string]::IsNullOrWhiteSpace($answer) -or $answer -match '^(y|yes)$'
}

if (-not $keepKeys) {
    $keySecure = Read-Host "LS_APP_KEY 입력 (입력값은 화면에 표시되지 않습니다)" -AsSecureString
    $secretSecure = Read-Host "LS_APP_SECRET 입력 (입력값은 화면에 표시되지 않습니다)" -AsSecureString
    $appKey = ConvertFrom-SecureInput $keySecure
    $appSecret = ConvertFrom-SecureInput $secretSecure
    if ([string]::IsNullOrWhiteSpace($appKey) -or [string]::IsNullOrWhiteSpace($appSecret)) {
        throw "앱키와 앱시크릿을 모두 입력해야 합니다."
    }
    $envText = Set-EnvValue $envText "LS_APP_KEY" $appKey
    $envText = Set-EnvValue $envText "LS_APP_SECRET" $appSecret
    $appKey = $null
    $appSecret = $null
}

$currentBaseUrl = "https://openapi.ls-sec.co.kr:8080"
if ($envText -match '(?m)^LS_BASE_URL=(.*)$') {
    $candidate = $Matches[1].Trim().Trim('"')
    if ($candidate) { $currentBaseUrl = $candidate }
}
$baseUrl = Read-Host "LS API 주소 [$currentBaseUrl] (그대로 쓰려면 Enter)"
if ([string]::IsNullOrWhiteSpace($baseUrl)) { $baseUrl = $currentBaseUrl }
$envText = Set-EnvValue $envText "LS_BASE_URL" $baseUrl
[System.IO.File]::WriteAllText($envPath, $envText, [System.Text.UTF8Encoding]::new($false))

$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codexCommand) {
    throw "Codex CLI를 찾지 못했습니다. Codex를 설치하고 PATH에 등록한 뒤 이 스크립트를 다시 실행하세요."
}

$existing = & $codexCommand.Source mcp list 2>&1 | Out-String
if ($existing -match [regex]::Escape($serverName)) {
    $answer = Read-Host "Codex에 기존 '$serverName' 등록이 있습니다. 새 경로로 갱신할까요? [y/N]"
    if ($answer -notmatch '^(y|yes)$') {
        Write-Host "기존 등록을 유지했습니다. .env와 의존성은 준비됐습니다."
        exit 0
    }
    & $codexCommand.Source mcp remove $serverName
    if ($LASTEXITCODE -ne 0) { throw "기존 MCP 등록을 갱신하지 못했습니다." }
}

$arguments = @(
    "mcp", "add", $serverName,
    "--env", "LS_OPENAPI_ENV_FILE=$envPath",
    "--", $pythonExe, "-m", "ls_openapi.mcp_server"
)
& $codexCommand.Source @arguments
if ($LASTEXITCODE -ne 0) { throw "Codex에 MCP 서버를 등록하지 못했습니다." }

Write-Host ""
Write-Host "설치와 Codex 등록이 끝났습니다."
Write-Host "Codex를 완전히 종료한 뒤 다시 열고, 새 대화에서 'A016C000 현재가와 호가를 조회해줘'라고 요청해보세요."
Write-Host "계좌 잔고 도구는 계좌 정보를 Codex 대화에 전달합니다. 주문 도구는 등록되지 않습니다."
