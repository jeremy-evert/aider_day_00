# 06 — Build the Aider Launcher

Inside `jeremy_run_1`, create:

```text
launch_aider.ps1
```

Use this first recording version:

```powershell
$ErrorActionPreference = "Stop"

$demoFolder = $PSScriptRoot
$helloFile = Join-Path $demoFolder "hello.py"
$model = if ($env:AIDER_DAY0_MODEL) { $env:AIDER_DAY0_MODEL } else { "qwen2.5-coder-3b-cpu:latest" }
$endpoint = "http://127.0.0.1:11434"

if (-not (Test-Path -LiteralPath $helloFile)) {
    throw "hello.py is missing. Stop and complete the earlier Day 0 steps first."
}

if (-not (Get-Command aider -ErrorAction SilentlyContinue)) {
    throw "Aider is not available on PATH. Stop and ask the instructor."
}

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw "Ollama is not available on PATH. Stop and ask the instructor."
}

Push-Location $demoFolder
try {
    $env:OLLAMA_API_BASE = $endpoint

    $models = (& ollama list 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        throw "Ollama did not answer. Stop and ask the instructor."
    }

    if ($models -notmatch [regex]::Escape($model)) {
        throw "Approved model '$model' is not already available. Stop; do not download a model."
    }

    Write-Host "Route: Ollama loopback $endpoint"
    Write-Host "Model: ollama_chat/$model"
    Write-Host "Aider target: hello.py"
    Write-Host "Expected change scope: hello.py only"
    Write-Host "Review mode: no automatic commit"

    $aiderArgs = @(
        "--model=ollama_chat/$model"
        "--edit-format=diff"
        "--file=./hello.py"
        "--no-auto-commits"
        "--no-auto-lint"
        "--no-check-update"
        "--no-analytics"
    )

    & aider @aiderArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Aider exited with code $LASTEXITCODE. Stop and inspect before continuing."
    }
}
finally {
    Pop-Location
}
```

This script does not install, download, repair, or change system settings.

## Green light

`launch_aider.ps1` exists beside `hello.py` and `AIDER_REQUEST.md`.
