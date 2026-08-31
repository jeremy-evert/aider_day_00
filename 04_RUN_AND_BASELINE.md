# 04 — Run It, Then Establish the Baseline

From inside `jeremy_run_1`:

```powershell
python .\hello.py
```

Expected output:

```text
Hello, world!
```

Now inspect repository state:

```powershell
git status --short --branch
```

Stage only the known-good starter file:

```powershell
git add .\hello.py
```

Then inspect again:

```powershell
git status --short --branch
git diff --staged -- .\hello.py
```

Think of the staged file as the known-good comparison shelf.

## Green light

- Python prints `Hello, world!`.
- `hello.py` is staged as the known-good baseline.
- Nothing unexpected is staged.
