---
name: wireflow
description: Turn a running frontend or prototype into a bilingual (English / Japanese) wireflow, a pannable canvas of real screen captures with key-path arrows between them and numbered, Figma-style comments pinned to the controls they describe. Readers can edit the map in the page and copy their changes for an AI agent to apply. Use when someone wants to explain how a prototype flows to people who will not run it, for design handoff, reviews or stakeholder walkthroughs, or when a pasted "Flow map changes" list needs applying. Not for redesigning the product or for claiming a backend exists.
license: MIT
metadata:
  version: "1.3"
  inspired-by: "frontend-to-ue (BadbotAI/BadGoods); the renderer and template here are rewritten"
---

# Wireflow

The output is one self-contained HTML file that opens offline in any browser. It works with any coding agent that can drive a browser, run Python and read this file. It shows:

- **Screens**: real captures of the product's key pages and states, grouped into labelled bands.
- **Arrows**: one per transition between two different screens, starting at the control that triggers it. Key paths are solid; the rest are dashed and hidden by default.
- **Comments**: a numbered pin beside the control and a card next to the screen with the same number. Orange cards are interactions, blue cards are notes about a state or rule.

There is no side panel. Everything a reader needs is on the canvas.

## Files

- `assets/flow-map.html`: the page template (all UI, both languages, edit mode).
- `scripts/render_flow.py <bundle-dir> --out <map>.html`: validates `flow-spec.json` and embeds the captures into one HTML file.
- `scripts/to_artifact.py <map>.html --out <page>.html --title "<Two To Four Words>"`: optional; converts the map into a claude.ai Artifact page.

A bundle directory holds `flow-spec.json` and `captures/<ID>.png`.

## Procedure

1. **Run the frontend** in an isolated browser (Playwright or similar), not the user's own browser profile. Use demo or test data only.
2. **List screens by meaning, not by DOM.** One screen per page or state that changes what a reader understands: each main page, each status that looks different, each dialog or menu that matters. Merge look-alike states and say so.
3. **Capture each screen** at one viewport size (default 1440×900). Hide dev overlays and move the pointer off the page first so no hover state leaks in.
4. **Measure anchors.** For every trigger control and every note that points at something, record its bounding box in the capture's own pixels (`{x, y, w, h}`). Only use measured boxes; omit `anchor` when there is nothing to point at. A box measured on one page is wrong on a capture where the list has scrolled or reordered; measure on that capture.
5. **Write `flow-spec.json`** (format below). Write every user-facing string in both languages. Keep control names exactly as the UI shows them, quoted, in both languages.
6. **Render** with `render_flow.py`.
7. **Check in a browser**: fit view, one zoomed screen per band, both languages, the All paths switch, a pin hover and click, a target chip jump, edit mode with Copy for AI agent, and Figma view. Fix overlaps by changing `grid` positions, not by editing the HTML.
8. **Privacy**: captures are images, so scan them by eye for real names, emails, customer data and tokens. Replace anything real with demo data before capturing.
9. **Deliver** the HTML file, or publish it (see Publishing). State the limits listed at the end.

## Choosing key paths

Decide this; do not ask the user screen by screen.

- Mark as `key` the transitions that tell the product's main story: the path a first-time reader must follow to understand what the feature is for. Usually the main entry, the main task and the step that changes data.
- Leave navigation chrome (search, mode switches, collapse), alternative entries and secondary states as non-key.
- Do not draw return paths (`isReturn: true`); they still appear as comments with a "Returns to" chip.
- A change that stays on the same page (`from == to`) is a comment, not an arrow. Say in its effect which other screen shows the result, if any.
- Aim for roughly 4 to 8 key paths. If more feel necessary, the map probably needs splitting into two files.

## flow-spec.json

```json
{
  "schemaVersion": "flow-1",
  "title": {"en": "Orders prototype", "ja": "注文プロトタイプ"},
  "defaultLang": "en",
  "viewport": {"width": 1440, "height": 900},
  "bands": [{"title": {"en": "Orders", "ja": "注文"}, "screens": ["ORD-01", "ORD-02"]}],
  "screens": [{
    "id": "ORD-01",
    "title": {"en": "Order list", "ja": "注文一覧"},
    "grid": {"col": 0, "row": 0},
    "capture": "captures/ORD-01.png",
    "notes": [{"anchor": {"x": 24, "y": 120, "w": 200, "h": 32},
               "text": {"en": "Overdue orders come first.", "ja": "期限切れの注文が先頭に表示されます。"}}]
  }],
  "transitions": [{
    "id": "TR-01", "from": "ORD-01", "to": "ORD-02", "key": true,
    "anchor": {"x": 24, "y": 180, "w": 600, "h": 48},
    "trigger": {"en": "Click an order row", "ja": "注文の行をクリック"},
    "effect": {"en": "Opens the order detail.", "ja": "注文の詳細を開きます。"}
  }]
}
```

- `id`: stable, ASCII, unique. Reuse IDs when updating a map; they are what change lists and URLs point at.
- `grid`: column and row. Put the starting screen in column 0, screens it leads to in column 1, and so on. Centre a hub screen vertically on the screens it fans out to. Each cell holds one screen.
- Optional layout tuning: `commentWidth` (default 620), `columnGap` (900), `rowGap` (960), all in capture pixels.
- `notes[].anchor` and `transitions[].anchor` are optional. `isReturn: true` marks a back path.

## Writing comments

- Interaction: the trigger is the control and action ("Click “Save”"); the effect is what visibly changes and where, in one sentence. Say when something is saved, because that is what readers most often get wrong.
- Note: one fact about a state or rule that the capture cannot show by itself (a count, an order, a condition). Skip layout descriptions; the capture already shows layout.
- Two to five comments per screen. A screen that needs more is usually two screens.
- Never describe behaviour you did not observe or read in the source. Mark anything inferred as such, or leave it out.

## What readers see and do

Layout, as in FigJam:

- **Top left**: the map title and a **View** menu with the language (EN / 日本語), the **All paths** switch, the **Page IDs** switch, **Figma view** and the legend. Language and switches are remembered per browser.
- **Top right**: the **Edit mode** switch, and **Changes (n)** once edit mode is on or edits exist.
- **Bottom right**: one panel with the minimap (click or drag to move) and the zoom controls (−, percentage, +, Fit all).

On the canvas:

- Drag pans; plain scroll pans; Ctrl or ⌘ plus scroll zooms at the pointer; `+`, `-` and `0` (fit all) work from the keyboard. `#SCREEN-ID` in the URL opens on that screen.
- **Figma view** (in the View menu, or ⌘\ / Ctrl+\) reloads the page as the whole map at 100 % on one plain, scrollable page with no toolbars; Esc or ⌘\ returns to the spot the reader left. `?figma` (or `?figma=ja`, `?figma=en`) opens it directly. It keeps the language, All paths and Page IDs last set in this browser (`=en` or `=ja` picks the language) and leaves out the edits saved in this browser. When someone wants the map in Figma, have them open Figma view and import the page with Figma's browser extension (a local file needs **Allow access to file URLs** turned on for the extension). If you have a tool that imports a web page into Figma, import the `?figma` page, never the normal view: that view shows only what fits in the window, too small to read. Do not rebuild the map in Figma by hand.
- Clicking a screen zooms to it and its comments. A comment's chip jumps to its target screen.
- Hovering a screen shows all of its arrows, even with All paths off, and dims the rest.
- Pins sit just outside the top corner of the control they mark, so the control stays visible. Hovering a pin outlines the control, lights its card, arrow and leader line, and shows the comment in a bubble beside the pin. Clicking a pin keeps the bubble open (Esc or a click on the canvas closes it). Hovering a card lights the same pin, outline and arrow.
- Comment cards hide when zoomed far out; pins and arrows stay.
- Screen IDs are hidden unless Page IDs is on. The copy button after each title copies the ID and the quoted title (`WRK-03 "Title"`, or `WRK-03「タイトル」` in Japanese), a precise name to paste into a request.

### Edit mode

Readers change the map in the page; an AI agent applies the result.

- The first time a reader turns on **Edit mode** in a browser, the Changes popover opens once with two short tips. Then a reader can:
  - edit a comment's text in place, in the current language;
  - **Delete** a comment (it stays visible, struck through, until applied; **Restore** undoes it);
  - tick **Key path** on an interaction to make it a key path, or untick it;
  - click anywhere on a screen to drop a new pin, write its text, and choose **Add note** (the text is added to the map) or **Ask AI agent** (the agent checks the prototype and updates the map; it never changes the product);
  - use **+ Ask the AI agent about this page** for a request without a position.
- **Changes (n)** opens one popover under the button. With no changes it shows the tips. With changes it shows a one-line summary ("4 changes on 2 pages"), **Clear all** (click twice) and **Copy for AI agent**. The summary expands to one short line per change, grouped by page in map order, each with Undo. Clicking a page name closes the popover and moves the canvas to that page, where each change is marked on its card. The copied text is a summary for people followed by a JSON block for the agent. Edits stay in that browser until cleared; they are not shared with other viewers.

## Applying a pasted change list

A pasted text that starts with `Flow map changes:` came from Copy for AI agent. Apply its JSON block to `flow-spec.json`, then re-render and re-publish. Each entry has an `op`:

| op | Apply to flow-spec.json |
| --- | --- |
| `editText` | Set `field` (`trigger`, `effect` or `text`) in `lang` on the transition (`transition`) or on the screen's note (`note` index). When `otherLanguageNeedsUpdate` is true, translate the new text into the other language too. |
| `delete` | Remove a note outright. An interaction is real behaviour, so before removing a transition confirm with the person that the path should leave the map. |
| `setKeyPath` | Set `key` on the transition. |
| `addNote` | Append a note to the screen with this `anchor` (or none) and the text in both languages. Check the anchor against the capture and snap it to the control it points at. |
| `addRequest` | Do not add as text. Investigate in the running prototype, then add, change or recapture screens and comments as the request asks, and report what changed and what could not be done. |

`comment` numbers are the page's display numbers at the time of copying; identify targets by `screen`, `transition` and `note` instead.

## Sharing

The map is one file with everything embedded, so it can be shared as an attachment or hosted on any static host (an internal file share, GitHub Pages, an S3 bucket). Hosting it keeps one link that you update in place.

- Keep `flow-spec.json` next to the published page, so an agent given the link can read the exact spec.
- If the captures show unreleased product, host it where only the intended people can open it.
- To update, re-render and replace the file at the same location.

### If your agent can publish claude.ai Artifacts

1. Run `to_artifact.py` on the rendered map with a two-to-four-word title.
2. Publish the page with `flow-spec.json` as a supporting file.
3. Tell the person the page is private until they share it from its Share menu.
4. Republish the same file path to keep the link.
5. If the agent has a tool for Artifact comments, answer comments there: make the change in the template or spec, re-render, republish, and reply with what changed and the new version. Leave resolving to people.

## Limits to state when delivering

- Screens are images, not editable layers.
- Only the observed paths are drawn; failures and edge cases appear only if they were reached.
- Name any states that were merged or left out.
- Edits made in the page live in one browser until copied and applied.
