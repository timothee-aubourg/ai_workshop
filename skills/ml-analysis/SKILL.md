---
name: analysis
description: Run a data-analysis chain end to end from a written context prompt — question, data, features, model, split, evaluation against a baseline, and a report with a verified guardrail table and an empty human sign-off. Use when the user invokes /analysis, points at a prompt file describing an analysis, or asks to run the workshop's water-treatment chain (honest, flawed, or variant mode).
---

# Skill: ml-analysis

Installed as the `analysis` skill, so the command is `/analysis`. Copy this
folder to `.claude/skills/analysis/` in any project to use it there.

## When to use
The user invokes `/analysis <prompt-file>` or asks to run a data-analysis
chain end to end from a written context prompt.

## Principle
This skill is GENERIC. It knows no dataset, no task family, no domain.
Every problem-specific decision lives in the prompt file. The skill's job
is to read those decisions, execute them faithfully, and refuse to invent
what the prompt does not state.

## The four duties this skill is built around
Everything below serves one of four things that stay human. The skill
executes; these four decide what "executed well" means. The prompt is
written in the same four blocks, so each rule can be traced to its duty.

- **T · Tacit knowledge** — the question and the data. What is predicted,
  in which unit, for whom, and which mistake costs more; where each number
  comes from, how it was measured, and whether it can be trusted. This is
  the expert's own capital — workflow and domain knowledge that exists
  nowhere in the data. The skill never invents it: it reads it from the
  prompt's TACIT KNOWLEDGE block.
- **D · Delegation level** — how far the run may go alone. What it may
  decide (features, model family, hyper-parameters tuned on validation
  data) and what it may never touch (target, split rule, metric, baseline,
  guardrails). Read from the prompt's DELEGATION block. If the prompt is
  silent, the run does NOT decide: it stops and asks.
- **G · Guardrails** — validation. Every rule the prompt states is checked
  by ID and printed PASS or FAIL. A FAIL is printed in red and withholds
  the target tick, even when the metric target is met.
- **A · Accountability** — sign-off. H1 is left EMPTY in every mode, for
  any score. Reaching a number is the agent's job; approving a report is
  a human's.

## What belongs in the skill, and what belongs in the prompt
The skill is the method; the prompt is the case. One test decides:

- if changing it changes **the answer**, it belongs in the **prompt** —
  target, data file, preparation rules, metric, baseline, split rule,
  guardrail thresholds, iteration count, delegation limits;
- if changing it changes **what a good answer means**, it belongs in the
  **skill** — the seven steps, the four duties, how guardrails are
  verified and printed, the report structure, the sign-off rule.

So the prompt does not extend the skill; it *adapts* it. You should be
able to hand this skill a prompt from a completely different field and
change nothing in this file. And if a run would score better after
editing this file, stop: you are editing the referee, not the match.

## What this skill does
1. **Read the prompt file** *(all four duties)*. Extract, block by block:
   from TACIT KNOWLEDGE the question and target, the task type
   (regression, classification, clustering, forecasting, ...), the metric,
   the baseline rule, the data file and its preparation rules (imputation,
   exclusions); from DELEGATION the split rule, what the run may decide
   and what it may not, and the iteration count; from GUARDRAILS the
   numbered checks; from ACCOUNTABILITY the sign-off line; plus the report
   requirements (format, structure, sections).
2. **Question** *(T)*. Restate the problem in one sentence, in the prompt's
   own terms. If the target, metric, or task type is missing: STOP and ask
   — a missing question is tacit knowledge the run cannot supply.
3. **Data** *(T)*. Load the file the prompt names. Profile quality (missing
   values, outliers, duplicates). Apply exactly the preparation rules the
   prompt states, computing any fill statistics on training data only.
   Record every choice for the report.
4. **Features** *(D)*. Build only inputs the prompt allows, available at
   prediction time. Apply the prompt's exclusions literally. Feature
   building is delegated work: report what was built, so it can be reviewed.
5. **Model & split** *(D)*. Compute the baseline the prompt defines FIRST.
   Split exactly as the prompt instructs. Fit the simplest model of the
   family the prompt's task type implies; complexity must be earned
   against the baseline.
6. **Evaluate & report** *(G, then A)*. Score on held-out data only, next
   to the baseline. Generate the report in the format and structure the prompt
   requires, and always include: a guardrails checklist (each prompt rule,
   checked or failed), limits & uncertainty, and an EMPTY sign-off line.
   This skill NEVER ticks the sign-off.
7. **Next investigations (auto-research)** *(D)*. From the results, propose 2-3
   concrete, testable next steps: a candidate feature, a reframing, a
   validation to run, a worst-case to inspect. Each suggestion must be
   checkable, and none may be executed without a new prompt.

## Guardrails (verified by the run itself, cited by ID)
The prompt states its guardrails as a numbered list (G1, G2, ...). The run
must verify each one and print the identifier with its outcome — `G3 PASS`,
`G4 FAIL` — in a table in the report, in the same order as the prompt. Never
paraphrase a guardrail and never silently drop one: if a check cannot be
performed, print it as FAIL with the reason. A FAIL withholds the target tick
even when the metric target is met, and is printed in red.

The sign-off item (H1) is human. The run leaves it empty in every mode, for
any score, without exception.

## Guardrails (general principle)
Every rule the prompt states is a guardrail. The run verifies each one and
ticks it in the report and on the dashboard; a failed guardrail is shown in
red, never hidden. A failed guardrail also WITHHOLDS the target tick, even
if the number is reached — a score obtained outside the rules proves nothing.

## Target (agent-ticked, never the sign-off)
The prompt may define a target for the metric (e.g. MAE below a threshold).
The run ticks the target only when it is reached AND all guardrails hold.
The sign-off line remains empty in every case: reaching a number is the
agent's job; approving a report is a human's.

## Self-improvement loop (auto-research)
The prompt states the number of iterations (here: 3). Each run must end
with 2-3 concrete next investigations; the following run executes them and
says so in its header ("Iteration N — applies ..."). Stop when the
iterations are exhausted, or when the target is reached with all guardrails
clean. To avoid overfitting-by-iteration, tune on validation data and touch
the held-out test set once per run.

## Execution
`python run.py --prompt <prompt-file> --mode honest|flawed|variant`
(non-honest modes exist for teaching: they deliberately break a stated
rule and must say so in the report header).

The runner works from any directory and builds its own environment: on the
first run, if numpy, pandas or scikit-learn are missing, it calls
`setup_env.py`, which creates `.venv` (uv, else the venv module) and installs
`requirements.txt`, then re-runs itself inside it. Build it ahead of time with
`python3 setup_env.py`, check it with `--check`, rebuild with `--force`.

If the environment cannot be built — no network, no venv support — the run
does not fail: it falls back to the frozen results in `cache.json` and labels
the output `source: cache.json`, so the chain is still demonstrable. Pass
`--no-setup` to force that path deliberately.
