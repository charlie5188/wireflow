# frontend-to-flow

A Claude Code skill that turns a running frontend or prototype into a bilingual (English / Japanese) flow map: a pannable canvas of real screen captures, key-path arrows between them, and numbered comments pinned to the controls they describe.

Readers can switch on **Edit mode** in the page to edit comments, change key paths, drop new pins or ask the AI agent to check something, then **Copy for AI agent** and paste the result to an agent, which applies it to `flow-spec.json` and re-renders.

## Install

```bash
git clone https://github.com/charlie5188/frontend-to-flow.git ~/.claude/skills/frontend-to-flow
```

Then ask Claude Code to make a flow map of a prototype. See [SKILL.md](SKILL.md) for the procedure and the `flow-spec.json` format.

## Contents

- `SKILL.md`: instructions for the agent.
- `assets/flow-map.html`: the page template.
- `scripts/render_flow.py`: validates a bundle and renders one offline HTML file.
- `scripts/to_artifact.py`: converts a rendered map into a claude.ai Artifact page.

Inspired by frontend-to-ue (BadbotAI/BadGoods). The renderer and template here are written from scratch.
