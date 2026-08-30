# Day 0 recording cockpit

This is the one linear path. Use the public repository's exact commit shown by
`git rev-parse HEAD`; do not improvise a second live Aider chamber.

1. Open `README.md`, `student/STUDENT_HANDOUT.md`, the Monty Hall spec, the
   Bite 01 prompt, and this file.
2. Start in `J:\git\aider_day_00\monty_hall_demo` and show clean status.
3. Establish the baseline: `python -m unittest -v`.
4. Show RED only for the intentionally introduced small test/change boundary,
   then run the file-backed Bite 01 request.
5. Inspect the one-line diff, compile, run the tests, and run `git diff --check`.
6. Restore the prepared payoff with `git restore --source=HEAD --staged
   --worktree -- monty_hall.py` if the visible bite altered the target.
7. Run the interactive game once, including one invalid input retry.
8. Run the seeded simulation and HTML report command in
   `recording/03_COMMANDS.md`; show the result and open the report.
9. Run the final tests and explain the Work First connection.

The accepted local-model route is Aider 0.86.2 with
`ollama_chat/qwen2.5-coder-3b-cpu:latest`, `--edit-format diff`, and a
file-backed message. It is yellow: the warm one-line bite was 10.8 seconds,
while the fresh rehearsal was about 51.2 seconds. Narrate the prompt and
expected diff during the wait. Do not use the rejected larger `diff` attempt.
The later `udiff` route was correct twice but remained too slow for repeated
visible classroom bites. The payoff is prepared and independently tested.

Only physical checks remain outside this package: microphone playback, OBS
framing, desktop/privacy scan, and global-key behavior.
