---
created: 2026-06-02 21:34
updated: 2026-06-02 21:34
---
# プロジェクト名：music-wishlist

## このプロジェクトについて
- 概要：[一言で説明]
- 使用言語・フレームワーク：[例：Python、Flet]
- 関連Obsidianノート：[[1. Project/music-wishlist/README]]

---

# Obsidian連携ルール

## 読み取り（セッション開始時に必ず実行）

新しい会話の最初に以下を実行:

1. `/Users/drying/Library/CloudStorage/Dropbox/KnowledgeDB/3. Resources/AI/Knowledge/mistakes.md` を読む
2. `/Users/drying/Library/CloudStorage/Dropbox/KnowledgeDB/3. Resources/AI/Preferences/` 配下を全て読む
3. `/Users/drying/Library/CloudStorage/Dropbox/KnowledgeDB/1. Project/music-wishlist/` 配下を読む
4. 読み取った内容を踏まえて回答する

## 書き込み（該当したらその場で実行、後回し禁止）

- `Knowledge/`: バグ解決・ツールの発見・環境構築でハマって解決したこと
- `Decisions/`: 複数の選択肢から1つを選んだ判断（A vs B、なぜAか）
- `Preferences/`: 作業スタイル・好みの新たな発見
- `1. Project/music-wishlist/`: プロジェクトの状態・設計メモ・進捗

すべてのパスは `/Users/drying/Library/CloudStorage/Dropbox/KnowledgeDB/3. Resources/AI/` 配下。

## 書き込みフォーマット

必ずYAMLフロントマターを付与:

---
tags: [relevant, tags]
project: music-wishlist
related: [[Other Note]]
---

ファイル命名規則:
- Knowledge: topic-subtopic.md（例: python-list-comprehension.md）
- Decisions: YYYY-MM-DD-topic.md（例: 2026-06-02-framework-choice.md）

## 報告

Obsidianを読み書きしたら必ず明示する:
「Obsidian: 3. Resources/AI/Knowledge/xxx.md を読みました」
「Obsidian: 3. Resources/AI/Knowledge/xxx.md に書き込みました」

---

# 作業スタイル

- 回答は必ず日本語で
- 基本はステップバイステップで何をしているか説明する
- トークン消費が多い場面ではコードをサクッと出す
- 動くものを優先、仕組みの深掘りは後回し