# wireflow

https://github.com/user-attachments/assets/cb711282-c979-4c08-837a-2dd4cf7f027d

[English](#english) · [日本語](#日本語)

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

### Share a map

A map is one HTML file with every screen and comment inside it, so you can pass it on like any file.

- **Open it.** Double-click the file. It opens in any browser, offline, with no setup.
- **Send it.** Share it like any file, in Slack, email or Drive, or put it on a static host to keep one link.
- **Put it in Notion.** Drag the file into a Notion page. It becomes an embedded web page that people can use in the page.
- **Put it in Figma.** Drag the file onto a Figma canvas. It becomes a code layer: press play to use the map there, or play it full screen.

The file is a snapshot, so render and share it again after changes. It holds every capture, so share it only where everyone who can open it may see the product.

#### Figma layers instead of a code layer

To get the map as regular Figma layers, open **View** and choose **Figma view**, or press ⌘\ (Ctrl+\ on Windows). The page then shows the whole map at full size, without toolbars, in the language and View settings you are using. Import that page with Figma's browser extension, then press Esc to go back. This copy is static, so hover, the language switch and edit mode do not work in it. To keep the map working in Figma, drag the file in as a code layer instead.

To open the Figma view from a link, add `?figma` to the end of the map's address (`?figma=en` or `?figma=ja` picks the language).

For a map saved on your computer, let the extension read local files first: in Chrome, open the extension's details and turn on **Allow access to file URLs**.

### Contents

- `SKILL.md`: instructions for the agent.
- `assets/flow-map.html`: the page template.
- `scripts/render_flow.py`: validates a bundle and renders one offline HTML file.
- `scripts/to_artifact.py`: optional; converts a rendered map into a claude.ai Artifact page.
- `examples/kiln-tasks/`: the fictional demo app, its captures and spec, and the rendered map.

### License

[MIT](LICENSE)

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

### マップを共有する

マップは、すべての画面とコメントを含む 1 つの HTML ファイルです。普通のファイルと同じように渡せます。

- **開く。** ファイルをダブルクリックします。準備なしで、オフラインでもどのブラウザでも開けます。
- **送る。** Slack、メール、Drive など、普通のファイルと同じように共有できます。静的ホスティングに置けば、同じリンクを使い続けられます。
- **Notion に置く。** ファイルを Notion のページにドラッグすると、埋め込みのウェブページになり、ページの中でそのまま操作できます。
- **Figma に置く。** ファイルを Figma のキャンバスにドラッグすると、コードレイヤーになります。再生ボタンを押すと Figma の中でマップを操作でき、フルスクリーンでも再生できます。

ファイルはその時点のスナップショットなので、変更したら生成し直して、もう一度共有してください。すべてのキャプチャが含まれるので、開ける人全員がその製品を見てよい場所でだけ共有してください。

#### コードレイヤーではなく Figma のレイヤーとして取り込む

普通の Figma のレイヤーとして取り込むには、「表示」メニューの **Figma 用の表示** を選ぶか、⌘\（日本語キーボードでは ⌘¥、Windows では Ctrl+\）を押します。ツールバーのない、マップ全体を原寸で並べたページになります。言語と「表示」メニューの設定は今のままです。このページを Figma のブラウザ拡張機能で取り込み、Esc で元の表示に戻ります。このコピーは静止していて、ホバー、言語の切り替え、編集モードは使えません。操作できる状態で Figma に置くには、ファイルをそのままドラッグしてコードレイヤーにします。

リンクから開く場合は、マップのアドレスの末尾に `?figma` を付けます（言語は `?figma=en` または `?figma=ja` で指定できます）。

パソコンに保存したマップの場合は、先に拡張機能がローカルのファイルを読めるようにしてください。Chrome では拡張機能の「詳細」を開き、**ファイルの URL へのアクセスを許可する** をオンにします。

### 構成

- `SKILL.md`：エージェント向けの手順。
- `assets/flow-map.html`：ページのテンプレート。
- `scripts/render_flow.py`：入力を検証し、オフラインで開ける HTML ファイルを 1 つ生成します。
- `scripts/to_artifact.py`：任意。生成したマップを claude.ai の Artifact ページに変換します。
- `examples/kiln-tasks/`：架空のデモアプリ、キャプチャ、spec、生成済みのマップ。

### ライセンス

[MIT](LICENSE)

---

Inspired by frontend-to-ue (BadbotAI/BadGoods). The renderer and template here are written from scratch. / BadbotAI/BadGoods の frontend-to-ue から着想を得ています。レンダラーとテンプレートは一から書き直しています。
