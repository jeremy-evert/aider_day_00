# Recording commands

Run from `J:\git\aider_day_00` unless noted.

```powershell
git status --short --branch
Set-Location .\monty_hall_demo
python -m unittest -v
python -m py_compile monty_hall.py
git diff --check
python monty_hall.py --seed 20260830 --simulate 10000 --html day00_seed_20260830.html --timestamp 2026-08-30T00:00
python -m unittest -v
```

For the approved local Aider demonstration, from the repository root:

```powershell
$env:OLLAMA_API_BASE = "http://127.0.0.1:11434"
aider --model ollama_chat/qwen2.5-coder-3b-cpu:latest --edit-format diff --file .\monty_hall_demo\monty_hall.py --message-file .\student\prompts\01_strategy_label.md --no-auto-commits --yes-always --no-check-update --no-analytics --no-auto-lint --no-pretty --no-stream
git diff -- .\monty_hall_demo\monty_hall.py
python -m py_compile .\monty_hall_demo\monty_hall.py
python -m unittest -v .\monty_hall_demo\test_monty_hall.py
git diff --check
git restore --source=HEAD --staged --worktree -- .\monty_hall_demo\monty_hall.py
```

Do not paste credentials, pull a model, publish media, or use a cloud key.
