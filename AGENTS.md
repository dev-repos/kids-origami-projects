# Agents

The full process for new origami projects (fold research, true-size A4 sheets, symbol key, step panels, PDF, final result drawing, README/index, verification, git) lives in **siddick/vercel-sandbox → `.claude/agents/origami.md`** (source of truth).

## Video quality rules (every Origami for Kids episode)

1. **Smooth folds** — eased 3D-ish hinge of the flap over the crease at **≥ 30 fps**; no jumps/cuts between states; camera holds steady.
2. **Clear direction** — phase order: show fold line (valley dashed blue / mountain dash-dot red) → big direction arrow → highlight moving flap → (optional fingers) → fold → crease → **result outline check**. For **cuts** (`foldType: "cut"`): red cut line + scissors icon travelling along it + safety tip “ask a grown-up”.
3. **Sync with narration** — each step’s `say` + `cue` map phases to Azure TTS word timings; motion starts when the narrator says the cue; next step waits until narration finishes.

Details (phases, easing, beat props): origami.md §5 / §5b.

## In this repo

- `spec/project.schema.json` – machine-readable project spec (`foldType` includes `cut`; steps may have `say`, `cue`, `safetyTip`)
- `projects/01-paper-cup/spec.json` – worked example with `say` / `cue` for video sync
- `tools/paper_cup.py` – generator for project #01 sheets + final.png
- Commit with `git -c user.name=Siddick -c user.email=siddick@gmail.com commit`; never change global config; push `gh-pages`.
