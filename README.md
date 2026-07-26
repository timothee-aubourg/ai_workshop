# Practical AI — fundamentals you can apply to your projects

Materials for the 90-minute Oxford session, OICSD–UPL faculty summer visit,
Somerville College, July 2026.

**Timothée Aubourg** · Nuffield Department of Clinical Neurosciences,
University of Oxford · timothee.aubourg@ndcn.ox.ac.uk

---

## Contents

| Path | What it is |
|---|---|
| `index.html` | The talk: 27 interactive pages, with presenter mode, transcript and voice. Self-contained — the reports and skill files are embedded, so it runs from any location. |
| `mobile.html` | Phone companion: the same content as card feeds and slide-up sheets. Add to home screen for a full-screen app. |
| `ml_report_honest.html` | Analysis report, **iteration 1** — guardrails enforced. |
| `ml_report_flawed.html` | Analysis report, **iteration 0** — the run that lies. |
| `ml_report_variant.html` | Analysis report, **iteration 2** — one domain feature added. |
| `ml_report_*.pdf` | The same three reports, printable. |
| `skills/ml-analysis/` | The generic skill: `SKILL.md`, `run.py`, `prompt.txt` (the frozen context prompt), `water_treatment.csv` (527 days, UCI id-106 schema, synthetic values), `cache.json`. |
| `skills/narrative-spine/` | The presentation-writing skill used to build the deck itself. |
| `present_deck.sh` / `.command` / `.bat` | Local presenting: serve the folder on `localhost:8765` and open the deck (Linux / macOS / Windows). |

## Deploy on GitHub Pages

This repository deploys as-is:

1. Push to GitHub (repository name `ai_workshop`).
2. Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.
3. The site goes live at `https://<your-user>.github.io/ai_workshop/`.

No build step, no server code, no dependencies — everything is static.
(`.nojekyll` is included so GitHub serves the files verbatim.)

## Using the deck

| Key | Action |
|---|---|
| `←` `→` | previous / next page |
| `↑` `↓` | step through the regions of a page |
| `←` `→` *(inside a region)* | move between that region's buttons |
| `Enter` | activate the focused button |
| `Esc` | leave the region — arrows go back to changing pages |
| `Space` | start / pause presenter mode |
| `E` | show or hide the transcript while presenting |
| `S` | script view |

The QR code in the bar encodes the page's own URL, so once deployed it points at
the live address, including the current page number.

## Structure

- **Intro** (3 pages) — title, speaker, agenda
- **Chapter 1 · What's going on in AI?** — a historic moment, a ladder of
  revolutions, intelligence as a commodity, six roles you can delegate
- **Chapter 2 · New challenges** — the energy bill, the social bill, the
  cognitive bill
- **Chapter 3 · Doing AI in your project** — what machine learning is (with the
  *AI or not AI?* activity), where you stand in the system, and one full chain
  run end to end
- **Close** — questions

Spoken script ≈ 51 minutes across the content pages, leaving room for the
activity, questions and discussion inside 90.

## Running the analysis yourself

Put `skills/ml-analysis/` and its `prompt.txt` into a Claude project, then:

```
/analysis prompt.txt
```

The skill reads the prompt, executes the chain end to end, ticks the guardrails
it verified, and returns a report whose sign-off line is empty — that signature
is yours. It also proposes the next investigations: the loop is specified for
three iterations, and the held-out test set is touched once per run.

## Notes

- Photographs (activity cards, speaker page) are hotlinked from Wikimedia
  Commons, NDCN and Saïd Business School and need an internet connection.
  Captions and monogram fallbacks remain if an image is blocked.
- To present locally, run the `present_deck` script for your platform (or any
  static server from this folder) so the PDFs and the `skills/` folder resolve;
  the deck itself is self-contained and also opens directly as a file.

## Sources cited in the deck

Energy and scaling: IEA *Energy and AI* (2025); Koomey et al., *Implications of
Historical Trends in the Electrical Efficiency of Computing*, IEEE Annals
(2011); Koomey & Naffziger, IEEE Spectrum (2015); Uptime Institute Global Data
Center Survey (2025); Lawrence Berkeley National Laboratory, interconnection
queues; Kaplan et al. (2020); Hoffmann et al. (2022); Bornmann et al. (2021);
Luccioni et al., arXiv:2501.16548.

Society and cognition: Challenger, Gray & Christmas reports; Anthropic; Gerlich
(2025); Lee et al., Microsoft/CHI (2025); Kosmyna et al., MIT.

Machine learning: Mitchell, *Machine Learning* (1997); Samuel (1959); Sutton &
Barto; Sculley et al., *Hidden Technical Debt in Machine Learning Systems*,
NeurIPS (2015); UCI Water Treatment Plant dataset schema (Poch 1993, CC BY 4.0 —
values regenerated for teaching).

Images: Wikimedia Commons contributors (CC BY-SA / CC0).
