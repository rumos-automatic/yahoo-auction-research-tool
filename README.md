# ヤフオク落札結果リサーチツール

ヤフオクの落札結果を自動で取得するPythonツールです。複数のキーワードを一度に検索し、落札件数や価格情報をCSV出力できます。

## 機能

- 🔍 **複数キーワード検索**: 一度に複数のキーワードで落札結果を検索
- 📊 **データ取得**: 180日間の落札件数、最安値、最高値、平均価格を自動取得
- 🖥️ **GUIアプリ**: 使いやすいグラフィカルユーザーインターフェース
- 💾 **CSV出力**: 検索結果をCSVファイルでエクスポート
- ⚡ **高速アクセス**: URLを直接生成して落札結果ページに即アクセス

## インストール

### 必要な環境

- Python 3.7以上
- Google Chrome
- ChromeDriver（Seleniumが自動でダウンロード）

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/rumos-automatic/yahoo-auction-research-tool.git
cd yahoo-auction-research-tool

# 必要なパッケージをインストール
pip install -r requirements.txt
```

## 使い方

### GUIアプリケーション（推奨）

```bash
python yahoo_auction_gui.py
```

1. テキストエリアに検索したいキーワードを1行ずつ入力
2. 「検索開始」ボタンをクリック
3. 結果が表形式で表示されます
4. 「CSV出力」ボタンで結果を保存できます

### コマンドライン版

```bash
python yahoo_auction_research.py
```

キーワードを入力すると、1つのキーワードの検索結果が表示されます。

## 取得できるデータ

- **キーワード**: 検索したキーワード
- **落札件数**: 過去180日間の落札件数
- **最安値**: 最も安い落札価格
- **最高値**: 最も高い落札価格
- **平均価格**: 平均落札価格

## ファイル構成

```
yahoo-auction-research-tool/
├── yahoo_auction_research.py  # コアロジック
├── yahoo_auction_gui.py       # GUIアプリケーション
├── requirements.txt           # 依存パッケージ
├── .gitignore                # Git除外設定
├── README.md                 # このファイル
├── CHANGELOG.md              # 変更履歴
└── メモ.txt                   # 開発メモ
```

## 技術仕様

- **言語**: Python
- **GUIフレームワーク**: Tkinter
- **Webスクレイピング**: Selenium WebDriver
- **ブラウザ**: Chrome（headlessモードには非対応）

## 注意事項

- ヤフオクの利用規約を遵守してください
- 短時間に大量のリクエストを送信しないでください
- スクレイピングの頻度には十分注意してください

## ライセンス

MIT License

## 作者

rumos-automatic

## 貢献

プルリクエストやイシューの報告を歓迎します！
