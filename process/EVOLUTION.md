# From first idea to recording freeze

The first Day 0 idea asked for a whole Monty Hall experience at once. That was
too large for a visible local-model bite, so the work was decomposed into
smaller Aider requests with explicit file boundaries and independent proof.

The controlled Chain Gun experiment then showed that the original `diff`
transport could hallucinate an unrelated path and run past 60 seconds. The
supported `udiff` transport succeeded twice, but at about 41.34 and 26.20
seconds it was still too slow for repeated classroom calls. Tests became the
chamber boundary, and future failing tests stayed out of the visible suite
until their chamber was introduced.

The recording therefore uses one small visible bite and a prepared,
independently tested Monty Hall payoff. That is a teaching decision, not a
claim that Aider is the strongest available coding agent. Safe prompts,
failures, raw-safe outputs, AAR conclusions, and video-preparation notes remain
public so students can inspect and adapt the engineering process.
