"""
ヤフオク落札結果リサーチツール
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import urllib.parse


class YahooAuctionResearch:
    def __init__(self):
        """ChromeDriverを初期化"""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def search_keyword(self, keyword):
        """
        キーワードを検索して落札結果を取得

        Args:
            keyword (str): 検索キーワード

        Returns:
            dict: 検索結果データ
        """
        try:
            # キーワードをURLエンコード
            encoded_keyword = urllib.parse.quote(keyword)

            # 落札結果ページのURLを直接生成
            url = f"https://auctions.yahoo.co.jp/closedsearch/closedsearch?va={encoded_keyword}&b=1&n=50&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&p="

            # 直接落札結果ページにアクセス
            self.driver.get(url)

            # ページ読み込み待機
            time.sleep(3)

            # データ取得
            results = self.get_search_results()
            results['keyword'] = keyword

            return results

        except TimeoutException:
            print("エラー: ページの読み込みがタイムアウトしました")
            return None
        except NoSuchElementException as e:
            print(f"エラー: 要素が見つかりませんでした - {e}")
            return None
        except Exception as e:
            print(f"予期しないエラー: {e}")
            return None

    def get_search_results(self):
        """
        検索結果から落札データを取得

        Returns:
            dict: 落札件数、最安値、最高値、平均価格
        """
        results = {}

        try:
            # 180日の落札件数を取得
            count_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="allContents"]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/h2'))
            )
            count_text = count_element.text
            # テキストから数字を抽出（例: "180日間で1,234件落札されました" -> 1234）
            import re
            count_match = re.search(r'([\d,]+)件', count_text)
            if count_match:
                results['count'] = count_match.group(1).replace(',', '')
            else:
                results['count'] = count_text

            # 最安値を取得
            min_price_element = self.driver.find_element(
                By.XPATH, '//*[@id="allContents"]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/dl/dd/a[1]'
            )
            results['min_price'] = min_price_element.text

            # 最高値を取得
            max_price_element = self.driver.find_element(
                By.XPATH, '//*[@id="allContents"]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/dl/dd/a[2]'
            )
            results['max_price'] = max_price_element.text

            # 平均価格を取得
            avg_price_element = self.driver.find_element(
                By.XPATH, '//*[@id="allContents"]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/dl/dd/a[3]'
            )
            results['avg_price'] = avg_price_element.text

        except Exception as e:
            print(f"データ取得エラー: {e}")
            results['error'] = str(e)

        return results

    def close(self):
        """ブラウザを閉じる"""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """with文のサポート"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with文のサポート - 自動でブラウザを閉じる"""
        self.close()


def main():
    """メイン関数"""
    print("=== ヤフオク落札結果リサーチツール ===\n")

    keyword = input("検索キーワードを入力してください: ")

    # with文を使用して自動的にブラウザを閉じる
    with YahooAuctionResearch() as research:
        print(f"\n'{keyword}' を検索中...\n")
        results = research.search_keyword(keyword)

        if results and 'error' not in results:
            print("=" * 50)
            print(f"検索キーワード: {results.get('keyword', 'N/A')}")
            print("-" * 50)
            print(f"180日間の落札件数: {results.get('count', 'N/A')}件")
            print(f"最安値: {results.get('min_price', 'N/A')}")
            print(f"最高値: {results.get('max_price', 'N/A')}")
            print(f"平均価格: {results.get('avg_price', 'N/A')}")
            print("=" * 50)
        else:
            print("検索結果の取得に失敗しました")


if __name__ == "__main__":
    main()
