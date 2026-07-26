---
name: ml-analysis
description: Run a data-analysis chain end to end from a written context prompt — question, data, features, model, split, evaluation against a baseline, and a report with a verified guardrail table and an empty human sign-off. Use when the user invokes /ml-analysis, points at a prompt file describing an analysis, or asks to run the workshop's water-treatment chain (honest, flawed, or variant mode).
---

# Skill: ml-analysis

## When to use
The user invokes `/ml-analysis <prompt-file>` or asks to run a data-analysis
chain end to end from a written context prompt.

## Principle
This skill is GENERIC. It knows no dataset, no task family, no domain.
Every problem-specific decision lives in the prompt file. The skill's job
is to read those decisions, execute them faithfully, and refuse to invent
what the prompt does not state.

## What this skill does
1. **Read the prompt file.** Extract: the question and target, the task
   type (regression, classification, clustering, forecasting, ...), the
   metric, the baseline rule, the data file, the preparation rules
   (imputation, exclusions), the split rule, and the report requirements
   (format, structure, sections).
2. **Question.** Restate the problem in one sentence, in the prompt's own
   terms. If the target, metric, or task type is missing: STOP and ask.
3. **Data.** Load the file the prompt names. Profile quality (missing
   values, outliers, duplicates). Apply exactly the preparation rules the
   prompt states, computing any fill statistics on training data only.
   Record every choice for the report.
4. **Features.** Build only inputs the prompt allows, available at
   prediction time. Apply the prompt's exclusions literally.
5. **Model & split.** Compute the baseline the prompt defines FIRST.
   Split exactly as the prompt instructs. Fit the simplest model of the
   family the prompt's task type implies; complexity must be earned
   against the baseline.
6. **Evaluate & report.** Score on held-out data only, next to the
   baseline. Generate the report in the format and structure the prompt
   requires, and always include: a guardrails checklist (each prompt rule,
   checked or failed), limits & uncertainty, and an EMPTY sign-off line.
   This skill NEVER ticks the sign-off.
7. **Next investigations (auto-research).** From the results, propose 2-3
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
