# wireflow

[English](#english) · [日本語](#日本語)

![Overview of a wireflow: screens grouped into bands, with key-path arrows between them](docs/preview-overview.png)

| Comments pinned to controls / 操作箇所に付いたコメント | Edit mode and the change list / 編集モードと変更リスト |
| --- | --- |
| ![Hovering a pin outlines the control and shows its comment](docs/preview-comments.png) | ![Edit mode with a new pin and the Changes panel](docs/preview-edit-mode.png) |

The screenshots use **Kiln Tasks**, a fictional app included in [`examples/kiln-tasks`](examples/kiln-tasks). / スクリーンショットはすべて架空のアプリ **Kiln Tasks**（[`examples/kiln-tasks`](examples/kiln-tasks)）のものです。

---

## English

An agent skill that turns a running frontend or prototype into a bilingual (English / Japanese) **wireflow**: a pannable canvas of real screen captures, key-path arrows between them, and numbered comments pinned to the controls they describe. The result is one self-contained HTML file that opens in any browser.

### What you get

- **Screens** captured from the running prototype, grouped into labelled bands.
- **Arrows** that start at the control that triggers them. Key paths are shown by default; the **All paths** switch adds the rest.
- **Comments** as numbered pins beside each control, with cards next to the screen. Hovering a pin shows its comment even when the card is off screen.
- **EN / 日本語** switch for every label and comment, a minimap, and a **Page IDs** switch plus a copy button for precise page names.
- **Edit mode**: edit comments, change key paths, drop new pins, or ask the AI agent to check something. **Copy for AI agent** copies a summary plus a JSON change list; paste it to your agent and it updates the map.

### Works with any agent

The skill is plain files: `SKILL.md` with instructions, an HTML template and two Python scripts (standard library only). Any coding agent that reads `SKILL.md` skills, can drive a browser (for example with Playwright) and can run Python can use it, such as Claude Code or Codex.

### Install

Clone it into the skills folder your agent reads. For Claude Code:

```bash
git clone https://github.com/charlie5188/wireflow.git ~/.claude/skills/wireflow
```

For other agents, clone it into that agent's skills folder, or point the agent at `SKILL.md`. Then ask the agent to make a wireflow of your prototype.

### Use without an agent

Write `flow-spec.json` and the captures yourself, then render:

```bash
python3 scripts/render_flow.py examples/kiln-tasks/bundle --out my-wireflow.html
```

Open [`examples/kiln-tasks/kiln-flow.html`](examples/kiln-tasks/kiln-flow.html) after cloning to try a finished map. See [SKILL.md](SKILL.md) for the procedure, the `flow-spec.json` format and how a pasted change list is applied.

### Contents

- `SKILL.md`: instructions for the agent.
- `assets/flow-map.html`: the page template.
- `scripts/render_flow.py`: validates a bundle and renders one offline HTML file.
- `scripts/to_artifact.py`: optional; converts a rendered map into a claude.ai Artifact page.
- `examples/kiln-tasks/`: the fictional demo app, its captures and spec, and the rendered map.
- `docs/`: preview images.

---

## 日本語

動いているフロントエンドやプロトタイプから、英語・日本語に対応した **ワイヤーフロー** を作るエージェント用スキルです。実際の画面キャプチャを並べたキャンバスに、主要な遷移の矢印と、操作箇所に付いた番号付きコメントを表示します。出力はブラウザで開ける HTML ファイル 1 つだけです。

### できること

- **画面**：動いているプロトタイプからキャプチャし、グループごとにまとめて配置します。
- **矢印**：遷移のきっかけになる操作箇所から始まります。初期表示は主要フローだけで、「すべてのフロー」スイッチでその他の遷移も表示します。
- **コメント**：操作箇所の横に番号付きのピン、画面の横にカードを表示します。ピンにホバーすると、カードが画面外にあってもその場で内容を確認できます。
- **EN / 日本語** の切り替え、ミニマップ、「ページ ID」スイッチ、正確なページ名をコピーするボタンがあります。
- **編集モード**：コメントの編集、主要フローの切り替え、ピンの追加、AI エージェントへの確認依頼ができます。「AI エージェント用にコピー」で要約と JSON の変更リストをコピーし、エージェントに貼り付けるとマップが更新されます。

### どのエージェントでも使えます

スキルの中身は、手順を書いた `SKILL.md`、HTML テンプレート、Python スクリプト 2 本（標準ライブラリのみ）だけです。`SKILL.md` 形式のスキルを読み込めて、ブラウザ操作（Playwright など）と Python の実行ができるエージェントなら使えます。Claude Code や Codex などで利用できます。

### インストール

エージェントが読み込むスキル用フォルダにクローンします。Claude Code の場合：

```bash
git clone https://github.com/charlie5188/wireflow.git ~/.claude/skills/wireflow
```

ほかのエージェントでは、そのエージェントのスキル用フォルダにクローンするか、`SKILL.md` を直接読み込ませてください。あとは「このプロトタイプのワイヤーフローを作って」と依頼するだけです。

### エージェントなしで使う

`flow-spec.json` とキャプチャを自分で用意して、次のコマンドで生成できます。

```bash
python3 scripts/render_flow.py examples/kiln-tasks/bundle --out my-wireflow.html
```

完成例はクローン後に [`examples/kiln-tasks/kiln-flow.html`](examples/kiln-tasks/kiln-flow.html) を開いて確認できます。手順、`flow-spec.json` の形式、貼り付けられた変更リストの反映方法は [SKILL.md](SKILL.md) を参照してください。

### 構成

- `SKILL.md`：エージェント向けの手順。
- `assets/flow-map.html`：ページのテンプレート。
- `scripts/render_flow.py`：入力を検証し、オフラインで開ける HTML ファイルを 1 つ生成します。
- `scripts/to_artifact.py`：任意。生成したマップを claude.ai の Artifact ページに変換します。
- `examples/kiln-tasks/`：架空のデモアプリ、キャプチャ、spec、生成済みのマップ。
- `docs/`：プレビュー画像。

---

Inspired by frontend-to-ue (BadbotAI/BadGoods). The renderer and template here are written from scratch. / BadbotAI/BadGoods の frontend-to-ue から着想を得ています。レンダラーとテンプレートは一から書き直しています。
