# Agents

The full process for new origami projects (fold research, true-size A4 sheets, symbol key, step panels, PDF, final result drawing, README/index, verification, git) lives in **siddick/vercel-sandbox → `.claude/agents/origami.md`** (source of truth).

In this repo:
- `spec/project.schema.json` – machine-readable project spec format
- `projects/01-paper-cup/spec.json` – worked example
- `tools/paper_cup.py` – generator for project #01 sheets + final.png
- Commit with `git -c user.name=Siddick -c user.email=siddick@gmail.com commit`; never change global config; push `gh-pages`.
