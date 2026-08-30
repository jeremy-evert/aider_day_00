import math
import os
import random
import webbrowser
from datetime import datetime

DOORS = [1, 2, 3]


# ── helpers ───────────────────────────────────────────────────────────────────

def get_host_door(prize, player):
    """The one rule that makes the math interesting."""
    options = [d for d in DOORS if d != prize and d != player]
    return random.choice(options)


def fmt_margin(m):
    """Honest margin display — no hiding behind ±0.0% at large n."""
    pct = m * 100
    if pct >= 1.0:  return f"±{pct:.2f}%"
    if pct >= 0.01: return f"±{pct:.3f}%"
    return               f"±{pct:.4f}%"


def run_trials(n):
    """Core simulation engine. Returns a full stats dict."""
    stay_wins = switch_wins = 0
    prize_count      = {1: 0, 2: 0, 3: 0}
    first_pick_count = {1: 0, 2: 0, 3: 0}

    for _ in range(n):
        prize    = random.choice(DOORS)
        player   = random.choice(DOORS)
        host     = get_host_door(prize, player)
        switched = next(d for d in DOORS if d != player and d != host)

        prize_count[prize]       += 1
        first_pick_count[player] += 1
        if player  == prize: stay_wins   += 1
        if switched == prize: switch_wins += 1

    return {
        "trials":           n,
        "stay_wins":        stay_wins,
        "switch_wins":      switch_wins,
        "prize_count":      prize_count,
        "first_pick_count": first_pick_count,
        "margin":           1.96 * math.sqrt(0.25 / n),
    }


# ── interactive game ──────────────────────────────────────────────────────────

def ask_door():
    while True:
        raw = input("Pick a door — 1, 2, or 3: ").strip()
        if raw in ("1", "2", "3"):
            return int(raw)
        print("Please type 1, 2, or 3.")


def ask_stay_or_switch():
    print("  1. Stay with your door")
    print("  2. Switch to the other door")
    while True:
        raw = input("Choose 1 or 2: ").strip()
        if raw == "1": return False
        if raw == "2": return True
        print("Please type 1 or 2.")


def play_one_round():
    prize  = random.choice(DOORS)
    player = ask_door()
    host   = get_host_door(prize, player)
    print(f"The host opens door {host} — there's a goat!")

    switch = ask_stay_or_switch()
    if switch:
        player = next(d for d in DOORS if d != player and d != host)

    if player == prize:
        print(f"Door {player}: PRIZE! You win! 🎉")
    else:
        print(f"Door {player}: goat. Prize was behind door {prize}. You lose.")


# ── simulation output ─────────────────────────────────────────────────────────

def print_simulation(stats):
    t, s, sw = stats["trials"], stats["stay_wins"], stats["switch_wins"]
    m = stats["margin"]
    w = len(f"{t:,}")

    print()
    print(f"  {'─'*60}")
    print(f"  Simulation — {t:,} trials")
    print(f"  {'─'*60}")

    print(f"\n  Prize placed behind each door:")
    for d in DOORS:
        c = stats["prize_count"][d]
        print(f"    Door {d}:  {c:{w},} / {t:,}  ({c/t:.1%})   expected ~33.3%")

    print(f"\n  Player's first pick:")
    for d in DOORS:
        c = stats["first_pick_count"][d]
        print(f"    Door {d}:  {c:{w},} / {t:,}  ({c/t:.1%})   expected ~33.3%")

    print(f"\n  Strategy comparison:")
    print(f"    Always stay:    {s:{w},} / {t:,}  ({s/t:.1%})   expected ~33.3%")
    print(f"    Always switch:  {sw:{w},} / {t:,}  ({sw/t:.1%})   expected ~66.7%")

    print(f"\n  Margin of error (95% confidence): {fmt_margin(m)}")
    print(f"  To halve your uncertainty, run 4× as many trials (the √n law).")
    print()
    print('  "All simulations are wrong. Some are useful."  — after George Box')
    print(f"  {'─'*60}")
    print()


# ── convergence table ─────────────────────────────────────────────────────────

STEPS = [10, 100, 1_000, 10_000, 100_000, 1_000_000]


def convergence_table():
    """Run at increasing scale and stream each row live as it completes."""
    col = 13
    print()
    print("  Watching the Law of Large Numbers")
    print(f"  {'─'*64}")
    print(f"  {'Trials':>{col}}   {'Stay':>8}   {'Switch':>8}   Margin")
    print(f"  {'─'*64}")

    rows      = []
    last_stats = None
    for n in STEPS:
        stats = run_trials(n)
        s, sw, m = stats["stay_wins"], stats["switch_wins"], stats["margin"]
        print(f"  {n:>{col},}   {s/n:>7.1%}   {sw/n:>7.1%}   {fmt_margin(m)}")
        rows.append((n, s, sw, m))
        last_stats = stats

    print(f"  {'─'*64}")
    print(f"  Expected: stay ≈ 33.3%  |  switch ≈ 66.7%")
    print()
    print("  Notice how the margin shrinks but never hits zero.")
    print("  To halve the margin, you need 4× the trials — because")
    print("  uncertainty shrinks with the square root of n, not n itself.")
    print("  That is why precise experiments are expensive.")
    print("  That is also why computers are so useful.")
    print()

    return rows, last_stats


# ── html helpers ──────────────────────────────────────────────────────────────

def bar_html(n, total, color):
    w = round(n / total * 100, 1)
    return (
        '<div style="background:#e8e8e8;border-radius:4px;height:20px;width:100%;">'
        f'<div style="background:{color};width:{w}%;height:20px;border-radius:4px;"></div>'
        '</div>'
    )


def conv_rows_html(rows):
    if not rows:
        return ""
    trs = "\n  ".join(
        f"<tr><td>{n:,}</td><td>{s/n:.1%}</td><td>{sw/n:.1%}</td>"
        f"<td>{fmt_margin(m)}</td><td>{bar_html(s, n, '#e74c3c')}</td></tr>"
        for n, s, sw, m in rows
    )
    return f"""
<h2>The Law of Large Numbers in action</h2>
<p>Each row is a complete independent simulation at increasing scale.
   Watch the results converge as the instrument becomes more precise.</p>
<table>
  <tr><th>Trials</th><th>Always Stay</th><th>Always Switch</th>
      <th>Margin ±</th><th>Stay visual</th></tr>
  {trs}
</table>
<p style="margin-top:10px;color:#555;font-size:.9em">
  Expected: stay ≈ 33.3% &nbsp;|&nbsp; switch ≈ 66.7%<br>
  To halve the margin, run <strong>4× as many trials</strong> —
  uncertainty shrinks with the <em>square root</em> of n, not n itself.
  That is why precise experiments are expensive. That is also why computers are useful.
</p>"""


# ── html report ───────────────────────────────────────────────────────────────

def make_html(stats, conv_rows=None):
    t  = stats["trials"]
    s  = stats["stay_wins"]
    sw = stats["switch_wins"]
    m  = stats["margin"]
    pc = stats["prize_count"]
    fp = stats["first_pick_count"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    prize_rows = "\n  ".join(
        f"<tr><td>Door {d}</td><td>{pc[d]:,}</td>"
        f"<td>{pc[d]/t:.1%}</td><td>~33.3%</td>"
        f"<td>{bar_html(pc[d], t, '#3498db')}</td></tr>"
        for d in DOORS
    )
    pick_rows = "\n  ".join(
        f"<tr><td>Door {d}</td><td>{fp[d]:,}</td>"
        f"<td>{fp[d]/t:.1%}</td><td>~33.3%</td>"
        f"<td>{bar_html(fp[d], t, '#9b59b6')}</td></tr>"
        for d in DOORS
    )
    conv_section = conv_rows_html(conv_rows or [])

    # Plain string — no f-string escaping needed for CSS braces
    css = """
    body    { font-family: system-ui, sans-serif; max-width: 900px;
               margin: 40px auto; padding: 0 24px; background: #f7f7f7; color: #222; }
    h1      { color: #2c3e50; margin-bottom: 4px; }
    h2      { color: #2c3e50; border-bottom: 2px solid #ddd;
               padding-bottom: 6px; margin-top: 36px; }
    table   { border-collapse: collapse; width: 100%; margin-top: 12px; }
    th, td  { padding: 9px 14px; text-align: left; border-bottom: 1px solid #ddd; }
    th      { background: #2c3e50; color: #fff; font-weight: 600; }
    tr:nth-child(even) { background: #efefef; }
    .hero   { display: flex; gap: 24px; margin: 24px 0; flex-wrap: wrap; }
    .card   { flex: 1; min-width: 200px; border-radius: 8px; padding: 20px 24px;
               color: white; text-align: center; }
    .card h3    { margin: 0 0 6px; font-size: 1rem; opacity: .85; }
    .card p     { margin: 0; font-size: 2.4rem; font-weight: 700; }
    .card small { font-size: 0.9rem; opacity: .8; }
    .stay    { background: #e74c3c; }
    .switch  { background: #27ae60; }
    .quote   { background: #eaf4fb; border-left: 5px solid #3498db;
                padding: 14px 20px; margin: 28px 0; font-style: italic; }
    .warn    { background: #fef9e7; border-left: 5px solid #f1c40f;
                padding: 14px 20px; margin: 28px 0; }
    .courses { display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }
    .course  { flex: 1; min-width: 220px; border-radius: 6px; padding: 14px 18px;
                border: 2px solid #ddd; background: white; }
    .course h4 { margin: 0 0 8px; color: #2c3e50; }
    .course p  { margin: 0; font-size: 0.9em; color: #444; line-height: 1.6; }
    td:last-child { width: 200px; }
    .footer  { color: #aaa; font-size: 0.82em; margin-top: 48px; border-top: 1px solid #ddd;
                padding-top: 16px; }
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Monty Hall — {t:,} Trials</title>
<style>{css}</style>
</head>
<body>

<h1>🎭 Monty Hall Simulation</h1>
<p style="color:#666">{now} &nbsp;·&nbsp; <strong>{t:,} trials</strong></p>

<div class="hero">
  <div class="card stay">
    <h3>Always Stay</h3>
    <p>{s/t:.1%}</p>
    <small>{s:,} wins / {t:,} trials</small>
  </div>
  <div class="card switch">
    <h3>Always Switch</h3>
    <p>{sw/t:.1%}</p>
    <small>{sw:,} wins / {t:,} trials</small>
  </div>
</div>

<div class="warn">
  <strong>Margin of error (95% confidence): {fmt_margin(m)}</strong><br>
  With {t:,} trials, any result within <strong>{fmt_margin(m)}</strong> of the expected
  value is normal random variation — not a flaw in the math.<br>
  Expected: <strong>33.3%</strong> stay &nbsp;·&nbsp; <strong>66.7%</strong> switch.<br><br>
  To halve your uncertainty, run <strong>4× as many trials</strong> — because uncertainty
  shrinks with the <em>square root</em> of n, not n itself.
  Precision is expensive. Computers are cheap.
</div>

<h2>Was the prize placed fairly?</h2>
<table>
  <tr><th>Door</th><th>Prize count</th><th>Rate</th><th>Expected</th><th>Visual</th></tr>
  {prize_rows}
</table>

<h2>Did the player pick fairly?</h2>
<table>
  <tr><th>Door</th><th>First pick</th><th>Rate</th><th>Expected</th><th>Visual</th></tr>
  {pick_rows}
</table>

{conv_section}

<h2>Why does switching win more often?</h2>
<p>
  When you first pick a door, you have a <strong>1-in-3 chance</strong> of being right —
  meaning there is a <strong>2-in-3 chance</strong> the prize is behind one of the other two doors.
  When the host opens a losing door, that 2/3 probability does not vanish.
  It <em>collapses onto the one remaining closed door.</em>
  Switching claims that 2/3 probability. Staying keeps your original 1/3.
</p>
<p>
  The simulation cannot prove <em>why</em> — it shows you the <em>shape</em> of what happens
  at scale. Mathematics explains why. Code automates the drudgery of checking.
  Your curiosity decides how far to push it.
</p>

<div class="quote">
  <strong>"All simulations are wrong. Some are useful."</strong><br>
  — after George Box<br><br>
  This program cannot prove the Monty Hall result from first principles.
  It shows you that over many trials, the numbers land close to what the math predicts.
  That is what instruments do — they make invisible things visible enough to think about.
  A microscope does not explain biology. It makes cells visible enough to reason about.
  This simulation does not explain probability. It makes the pattern visible enough to question.
</div>

<h2>The same code, three different lenses</h2>
<div class="courses">
  <div class="course">
    <h4>📘 CS 1 — First Programs</h4>
    <p>You just wrote a probability experiment with loops, functions, and input validation.
       The computer ran {t:,} trials in the time it takes to blink.
       That is the point of code: delegate the drudgery, keep the reasoning.</p>
  </div>
  <div class="course">
    <h4>📗 Discrete Structures</h4>
    <p>The sample space has exactly 9 equally-likely outcomes (3 prize doors × 3 player picks).
       Enumerate them by hand. Count the switching wins. Verify that the math and the
       simulation agree — and explain why they <em>must</em>.</p>
  </div>
  <div class="course">
    <h4>📙 Computer Architecture</h4>
    <p>One CPU core ran all {t:,} trials while the other cores sat idle.
       How would you redesign this simulation to use all cores in parallel?
       What would the speedup formula look like? Start with Amdahl's Law
       and tell me where the limit is.</p>
  </div>
</div>

<div class="footer">
  Opus_monty_hall_0_5_0 &nbsp;·&nbsp; Aider 101 Day 0 &nbsp;·&nbsp; {now}<br>
  Built iteratively with Olivia (Copilot) as Shot 1 of a three-shot prompt engineering exercise.
  Shot 2: ChatGPT Think Deeper builds this from a spec. Shot 3: Aider + local CPU model builds it from a tight prompt.
</div>
</body>
</html>"""


# ── main loop ─────────────────────────────────────────────────────────────────

def ask_save_and_open(stats, conv_rows=None):
    while True:
        ans = input("Save and open a results page? (y/n): ").strip().lower()
        if ans in ("y", "n"):
            break
        print("Type y or n.")
    if ans == "y":
        n = stats["trials"]
        fname = f"monty_hall_{n}_trials.html" if not conv_rows else "monty_hall_convergence.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(make_html(stats, conv_rows))
        print(f"  Saved: {fname}")
        webbrowser.open(os.path.abspath(fname))


print("=== Monty Hall ===")
print()

while True:
    print("  1. Play one game")
    print("  2. Run a simulation")
    print("  3. Watch the Law of Large Numbers")
    print("  4. Quit")
    print()

    while True:
        mode = input("Choose 1, 2, 3, or 4: ").strip()
        if mode in ("1", "2", "3", "4"):
            break
        print("Please type 1, 2, 3, or 4.")
    print()

    if mode == "1":
        play_one_round()

    elif mode == "2":
        while True:
            raw = input("How many trials? ").strip()
            try:
                trials = int(raw)
                if trials > 0:
                    break
            except ValueError:
                pass
            print("Please enter a positive whole number.")
        stats = run_trials(trials)
        print_simulation(stats)
        ask_save_and_open(stats)

    elif mode == "3":
        conv_rows, last_stats = convergence_table()
        ask_save_and_open(last_stats, conv_rows)

    else:
        print("See you next time. 👋")
        break

    print()
