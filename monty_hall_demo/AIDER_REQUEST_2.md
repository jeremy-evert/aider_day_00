Review and correct the existing first-pass Monty Hall game, then add the
second pass described in MONTY_HALL_SPEC.md.

Keep the interactive game working and make the smallest focused change to
monty_hall.py. Use door numbers 1, 2, and 3 as door identities; do not confuse
the text "goat" or "prize" with a door number. The host must reveal exactly one
losing door that is different from the player's door, and the switch result
must be computed from the one remaining closed door.

Add a standard-library-only simulation mode available as:

    python monty_hall.py --simulate 10000

The simulation must run the same three-door host rule for every trial, compare
always-stay with always-switch, and report counts and percentages. Expose a
small callable such as simulate(trials, rng=None) so an independent unittest
can run it without interactive input. Reject a non-positive trial count with a
clear command-line error. Keep input validation and the interactive output
clear for a beginning student.

Do not edit MONTY_HALL_SPEC.md, either AIDER_REQUEST file, or any other file.
Before editing, state the single file you expect to change.
