# Monty Hall demo specification

This is the bounded specification for the Day 0 instructor demonstration.

Build a small standard-library-only Python console program in two passes:

1. Implement a playable three-door Monty Hall game.
2. Add a simulation mode without changing the game rules.

The playable version must:

- place one prize and two goats behind doors 1, 2, and 3;
- accept a player's door choice;
- have the host reveal one losing door that the player did not choose;
- offer the player a stay-or-switch decision;
- reveal the result clearly; and
- reject invalid input without adding dependencies.

The simulation version must:

- run from the command line with a requested trial count;
- compare always-stay and always-switch strategies using the same host rule;
- report counts and percentages; and
- make the result testable without interactive input.

Use the smallest readable design. Keep the interactive game and simulation
logic close enough for a beginning student to follow, but separate enough that
an independent test can check the probability claim.

Acceptance evidence:

- `python monty_hall.py` starts the three-door game;
- `python monty_hall.py --simulate 10000` reports stay near one-third and
  switch near two-thirds;
- `python -m unittest -v` passes the independent checks; and
- the final Git diff contains only the demo files intended for this lesson.
