# Mission 009 — safe public summary

The accepted dependency-free Monty Hall target supports play, stay/switch
invariants, seeded simulation, distributions, convergence, standalone HTML,
and independent tests. Five baseline tests and five behavioral-parity tests
passed. The selected model was qwen2.5-coder-3b-cpu; the warm one-line bite was
10.8 seconds and the fresh rehearsal about 51.2 seconds. Larger bites were
stopped or split rather than presented as successes.

The deterministic rehearsal used seed `20260830`, 10,000 trials, and produced
3,360 stay wins (33.6%) and 6,640 switch wins (66.4%), with a 95% margin of
`+/- 0.98%`. The reset strategy restores only the named target, leaving an
understandable Git state.
