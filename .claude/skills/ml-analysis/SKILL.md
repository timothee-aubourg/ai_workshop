---
name: ml-analysis
description: Run a data-analysis chain end to end from a written context prompt — question, data, features, model, split, evaluation against a baseline, and a report with a verified guardrail table and an empty human sign-off. Use when the user invokes /ml-analysis, points at a prompt file describing an analysis, or asks to run the workshop's water-treatment chain (honest, flawed, or variant mode).
---

# ml-analysis

The full method — what the skill reads from the prompt, the seven steps, the
guardrail rules, the sign-off rule, and the self-improvement loop — is written
in the workshop copy of this skill. Read it first and follow it literally:

- **Method:** `skills/ml-analysis/SKILL.md`
- **Context prompt (the frozen workshop problem):** `skills/ml-analysis/prompt.txt`
- **Data:** `skills/ml-analysis/water_treatment.csv` (527 daily rows, UCI id-106 schema, synthetic values)
- **Runner:** `skills/ml-analysis/run.py`
- **Frozen results** (used when scikit-learn is not installed): `skills/ml-analysis/cache.json`

Run the chain with:

```
python3 skills/ml-analysis/run.py --prompt skills/ml-analysis/prompt.txt --mode honest
```

`--mode flawed` and `--mode variant` exist for teaching: they deliberately break
a stated rule (a leaked feature, a shuffled split) and the report must say so in
its header. The runner works from any working directory and falls back to
`cache.json` when scikit-learn is missing.

Two rules override everything, in every mode and for any score: a failed
guardrail is printed in red and withholds the target tick, and the H1 human
sign-off line is left **empty** — the skill never ticks it.
