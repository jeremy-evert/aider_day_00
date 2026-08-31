# 08 — Inspect the Diff and Prove the Behavior

After leaving Aider, stay inside `jeremy_run_1` and ask Git what actually changed:

```powershell
git status --short --branch
git diff -- .\hello.py
git diff --staged -- .\hello.py
```

Your prediction was:

```text
One line in hello.py should change.
No other file should change.
```

Now run the program independently:

```powershell
python .\hello.py
```

Expected output:

```text
Hello, Aider!
```

Remember:

```text
Aider says it worked.       CLAIM
Git shows the change.       EVIDENCE
Python runs the result.     PROOF
```

## Green light

The scope, diff, and independent program output all agree with the prediction.
