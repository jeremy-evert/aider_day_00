# 01 — Create Your Run Folder

Create a fresh folder for this rehearsal:

```powershell
New-Item -ItemType Directory -Path .\jeremy_run_1 -Force
Set-Location .\jeremy_run_1
Get-Location
```

Then prove the repository state:

```powershell
git status --short --branch
```

## Green light

You are inside `jeremy_run_1` and you know exactly where you are.

If the folder or repository state is not what you expect:

```text
STOP → LOOK → ASK ONE BOUNDED QUESTION
```
