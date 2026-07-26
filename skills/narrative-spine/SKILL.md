---
name: narrative-spine
description: Design, audit, and refine the message architecture of a multi-level talk or document (talk → chapters → sections → beats). Use when the user wants a consistent overall message split into articulated sub-messages, explicit bridges between successive units, or an audit of scripts/transcripts against an intended narrative. Triggers on phrases like "overall message", "narrative consistency", "connect the sections", "message per chapter", "the talk should build".
---

# Narrative Spine

A talk is a tree of messages. This skill makes that tree explicit, then uses it as the contract every sentence must serve.

## The model

Four objects, at every level of the tree.

**Spine.** One sentence. The claim this unit exists to establish. A unit without a spine is decoration. A spine that needs two sentences is two units.

**Children.** The sub-units. Their spines, taken together, must entail the parent spine — nothing essential missing, nothing present that serves no parent. This is the composition test.

**Bridges.** One per seam between successive siblings. A bridge is a spoken sentence (or two) that does exactly two things: closes the left unit by restating its spine in past tense, and opens the right unit as a question the left one raised. Bridges are content, not transitions; "now let's talk about X" is not a bridge.

**Echoes.** Two or three motifs planted early and paid off late (an image, a number, a phrase). Echoes are what make the tree feel like one talk instead of stapled sections. Each echo lists its plant and its payoffs, by node.

## The artifact

Write the tree as a single YAML file (`narrative_spine.yaml`):

```yaml
talk:
  spine: "…"
  echoes:
    - motif: "…"
      plant: ch1.s3        # node where it first appears
      payoff: [ch2.s1, ch2.s3]
  chapters:
    - id: ch1
      spine: "…"
      bridge_out: "…"      # spoken at the chapter seam
      sections:
        - id: ch1.s1
          spine: "…"
          bridge_out: "…"  # spoken as the section's final beat
          beats:           # optional third level
            - "…"
```

## The audit

Run these checks against the actual scripts/transcripts. Report failures as a table: node → check → offending or missing text.

1. **Spine coverage.** For each section, point to the exact sentences in its script that state the spine. If you cannot quote them, the spine is unspoken — fail.
2. **Composition.** Read only the section spines of a chapter. Do they entail the chapter spine? List anything in the chapter spine no section carries, and any section whose spine serves no parent.
3. **Bridge presence.** The last beat of every unit must contain its `bridge_out`, close-paraphrased. The first beat of the next unit must not re-explain what the bridge already established.
4. **Orphan sweep.** Every beat maps to exactly one spine it serves. Beats that serve none are cut or rewritten; beats serving two are split.
5. **Echo ledger.** Each declared echo has its plant and every payoff present in the text, using recognisably the same wording or image.

## The refinement loop

1. Draft the tree top-down: talk spine → chapter spines → section spines → bridges → echoes. Get the tree approved before touching prose.
2. Audit existing text against the tree. Patch the smallest set of sentences that makes every check pass — usually the bridges and one spine sentence per section.
3. Only then polish style. Style edits never precede structure edits.

## Style constraints inherited by all prose this skill touches

Simple sentences. Concrete nouns. One idea per sentence. No slogans, no "X is not Y, X is Z" pivots, no self-congratulation. A claim is followed by its evidence or its mechanism, in the next sentence.
