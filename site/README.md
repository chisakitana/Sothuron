# 卒論ノートの閲覧サイト

URL：https://sothuron-study-hub.jocundwaxwing8.chatgpt.site

## 役割と正本

リポジトリ直下のWordが正本、PDFが同版の閲覧用。サイトは配布時点のコピーを表示する。ユーザーはSitesを開いて読み、編集依頼は会話で伝える。サイトに本文編集機能はない。本人用の閲覧範囲を維持する。

## ファイル

- index.html / style.css / app.js：画面、スマートフォン向けの表示、画像拡大、文字表示、文献の絞り込み。
- build.py：直下のWordから段落を抽出し、文献一覧とともにdist/data.jsonへ格納。PDF・Word・ログ・文献一覧・previewsの画像をdist/にコピーする。元のWord/PDFは変更しない。
- .openai/hosting.json：同じSitesを更新するためのIDと静的配布設定。秘密情報は含まない。
- dist/：実際の配布物。ログ・文献・Word・PDFは作成時点のコピーであり、自動でGitHubと同期するものではない。

## 更新手順

1. 直下のWordを保全して編集し、その最新版からPDFを出力する。
2. PDF全ページを画像にして確認し、直下のpreviews/を同版にそろえる。
3. ページ数が変わった場合はindex.html/app.jsの表示・拡大処理と件数を修正する。
4. リポジトリ直下で `python site/build.py` を実行する。python-docxが必要。
5. 同梱リンク、文献件数、原本とコピーの一致、JavaScript構文を確認する。ブラウザツールが利用可能ならスマートフォン幅で表示と操作を確認する。
6. Sitesスキルに沿って、hosting.jsonの同じproject_idのソースリポジトリへ変更を同期し、dist/と.openai/hosting.jsonを含むアーカイブを同じコミットから作成して配布する。ソース用認証情報を保存しない。
7. 公開成功を確認し、GitHub側にもソース・配布物・WORK_LOG.mdをコミットしてpushする。GitHub保存だけではサイトは更新されない。

## 現時点の検証範囲

初版は3ページの研究準備版。ファイル・リンク・文献件数・原本一致・JavaScript構文を確認。Sites配布成功を確認。ブラウザ操作ツールが提供されていないため、実際のiPhone上の表示・ダウンロードは未確認。
