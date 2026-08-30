# Day 0 — Get control of the machine with Aider

This public repository is both a runnable CS I lesson and an honest record of
how the lesson was engineered. It is intentionally still evolving: the code
and student path are usable, while `process/` keeps the prompts, tests,
failed attempts, and recording decisions visible.

## First action after cloning

```powershell
git clone https://github.com/jeremy-evert/aider_day_00.git
Set-Location aider_day_00\monty_hall_demo
python -m unittest -v
```

Then read [student/STUDENT_HANDOUT.md](student/STUDENT_HANDOUT.md). The lesson
starts with folder/Git/Python observations, then makes one tiny Aider change,
reviews the diff, and proves the result. The robot changed something. Prove it
still works. Write down what happened.

## What you will learn

- how files, local Git history, and a remote repository differ;
- how to give a coding tool one bounded request;
- why a success message is not acceptance;
- how independent tests and a deterministic simulation support a claim; and
- how an instructor turns experiments and failures into a repeatable lesson.

The runnable lesson is in `monty_hall_demo/`. Its tests are
`monty_hall_demo/test_monty_hall.py`. The prepared Aider request used for the
visible bite is `student/prompts/01_strategy_label.md`.

Yes, this could have been done more easily with a frontier agent. In CS I, the
goal is not getting the work done. The goal is helping new users understand the
process well enough to scale into the tools they will meet in the wild.

## Requirements and status

The core lesson uses Python's standard library and needs no cloud account or
Codex/Claude/Foreman access. The recording variant additionally uses the
instructor's already-installed Aider/Ollama setup; students may follow the
software-observation steps without downloading a model.

This is a transparent teaching workshop, not a claim that Aider is the
strongest coding agent. Deliberate friction—small prompts, visible diffs,
RED/GREEN tests, and separate proof—is educational.

## Find the deeper trail

- `student/` — the direct student lesson, tests, and safe prompt.
- `recording/` — the linear cockpit, script, commands, and cue card Jeremy can
  use before recording.
- `process/` — the safe inheritance map, experiment summaries, prompt history,
  Chain Gun correction trail, and the decisions behind the freeze.

The unrelated `M365_Copilot_EULA_Terms_19Nov2025.pdf` remains local-only and is
not part of this repository: redistribution rights and teaching need were not
established.
