# Day 0 student handout

Start at the repository root, then run:

```powershell
Set-Location .\monty_hall_demo
python -m unittest -v
python monty_hall.py --simulate 10000 --seed 20260830 --html day00_seed_20260830.html --timestamp 2026-08-30T00:00
```

The test suite is the baseline proof. The simulation should show staying near
one third and switching near two thirds. Open the generated HTML file if your
instructor asks for the report.

The teaching loop is:

```text
GOAL -> BASELINE -> AIDER -> DIFF -> PROOF -> COMMIT
```

For the Aider portion, show `student/prompts/01_strategy_label.md` first. It
asks for one named constant in one named file. Inspect `git diff` before
trusting any tool message. If the change is unexpected, stop and ask for help;
do not clean or reset an unclear tree.

Use your own Git identity and instructor-provided repository when practicing
remote operations. Never put a password, token, private key, or API key in a
prompt, receipt, or commit.
