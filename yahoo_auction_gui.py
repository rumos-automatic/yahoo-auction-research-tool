"""
ヤフオク落札結果リサーチツール - GUIバージョン
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from yahoo_auction_research import YahooAuctionResearch
import csv
from datetime import datetime


class YahooAuctionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ヤフオク落札結果リサーチツール")
        self.root.geometry("900x600")

        # データ保存用
        self.results_data = []

        self.create_widgets()

    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # キーワード入力エリア
        keyword_frame = ttk.LabelFrame(main_frame, text="検索キーワード（1行に1つずつ入力）", padding="10")
        keyword_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.keyword_text = scrolledtext.ScrolledText(keyword_frame, height=8, width=80)
        self.keyword_text.pack(fill=tk.BOTH, expand=True)

        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.search_button = ttk.Button(button_frame, text="検索開始", command=self.start_search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="クリア", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.export_button = ttk.Button(button_frame, text="CSV出力", command=self.export_csv)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # プログレスバー
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # 結果表示エリア
        result_frame = ttk.LabelFrame(main_frame, text="検索結果", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Treeviewでテーブル表示
        columns = ('キーワード', '落札件数', '最安値', '最高値', '平均価格')
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)

        # 列の設定
        self.tree.heading('キーワード', text='キーワード')
        self.tree.heading('落札件数', text='落札件数')
        self.tree.heading('最安値', text='最安値')
        self.tree.heading('最高値', text='最高値')
        self.tree.heading('平均価格', text='平均価格')

        self.tree.column('キーワード', width=200)
        self.tree.column('落札件数', width=100)
        self.tree.column('最安値', width=100)
        self.tree.column('最高値', width=100)
        self.tree.column('平均価格', width=100)

        # スクロールバー
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ステータスバー
        self.status_label = ttk.Label(main_frame, text="待機中", relief=tk.SUNKEN)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # グリッド設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

    def start_search(self):
        """検索を開始"""
        keywords_text = self.keyword_text.get("1.0", tk.END).strip()

        if not keywords_text:
            messagebox.showwarning("警告", "キーワードを入力してください")
            return

        keywords = [kw.strip() for kw in keywords_text.split('\n') if kw.strip()]

        if not keywords:
            messagebox.showwarning("警告", "有効なキーワードを入力してください")
            return

        # ボタンを無効化
        self.search_button.config(state=tk.DISABLED)
        self.progress.start()

        # 別スレッドで検索実行
        thread = threading.Thread(target=self.search_keywords, args=(keywords,))
        thread.daemon = True
        thread.start()

    def search_keywords(self, keywords):
        """複数キーワードを検索"""
        try:
            research = YahooAuctionResearch()

            for i, keyword in enumerate(keywords, 1):
                self.update_status(f"検索中: {keyword} ({i}/{len(keywords)})")

                result = research.search_keyword(keyword)

                if result and 'error' not in result:
                    # 結果をテーブルに追加
                    self.add_result_to_table(result)
                else:
                    # エラー結果を追加
                    self.add_error_result(keyword)

            research.close()

            self.update_status(f"検索完了: {len(keywords)}件のキーワードを処理しました")

        except Exception as e:
            self.update_status(f"エラー: {str(e)}")
            messagebox.showerror("エラー", f"検索中にエラーが発生しました:\n{str(e)}")

        finally:
            # UIを元に戻す
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.search_button.config(state=tk.NORMAL))

    def add_result_to_table(self, result):
        """結果をテーブルに追加"""
        def add():
            values = (
                result.get('keyword', 'N/A'),
                result.get('count', 'N/A'),
                result.get('min_price', 'N/A'),
                result.get('max_price', 'N/A'),
                result.get('avg_price', 'N/A')
            )
            self.tree.insert('', tk.END, values=values)
            self.results_data.append(result)

        self.root.after(0, add)

    def add_error_result(self, keyword):
        """エラー結果をテーブルに追加"""
        def add():
            values = (keyword, 'エラー', 'エラー', 'エラー', 'エラー')
            self.tree.insert('', tk.END, values=values)

        self.root.after(0, add)

    def update_status(self, message):
        """ステータスを更新"""
        def update():
            self.status_label.config(text=message)

        self.root.after(0, update)

    def clear_results(self):
        """結果をクリア"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results_data = []
        self.update_status("結果をクリアしました")

    def export_csv(self):
        """結果をCSVファイルに出力"""
        if not self.results_data:
            messagebox.showwarning("警告", "出力するデータがありません")
            return

        # ファイル保存ダイアログ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"yahoo_auction_result_{timestamp}.csv",
            filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")]
        )

        if not filename:
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)

                # ヘッダー
                writer.writerow(['キーワード', '落札件数', '最安値', '最高値', '平均価格'])

                # データ
                for result in self.results_data:
                    writer.writerow([
                        result.get('keyword', 'N/A'),
                        result.get('count', 'N/A'),
                        result.get('min_price', 'N/A'),
                        result.get('max_price', 'N/A'),
                        result.get('avg_price', 'N/A')
                    ])

            messagebox.showinfo("成功", f"CSVファイルを保存しました:\n{filename}")
            self.update_status(f"CSVファイルを保存: {filename}")

        except Exception as e:
            messagebox.showerror("エラー", f"CSV出力中にエラーが発生しました:\n{str(e)}")


def main():
    root = tk.Tk()
    app = YahooAuctionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
