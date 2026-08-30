import math
import os
import random
import webbrowser
from datetime import datetime

DOORS = [1, 2, 3]


def get_host_door(prize, player):
    """Pick a door the host can safely open — not the prize, not the player's."""
    options = [d for d in DOORS if d != prize and d != player]
    return random.choice(options)


# ── interactive game ────────────────────────────────────────────────────────

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
        if raw == "1":
            return False   # stay
        if raw == "2":
            return True    # switch
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


# ── simulation ──────────────────────────────────────────────────────────────

def simulate(trials):
    stay_wins        = 0
    switch_wins      = 0
    prize_count      = {1: 0, 2: 0, 3: 0}
    first_pick_count = {1: 0, 2: 0, 3: 0}

    for _ in range(trials):
        prize    = random.choice(DOORS)
        player   = random.choice(DOORS)
        host     = get_host_door(prize, player)
        switched = next(d for d in DOORS if d != player and d != host)

        prize_count[prize]       += 1
        first_pick_count[player] += 1

        if player  == prize:
            stay_wins   += 1
        if switched == prize:
            switch_wins += 1

    # 95% margin of error for a proportion near 0.5 (conservative bound)
    margin = 1.96 * math.sqrt(0.5 * 0.5 / trials)

    w = len(f"{trials:,}")   # width for alignment

    print()
    print(f"  {'─'*50}")
    print(f"  Simulation — {trials:,} trials")
    print(f"  {'─'*50}")

    print(f"\n  Prize placed behind each door:")
    for d in DOORS:
        print(f"    Door {d}:  {prize_count[d]:{w},} / {trials:,}  "
              f"({prize_count[d]/trials:.1%})   expected ~33.3%")

    print(f"\n  Player's first pick:")
    for d in DOORS:
        print(f"    Door {d}:  {first_pick_count[d]:{w},} / {trials:,}  "
              f"({first_pick_count[d]/trials:.1%})   expected ~33.3%")

    print(f"\n  Strategy comparison:")
    print(f"    Always stay:    {stay_wins:{w},} / {trials:,}  "
          f"({stay_wins/trials:.1%})   expected ~33.3%")
    print(f"    Always switch:  {switch_wins:{w},} / {trials:,}  "
          f"({switch_wins/trials:.1%})   expected ~66.7%")

    print(f"\n  Margin of error (95% confidence):  ±{margin:.1%}")
    print(f"  With {trials:,} trials, any result within that margin")
    print(f"  of the expected value is normal random noise — not a bug.")
    print(f"  Run 100 trials, then 10,000. Watch the margin shrink.")
    print()
    print('  "All simulations are wrong. Some are useful."')
    print("   — after George Box")
    print(f"  {'─'*50}")
    print()

    return {
        "trials":           trials,
        "stay_wins":        stay_wins,
        "switch_wins":      switch_wins,
        "prize_count":      prize_count,
        "first_pick_count": first_pick_count,
        "margin":           margin,
    }


# ── html report ─────────────────────────────────────────────────────────────

def pct(n, total):
    return f"{n / total:.1%}"


def bar(n, total, color):
    width = round(n / total * 100, 1)
    return (
        f'<div style="background:#e8e8e8;border-radius:4px;height:22px;width:100%;">'
        f'<div style="background:{color};width:{width}%;height:22px;border-radius:4px;">'
        f'</div></div>'
    )


def make_html(stats):
    t   = stats["trials"]
    s   = stats["stay_wins"]
    sw  = stats["switch_wins"]
    m   = stats["margin"]
    pc  = stats["prize_count"]
    fp  = stats["first_pick_count"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    prize_rows = "\n".join(
        f"<tr><td>Door {d}</td>"
        f"<td>{pc[d]:,}</td>"
        f"<td>{pct(pc[d], t)}</td>"
        f"<td>~33.3%</td>"
        f"<td>{bar(pc[d], t, '#3498db')}</td></tr>"
        for d in DOORS
    )
    pick_rows = "\n".join(
        f"<tr><td>Door {d}</td>"
        f"<td>{fp[d]:,}</td>"
        f"<td>{pct(fp[d], t)}</td>"
        f"<td>~33.3%</td>"
        f"<td>{bar(fp[d], t, '#9b59b6')}</td></tr>"
        for d in DOORS
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Monty Hall — {t:,} Trials</title>
<style>
  body   {{ font-family: system-ui, sans-serif; max-width: 860px;
            margin: 40px auto; padding: 0 24px; background: #f7f7f7; color: #222; }}
  h1     {{ color: #2c3e50; margin-bottom: 4px; }}
  h2     {{ color: #2c3e50; border-bottom: 2px solid #ddd;
            padding-bottom: 6px; margin-top: 36px; }}
  table  {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
  th, td {{ padding: 9px 14px; text-align: left; border-bottom: 1px solid #ddd; }}
  th     {{ background: #2c3e50; color: #fff; font-weight: 600; }}
  tr:nth-child(even) {{ background: #efefef; }}
  .hero  {{ display: flex; gap: 24px; margin: 24px 0; }}
  .card  {{ flex: 1; border-radius: 8px; padding: 20px 24px;
            color: white; text-align: center; }}
  .card h3 {{ margin: 0 0 6px; font-size: 1rem; opacity: .85; }}
  .card p  {{ margin: 0; font-size: 2.2rem; font-weight: 700; }}
  .card small {{ font-size: 0.9rem; opacity: .8; }}
  .stay   {{ background: #e74c3c; }}
  .switch {{ background: #27ae60; }}
  .quote  {{ background: #eaf4fb; border-left: 5px solid #3498db;
             padding: 14px 20px; margin: 28px 0; font-style: italic; }}
  .warn   {{ background: #fef9e7; border-left: 5px solid #f1c40f;
             padding: 14px 20px; margin: 28px 0; }}
  .footer {{ color: #aaa; font-size: 0.82em; margin-top: 48px; }}
  td:nth-child(5) {{ width: 220px; }}
</style>
</head>
<body>

<h1>🎭 Monty Hall Simulation</h1>
<p style="color:#666">{now} &nbsp;·&nbsp; <strong>{t:,} trials</strong></p>

<div class="hero">
  <div class="card stay">
    <h3>Always Stay</h3>
    <p>{pct(s, t)}</p>
    <small>{s:,} wins out of {t:,}</small>
  </div>
  <div class="card switch">
    <h3>Always Switch</h3>
    <p>{pct(sw, t)}</p>
    <small>{sw:,} wins out of {t:,}</small>
  </div>
</div>

<div class="warn">
  <strong>Margin of error (95% confidence): ±{m:.1%}</strong><br>
  With {t:,} trials, any result within <strong>±{m:.1%}</strong> of the expected value
  is normal random variation — not a flaw in the math.
  The expected values are exactly <strong>33.3%</strong> (stay) and <strong>66.7%</strong> (switch).<br><br>
  Try running 100 trials vs. 10,000 and watch the margin shrink.
  That is the instrument becoming more precise.
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

<h2>Why does switching win more often?</h2>
<p>
  When you first pick a door, you have a <strong>1-in-3 chance</strong> of being right —
  meaning there is a <strong>2-in-3 chance</strong> the prize is behind one of the other two.
  When the host opens a losing door, that 2-in-3 probability does not disappear.
  It <em>collapses onto the one remaining closed door</em>.
  Switching claims that 2-in-3 probability. Staying keeps your original 1-in-3.
</p>
<p>
  The simulation does not prove <em>why</em> — it just shows you the <em>shape</em> of what
  happens when you run the experiment many times. Mathematics explains why.
  Code automates the drudgery of checking.
</p>

<div class="quote">
  <strong>"All simulations are wrong. Some are useful."</strong><br>
  — after George Box<br><br>
  This program cannot prove the Monty Hall result from first principles.
  It can show you that, over many trials with a fair random setup,
  the numbers land close to what the math predicts.
  That is what instruments do — they make invisible things visible enough to think about.
  The precision of the instrument depends on how many trials you run.
  Your curiosity decides how far to push it.
</div>

<div class="footer">
  Generated by Opus_monty_hall · Aider 101 Day 0 · {now}
</div>
</body>
</html>"""


# ── main loop ────────────────────────────────────────────────────────────────

print("=== Monty Hall ===")
print()

while True:
    print("  1. Play one game")
    print("  2. Run a simulation")
    print("  3. Quit")
    print()

    while True:
        mode = input("Choose 1, 2, or 3: ").strip()
        if mode in ("1", "2", "3"):
            break
        print("Please type 1, 2, or 3.")
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

        stats = simulate(trials)

        while True:
            save = input("Save a results page and open it? (y/n): ").strip().lower()
            if save in ("y", "n"):
                break
            print("Type y or n.")

        if save == "y":
            filename = f"monty_hall_{trials}_trials.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(make_html(stats))
            print(f"  Saved: {filename}")
            webbrowser.open(os.path.abspath(filename))

    else:
        print("See you next time. 👋")
        break

    print()
