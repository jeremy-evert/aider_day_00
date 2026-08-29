Fix only the existing interactive game in monty_hall.py. The current code is
wrong because it stores "goat" and "prize" values where it needs door numbers.

Use integer door identities 1, 2, and 3. Pick one integer prize door, convert
the validated player input to an integer, choose the host's revealed door from
the integer doors that are neither the prize nor the player's door, and print
that integer door. After stay-or-switch input, choose the one remaining closed
door when switching. Keep the program standard-library-only, small, and clear.

Do not add simulation mode yet. Do not edit MONTY_HALL_SPEC.md or any request
file. Change only monty_hall.py and state that before editing.
