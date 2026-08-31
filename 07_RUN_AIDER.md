# 07 — Run the Microscopic Aider Bite

From inside `jeremy_run_1`:

```powershell
.\launch_aider.ps1
```

Before pasting anything, confirm the launcher prints:

```text
Aider target: hello.py
Expected change scope: hello.py only
```

Then paste the request from `AIDER_REQUEST.md`.

Inside Aider, inspect the proposed/resulting change with:

```text
/diff
```

Then exit Aider.

## Green light

Aider completed the tiny request and you have not yet accepted success merely because Aider said it worked.
