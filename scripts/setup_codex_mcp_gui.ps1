#requires -Version 5.1
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()

$repoRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $repoRoot ".env"
$backendPath = Join-Path $PSScriptRoot "setup_codex_mcp_run.ps1"
$logDirectory = Join-Path $env:LOCALAPPDATA "LSOpenAPI"
$logPath = Join-Path $logDirectory "setup.log"
$form = New-Object Windows.Forms.Form
$form.Text = "LS OpenAPI MCP 설치"
$form.StartPosition = "CenterScreen"
$form.Size = New-Object Drawing.Size(760, 690)
$form.MinimumSize = New-Object Drawing.Size(760, 690)
$form.Font = New-Object Drawing.Font("맑은 고딕", 9)
$form.BackColor = [Drawing.Color]::White

$title = New-Object Windows.Forms.Label
$title.Text = "LS OpenAPI 로컬 MCP 연결"
$title.Font = New-Object Drawing.Font("맑은 고딕", 17, [Drawing.FontStyle]::Bold)
$title.Location = New-Object Drawing.Point(24, 18)
$title.Size = New-Object Drawing.Size(690, 34)
$form.Controls.Add($title)

$intro = New-Object Windows.Forms.Label
$intro.Text = "앱키를 저장하고 Codex에 조회용 MCP 서버를 등록합니다. API 조회나 주문은 실행하지 않습니다."
$intro.Location = New-Object Drawing.Point(26, 59)
$intro.Size = New-Object Drawing.Size(700, 28)
$form.Controls.Add($intro)

function Add-Label {
    param([string]$Text, [int]$X, [int]$Y, [int]$W = 175)
    $control = New-Object Windows.Forms.Label
    $control.Text = $Text
    $control.Location = New-Object Drawing.Point($X, $Y)
    $control.Size = New-Object Drawing.Size($W, 25)
    $form.Controls.Add($control)
    return $control
}

Add-Label "LS_APP_KEY" 28 105 | Out-Null
$keyBox = New-Object Windows.Forms.TextBox
$keyBox.Location = New-Object Drawing.Point(205, 101)
$keyBox.Size = New-Object Drawing.Size(505, 27)
$keyBox.UseSystemPasswordChar = $true
$form.Controls.Add($keyBox)

Add-Label "LS_APP_SECRET" 28 145 | Out-Null
$secretBox = New-Object Windows.Forms.TextBox
$secretBox.Location = New-Object Drawing.Point(205, 141)
$secretBox.Size = New-Object Drawing.Size(505, 27)
$secretBox.UseSystemPasswordChar = $true
$form.Controls.Add($secretBox)

$keyHint = New-Object Windows.Forms.Label
$keyHint.Text = "입력한 키는 마스킹되어 보입니다. 로컬 .env에 저장되며 화면 로그에는 기록되지 않습니다."
$keyHint.ForeColor = [Drawing.Color]::FromArgb(85, 95, 110)
$keyHint.Location = New-Object Drawing.Point(205, 171)
$keyHint.Size = New-Object Drawing.Size(505, 25)
$form.Controls.Add($keyHint)

Add-Label "LS API 주소" 28 207 | Out-Null
$urlBox = New-Object Windows.Forms.TextBox
$urlBox.Text = "https://openapi.ls-sec.co.kr:8080"
$urlBox.Location = New-Object Drawing.Point(205, 203)
$urlBox.Size = New-Object Drawing.Size(505, 27)
$form.Controls.Add($urlBox)

$replaceBox = New-Object Windows.Forms.CheckBox
$replaceBox.Text = "기존 'ls-openapi-local' 등록이 있으면 갱신"
$replaceBox.Checked = $true
$replaceBox.Location = New-Object Drawing.Point(205, 239)
$replaceBox.Size = New-Object Drawing.Size(505, 25)
$form.Controls.Add($replaceBox)

$statusLabel = New-Object Windows.Forms.Label
$statusLabel.Text = "준비됨 — 정보를 확인하고 설치를 시작하세요."
$statusLabel.Font = New-Object Drawing.Font("맑은 고딕", 9, [Drawing.FontStyle]::Bold)
$statusLabel.Location = New-Object Drawing.Point(28, 279)
$statusLabel.Size = New-Object Drawing.Size(680, 25)
$form.Controls.Add($statusLabel)

$progress = New-Object Windows.Forms.ProgressBar
$progress.Location = New-Object Drawing.Point(28, 308)
$progress.Size = New-Object Drawing.Size(682, 18)
$progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
$progress.Minimum = 0
$progress.Maximum = 6
$progress.Value = 0
$form.Controls.Add($progress)

$logLabel = New-Object Windows.Forms.Label
$logLabel.Text = "설치 로그"
$logLabel.Location = New-Object Drawing.Point(28, 339)
$logLabel.Size = New-Object Drawing.Size(200, 22)
$form.Controls.Add($logLabel)

$logBox = New-Object Windows.Forms.RichTextBox
$logBox.Location = New-Object Drawing.Point(28, 363)
$logBox.Size = New-Object Drawing.Size(682, 220)
$logBox.ReadOnly = $true
$logBox.BackColor = [Drawing.Color]::FromArgb(247, 248, 250)
$logBox.Font = New-Object Drawing.Font("Consolas", 9)
$form.Controls.Add($logBox)

$logPathLabel = New-Object Windows.Forms.Label
$logPathLabel.Text = "상세 로그: $logPath"
$logPathLabel.Location = New-Object Drawing.Point(28, 584)
$logPathLabel.Size = New-Object Drawing.Size(470, 24)
$logPathLabel.AutoEllipsis = $true
$logPathLabel.ForeColor = [Drawing.Color]::FromArgb(85, 95, 110)
$form.Controls.Add($logPathLabel)

$elapsedLabel = New-Object Windows.Forms.Label
$elapsedLabel.Text = ""
$elapsedLabel.Location = New-Object Drawing.Point(28, 614)
$elapsedLabel.Size = New-Object Drawing.Size(300, 24)
$form.Controls.Add($elapsedLabel)

$startButton = New-Object Windows.Forms.Button
$startButton.Text = "설치 시작"
$startButton.Location = New-Object Drawing.Point(516, 614)
$startButton.Size = New-Object Drawing.Size(92, 34)
$startButton.BackColor = [Drawing.Color]::FromArgb(35, 95, 190)
$startButton.ForeColor = [Drawing.Color]::White
$startButton.FlatStyle = [Windows.Forms.FlatStyle]::Flat
$form.Controls.Add($startButton)

$closeButton = New-Object Windows.Forms.Button
$closeButton.Text = "닫기"
$closeButton.Location = New-Object Drawing.Point(618, 614)
$closeButton.Size = New-Object Drawing.Size(92, 34)
$form.Controls.Add($closeButton)
$closeButton.Add_Click({ $form.Close() })

$openLogButton = New-Object Windows.Forms.Button
$openLogButton.Text = "로그 열기"
$openLogButton.Location = New-Object Drawing.Point(414, 614)
$openLogButton.Size = New-Object Drawing.Size(92, 34)
$openLogButton.Enabled = $false
$openLogButton.Add_Click({
    if (Test-Path -LiteralPath $logPath) {
        Start-Process notepad.exe -ArgumentList @("`"$logPath`"")
    }
})
$form.Controls.Add($openLogButton)

function Read-DotEnvValue {
    param([string]$Text, [string]$Name)
    $match = [regex]::Match($Text, "(?m)^$([regex]::Escape($Name))=(.*)$")
    if (-not $match.Success) { return "" }
    $value = $match.Groups[1].Value.Trim()
    if ($value.Length -ge 2 -and $value.StartsWith('"') -and $value.EndsWith('"')) {
        $value = $value.Substring(1, $value.Length - 2).Replace('\"', '"')
    }
    return $value
}

if (Test-Path -LiteralPath $envPath) {
    $savedEnv = [IO.File]::ReadAllText($envPath)
    $keyBox.Text = Read-DotEnvValue $savedEnv "LS_APP_KEY"
    $secretBox.Text = Read-DotEnvValue $savedEnv "LS_APP_SECRET"
    $savedUrl = Read-DotEnvValue $savedEnv "LS_BASE_URL"
    if ($savedUrl) { $urlBox.Text = $savedUrl }
    if ($keyBox.Text -and $secretBox.Text) {
        $statusLabel.Text = "기존 .env 키를 불러왔습니다. 마스킹된 입력칸에서 확인하거나 교체하세요."
    }
}

$script:process = $null
$script:startedAt = $null
$script:step = 0
$timer = New-Object Windows.Forms.Timer
$timer.Interval = 250

$appendLog = [Action[string]]{
    param($Line)
    if ([string]::IsNullOrWhiteSpace($Line)) { return }
    $safeLine = $Line
    foreach ($secret in $script:secretValues) {
        if (-not [string]::IsNullOrEmpty($secret)) { $safeLine = $safeLine.Replace($secret, "[숨김]") }
    }
    try {
        $logBox.AppendText($safeLine + [Environment]::NewLine)
    }
    catch { }
    $logBox.SelectionStart = $logBox.TextLength
    $logBox.ScrollToCaret()
    if ($Line -match '^\[STEP\] \[(\d+)/6\] (.+)$') {
        $number = [int]$Matches[1]
        $script:step = [Math]::Min(6, [Math]::Max(0, $number))
        if ($progress.Style -ne [Windows.Forms.ProgressBarStyle]::Marquee) {
            $progress.Value = $script:step
        }
        $statusLabel.Text = $Matches[2]
    }
    if ($Line -match '^\[ERROR\]') {
        $statusLabel.Text = "오류 — 로그를 확인한 뒤 입력값과 설치 환경을 확인하세요."
        $statusLabel.ForeColor = [Drawing.Color]::Firebrick
        $progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
    }
    if ($Line -match '설치와 Codex 등록이 완료됐습니다') {
        $statusLabel.Text = "완료 — Codex를 완전히 종료한 뒤 다시 열어주세요."
        $statusLabel.ForeColor = [Drawing.Color]::DarkGreen
        $progress.Value = 6
        $progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
    }
    if ($Line -match "기존 'ls-openapi-local' 등록을 유지했습니다") {
        $statusLabel.Text = "기존 MCP 등록을 유지했습니다. 새 폴더 경로를 연결하려면 갱신 옵션을 선택하세요."
        $statusLabel.ForeColor = [Drawing.Color]::DarkGoldenrod
        $progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
    }
}

$startButton.Add_Click({
    if ([string]::IsNullOrWhiteSpace($keyBox.Text) -or [string]::IsNullOrWhiteSpace($secretBox.Text)) {
        [Windows.Forms.MessageBox]::Show("앱키와 앱시크릿을 모두 입력하세요. 보안 입력이라 입력 문자는 화면에 표시되지 않고 마스킹됩니다.", "키 입력 필요", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Warning) | Out-Null
        return
    }
    if ([string]::IsNullOrWhiteSpace($urlBox.Text)) {
        [Windows.Forms.MessageBox]::Show("LS API 주소를 입력하세요.", "주소 입력 필요", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Warning) | Out-Null
        return
    }
    if (-not (Test-Path -LiteralPath $backendPath)) {
        [Windows.Forms.MessageBox]::Show("설치 작업 파일을 찾지 못했습니다: $backendPath", "파일 오류", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Error) | Out-Null
        return
    }

    $logBox.Clear()
    $script:secretValues = @($keyBox.Text, $secretBox.Text)
    try {
        New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
        [IO.File]::WriteAllText($logPath, ("LS OpenAPI MCP 설치 로그 - {0:yyyy-MM-dd HH:mm:ss}{1}" -f (Get-Date), [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
    }
    catch {
        [Windows.Forms.MessageBox]::Show("로그 파일을 만들 수 없습니다: $($_.Exception.Message)", "로그 오류", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Warning) | Out-Null
    }
    $openLogButton.Enabled = $true
    $statusLabel.ForeColor = [Drawing.Color]::Black
    $statusLabel.Text = "설치를 시작합니다..."
    $progress.Style = [Windows.Forms.ProgressBarStyle]::Marquee
    $progress.MarqueeAnimationSpeed = 28
    $startButton.Enabled = $false
    $keyBox.Enabled = $false
    $secretBox.Enabled = $false
    $urlBox.Enabled = $false
    $replaceBox.Enabled = $false
    $script:startedAt = [Diagnostics.Stopwatch]::StartNew()

    $powershellExe = Join-Path $env:WINDIR "System32\WindowsPowerShell\v1.0\powershell.exe"
    $processInfo = New-Object Diagnostics.ProcessStartInfo
    $processInfo.FileName = $powershellExe
    $processInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$backendPath`""
    $processInfo.WorkingDirectory = $repoRoot
    $processInfo.UseShellExecute = $false
    $processInfo.CreateNoWindow = $true
    $processInfo.RedirectStandardOutput = $true
    $processInfo.RedirectStandardError = $true
    $processInfo.StandardOutputEncoding = New-Object Text.UTF8Encoding($false)
    $processInfo.StandardErrorEncoding = New-Object Text.UTF8Encoding($false)
    $processInfo.EnvironmentVariables["LS_SETUP_APP_KEY"] = $keyBox.Text
    $processInfo.EnvironmentVariables["LS_SETUP_APP_SECRET"] = $secretBox.Text
    $processInfo.EnvironmentVariables["LS_SETUP_BASE_URL"] = $urlBox.Text.Trim()
    if ($replaceBox.Checked) { $processInfo.EnvironmentVariables["LS_SETUP_REPLACE_EXISTING"] = "1" }
    else { $processInfo.EnvironmentVariables["LS_SETUP_REPLACE_EXISTING"] = "0" }
    $processInfo.EnvironmentVariables["PYTHONUTF8"] = "1"
    $processInfo.EnvironmentVariables["LS_SETUP_LOG_PATH"] = $logPath

    $script:process = New-Object Diagnostics.Process
    $script:process.StartInfo = $processInfo
    $script:process.EnableRaisingEvents = $true
    $script:process.add_OutputDataReceived({
        param($sender, $eventArgs)
        if ($null -ne $eventArgs.Data) {
            try { $form.BeginInvoke($appendLog, @($eventArgs.Data)) | Out-Null }
            catch { try { [IO.File]::AppendAllText($logPath, ("STDOUT: {0}{1}" -f $eventArgs.Data, [Environment]::NewLine), [Text.UTF8Encoding]::new($false)) } catch {} }
        }
    }.GetNewClosure())
    $script:process.add_ErrorDataReceived({
        param($sender, $eventArgs)
        if ($null -ne $eventArgs.Data) {
            try { $form.BeginInvoke($appendLog, @("[STDERR] $($eventArgs.Data)")) | Out-Null }
            catch { try { [IO.File]::AppendAllText($logPath, ("STDERR: {0}{1}" -f $eventArgs.Data, [Environment]::NewLine), [Text.UTF8Encoding]::new($false)) } catch {} }
        }
    }.GetNewClosure())
    $script:process.add_Exited({
        $exitCode = $script:process.ExitCode
        $form.BeginInvoke([Action]{
            $timer.Stop()
            if ($script:startedAt) {
                $script:startedAt.Stop()
                $elapsedLabel.Text = ("총 소요 시간: {0:N0}초" -f $script:startedAt.Elapsed.TotalSeconds)
            }
            if ($exitCode -ne 0 -and $statusLabel.ForeColor -ne [Drawing.Color]::Firebrick) {
                $statusLabel.Text = "설치가 중단됐습니다. 로그 내용을 확인하세요."
                $statusLabel.ForeColor = [Drawing.Color]::Firebrick
                $progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
            }
            $startButton.Enabled = $true
            $keyBox.Enabled = $true
            $secretBox.Enabled = $true
            $urlBox.Enabled = $true
            $replaceBox.Enabled = $true
            $openLogButton.Enabled = $true
            $script:secretValues = @()
        }) | Out-Null
    }.GetNewClosure())
    try {
        [void]$script:process.Start()
        $script:process.BeginOutputReadLine()
        $script:process.BeginErrorReadLine()
        $timer.Start()
    }
    catch {
        $progress.Style = [Windows.Forms.ProgressBarStyle]::Blocks
        $statusLabel.Text = "설치 작업을 시작하지 못했습니다."
        $statusLabel.ForeColor = [Drawing.Color]::Firebrick
        $startButton.Enabled = $true
        $keyBox.Enabled = $true
        $secretBox.Enabled = $true
        $urlBox.Enabled = $true
        $replaceBox.Enabled = $true
        [Windows.Forms.MessageBox]::Show($_.Exception.Message, "시작 오류", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Error) | Out-Null
    }
})

$timer.Add_Tick({
    if ($script:startedAt) {
        $elapsedLabel.Text = ("경과 시간: {0:N0}초" -f $script:startedAt.Elapsed.TotalSeconds)
    }
    if ($script:process -and $script:process.HasExited -and $startButton.Enabled -eq $false) {
        $script:process.Refresh()
    }
})

$form.Add_FormClosing({
    param($sender, $eventArgs)
    if ($script:process -and -not $script:process.HasExited) {
        $eventArgs.Cancel = $true
        [Windows.Forms.MessageBox]::Show("설치가 진행 중입니다. 완료 또는 오류가 표시된 뒤 닫아주세요.", "설치 진행 중", [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Information) | Out-Null
    }
})

[void]$form.ShowDialog()
