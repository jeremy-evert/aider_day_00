# 09 — Decide What Survives

Choose one:

```text
KEEP
REPAIR
REJECT
```

If the result is green and you choose KEEP, stage the accepted version:

```powershell
git add .\hello.py .\AIDER_REQUEST.md .\launch_aider.ps1
```

Inspect before committing:

```powershell
git status --short --branch
git diff --staged
```

Then commit the accepted run:

```powershell
git commit -m "Complete Jeremy Day 0 run 1"
```

Do not commit a result you have not inspected and independently run.

## Green light

The commit contains only the artifacts you intended to keep from `jeremy_run_1`.
