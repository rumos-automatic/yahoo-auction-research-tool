# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-05

### Added
- 初回リリース
- Seleniumを使用したヤフオク落札結果の自動取得機能
- 複数キーワードの一括検索機能
- GUIアプリケーション（Tkinter使用）
  - テキストエリアでの複数キーワード入力
  - 表形式での検索結果表示
  - プログレスバー表示
  - ステータス表示
- CSV出力機能（検索結果のエクスポート）
- コマンドライン版ツール
- URLを直接生成して落札結果ページにアクセス

### Features
- **データ取得項目**
  - 180日間の落札件数
  - 最安値
  - 最高値
  - 平均価格

### Technical Details
- Python 3.7以上対応
- Selenium WebDriverによる自動化
- Chrome/ChromeDriver使用
- URLエンコードによる検索クエリ生成

### Documentation
- README.md追加
- CHANGELOG.md追加
- .gitignore設定
- requirements.txt作成
