# PDF確認用のフォント代替設定

Wordには大学指定のMS 明朝、見出しには仮のMS ゴシックを設定している。Linux環境にそのフォントがない場合に、PDF出力だけでNoto Serif CJK JP / Noto Sans CJK JPへ代替する設定をpdf-fonts.confに記録した。指定フォントをPDFへ埋め込んだものではない。

出力時はリポジトリ直下から `FONTCONFIG_FILE="$PWD/tools/pdf-fonts.conf"` をレンダラーの環境変数に指定する。Wordは初期生成スクリプトで作り直さず、最新版を直接編集する。出力後はPDFの全ページを画像で確認する。

40字×30行はOOXMLのdocGrid（linesAndChars、linePitch=448、charSpace=0）と本文幅8400twip・本文高13440twipで設定。本文10.5ポイント、A4縦。余白は指定がなかったためこのグリッドに合う仮値とした。MSフォントのあるWindows版Wordで、ページ設定の表示と最終レイアウトを確認する必要がある。
