#requires -Version 5.1
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)

function Write-Step {
    param([int]$Number, [string]$Message)
    Write-Output "[STEP] [$Number/6] $Message"
}

try {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $venvPath = Join-Path $repoRoot ".venv"
    $pythonExe = Join-Path $venvPath "Scripts\python.exe"
    $envPath = Join-Path $repoRoot ".env"
    $serverName = "ls-openapi-local"
    $appKey = $env:LS_SETUP_APP_KEY
    $appSecret = $env:LS_SETUP_APP_SECRET
    $baseUrl = $env:LS_SETUP_BASE_URL
    $replaceExisting = $env:LS_SETUP_REPLACE_EXISTING -eq "1"

    # Do not let credential variables leak into pip or other child processes.
    Remove-Item Env:\LS_SETUP_APP_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\LS_SETUP_APP_SECRET -ErrorAction SilentlyContinue
    Remove-Item Env:\LS_SETUP_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\LS_SETUP_REPLACE_EXISTING -ErrorAction SilentlyContinue

    if ([string]::IsNullOrWhiteSpace($appKey) -or [string]::IsNullOrWhiteSpace($appSecret)) {
        throw "앱키와 앱시크릿을 모두 입력해야 합니다."
    }

    Write-Step 1 "Python 버전을 확인합니다."
    $systemPython = Get-Command python -ErrorAction SilentlyContinue
    if (-not $systemPython) { throw "Python 3.10 이상이 필요합니다. python.org에서 설치한 뒤 다시 실행하세요." }
    $versionText = & $systemPython.Source -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($LASTEXITCODE -ne 0 -or [version]$versionText -lt [version]"3.10") {
        throw "Python 3.10 이상이 필요합니다. 감지된 버전: $versionText"
    }
    Write-Output "Python $versionText"

    Write-Step 2 "Python 가상환경을 준비합니다."
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        & $systemPython.Source -m venv $venvPath
        if ($LASTEXITCODE -ne 0) { throw "Python 가상환경을 만들지 못했습니다." }
    }
    else { Write-Output "기존 가상환경을 사용합니다." }

    Write-Step 3 "MCP 패키지를 설치합니다. 패키지 다운로드 진행률은 아래 로그에 표시됩니다."
    $installTimer = [Diagnostics.Stopwatch]::StartNew()
    & $pythonExe -m pip install --disable-pip-version-check -e "${repoRoot}[mcp]"
    $pipExitCode = $LASTEXITCODE
    $installTimer.Stop()
    if ($pipExitCode -ne 0) { throw "패키지 설치에 실패했습니다. 인터넷 연결을 확인한 뒤 다시 실행하세요." }
    Write-Output ("패키지 설치 완료 (소요 {0:N0}초)." -f $installTimer.Elapsed.TotalSeconds)

    Write-Step 4 "앱키와 API 주소를 로컬 .env에 저장합니다."
    if (Test-Path -LiteralPath $envPath) { $envText = [IO.File]::ReadAllText($envPath) }
    else {
        $examplePath = Join-Path $repoRoot ".env.example"
        if (-not (Test-Path -LiteralPath $examplePath)) { throw ".env.example 파일을 찾을 수 없습니다." }
        $envText = [IO.File]::ReadAllText($examplePath)
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
    $envText = Set-EnvValue $envText "LS_APP_KEY" $appKey
    $envText = Set-EnvValue $envText "LS_APP_SECRET" $appSecret
    $envText = Set-EnvValue $envText "LS_BASE_URL" $baseUrl
    [IO.File]::WriteAllText($envPath, $envText, [Text.UTF8Encoding]::new($false))
    $appKey = $null
    $appSecret = $null

    Write-Step 5 "Codex CLI와 기존 MCP 등록을 확인합니다."
    $codexCommand = Get-Command codex -ErrorAction SilentlyContinue
    if (-not $codexCommand) { throw "Codex CLI(codex)를 찾지 못했습니다. Codex를 설치하고 PATH를 확인하세요." }
    $existing = & $codexCommand.Source mcp list 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "Codex CLI에서 MCP 등록 목록을 읽지 못했습니다." }
    if ($existing -match [regex]::Escape($serverName)) {
        if (-not $replaceExisting) {
            Write-Output "기존 '$serverName' 등록을 유지했습니다. .env와 패키지는 준비됐습니다."
            exit 0
        }
        & $codexCommand.Source mcp remove $serverName
        if ($LASTEXITCODE -ne 0) { throw "기존 MCP 등록을 갱신하지 못했습니다." }
    }

    Write-Step 6 "Codex에 로컬 MCP 서버를 등록합니다."
    $arguments = @("mcp", "add", $serverName, "--env", "LS_OPENAPI_ENV_FILE=$envPath", "--", $pythonExe, "-m", "ls_openapi.mcp_server")
    & $codexCommand.Source @arguments
    if ($LASTEXITCODE -ne 0) { throw "Codex에 MCP 서버를 등록하지 못했습니다." }

    Write-Output "설치와 Codex 등록이 완료됐습니다."
    Write-Output "Codex를 완전히 종료한 뒤 다시 열고 새 대화에서 시세 조회 도구를 사용하세요."
    Write-Output "계좌 잔고 도구는 계좌 정보를 Codex 대화에 전달합니다. 주문 도구는 등록되지 않습니다."
    exit 0
}
catch {
    Write-Output "[ERROR] $($_.Exception.Message)"
    exit 1
}
