# scripts/main_poster.py

import os
import json
import requests
from google import genai
from amazon_paapi import AmazonApi # Amazon PA-APIのライブラリによってインポート名が異なる場合があります

# --- 1. 環境変数の読み込み ---
try:
 # Amazon PA-API
    AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']
    AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY'] # <-- ここを修正
    AMAZON_PARTNER_TAG = os.environ['AMAZON_PARTNER_TAG']
    
    # Gemini API
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    
    # WordPress API
    WORDPRESS_URL = os.environ['WORDPRESS_URL']
    WORDPRESS_USER = os.environ['WORDPRESS_USER']
    WORDPRESS_PASSWORD = os.environ['WORDPRESS_PASSWORD']

except KeyError as e:
    print(f"環境変数 {e} が設定されていません。GitHub Actions Secretsを確認してください。")
    exit(1)

# --- 2. クライアントの初期化 ---
# Gemini クライアント
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Amazon PA-API クライアント（リージョンは日本を想定）
try:
    # ↓↓↓ ここを修正: AmazonAPI ではなく AmazonApi (小文字の 'i') に変更 ↓↓↓
    amazon_api = AmazonApi( 
        AMAZON_ACCESS_KEY, 
        AMAZON_SECRET_KEY, 
        AMAZON_PARTNER_TAG, 
        'JP' # 日本のリージョン
    )
    # ↑↑↑ ここを修正 ↑↑↑
except Exception as e:
    print(f"Amazon APIの初期化に失敗しました: {e}")
    exit(1)

# ここから主要な関数を定義します...
# ASINは、新しい記事を作成するたびにこのリストを更新するか、
# 外部ファイルやデータベースから取得するロジックが必要です。
# 例として、ゲーミングマウスとノイキャンイヤホンのASINを仮置きします。

POST_ASINS = [
    'B07YQ4J3V7', # 例: ロジクール G502 HERO (ゲーミングマウス)
    'B0CSHCD6R1', # 例: Sony WF-1000XM5 (ノイキャンイヤホン)
]
# scripts/main_poster.py に追記

def get_product_data(asin: str) -> dict or None:
    """
    Amazon PA-APIを使用して、特定ASINのガジェット情報を取得する。
    """
    try:
        # ItemsResultの取得（複数リソースを指定して詳細情報を得る）
        # 'Images.Primary.Large', 'ItemInfo.Title', 'Offers.Listings.Price', 'ItemInfo.Features'など
        response = amazon_api.get_items(
            item_ids=[asin], 
            resources=[
                'ItemInfo.Title', 
                'Images.Primary.Large', 
                'Offers.Listings.0.Price', 
                'Offers.Listings.0.URLs', # アソシエイトURLを取得
                'ItemInfo.ContentInfo', # 商品の詳細スペック情報を含む可能性あり
                'ItemInfo.Features', # 箇条書きの特徴
            ]
        )
        
        # 結果の確認
        if not response.items_result or not response.items_result.items:
            print(f"ASIN: {asin} の商品情報が見つかりませんでした。")
            return None
        
        item = response.items_result.items[0]
        
        # 必要な情報の抽出
        title = item.item_info.title.display_value if item.item_info.title else "タイトル不明"
        image_url = item.images.primary.large.url if item.images and item.images.primary and item.images.primary.large else ""
        
        # アソシエイトリンクの取得
        affiliate_url = ""
        if item.offers and item.offers.listings:
            # 最初のオファーのURLを取得
            affiliate_url = item.offers.listings[0].urls.product_url if item.offers.listings[0].urls else ""

        # 特徴（詳細スペック）を箇条書きリストとして取得
        features = []
        if item.item_info.features and item.item_info.features.display_values:
            features = item.item_info.features.display_values
        
        # 商品概要（今回はPA-APIから直接「段落」として挿入したいので、
        # 簡易な説明をAPIから取得できる場合はそれを使用。ない場合はタイトルと特徴から構成する）
        description = title + "の特徴: " + "、".join(features[:3]) # 暫定的な説明文
        
        return {
            'asin': asin,
            'title': title,
            'image_url': image_url,
            'affiliate_url': affiliate_url,
            'features': features,
            'description': description,
        }

    except Exception as e:
        print(f"PA-API処理中にエラーが発生しました (ASIN: {asin}): {e}")
        return None

# main関数に仮の実行ロジックを追加してテスト
if __name__ == '__main__':
    # 環境変数の読み込み、クライアント初期化のコードは既に記述済みとして...
    
    # 最初のASINをテスト実行
    test_asin = POST_ASINS[0]
    product_data = get_product_data(test_asin)
    
    if product_data:
        print("\n--- PA-API 取得結果 ---")
        print(f"タイトル: {product_data['title']}")
        print(f"画像URL: {product_data['image_url']}")
        print(f"アソシエイトURL: {product_data['affiliate_url']}")
        print(f"特徴（一部）: {product_data['features'][:3]}")
    else:
        print(f"ASIN: {test_asin} のデータ取得に失敗しました。")
        # scripts/main_poster.py に追記

def generate_article_content(product_data: dict) -> str:
    """
    Gemini APIを使用して、ガジェットレビュー記事の本文（Markdown/HTML）を生成する。
    """
    title = product_data['title']
    features_list = "\n- ".join(product_data['features'])
    
    # 記事構成と出力形式を厳密に指定したプロンプト
    prompt = f"""
    あなたは、プロのガジェットレビュアーです。以下の商品情報に基づき、ブログ記事の本文を生成してください。
    
    # 商品情報
    タイトル: {title}
    特徴リスト（スペック情報）:
    - {features_list}
    
    # 記事の構成と要件（HTMLフォーマット）
    1. 導入：読者の興味を引くキャッチーな導入（<h1>タグは不要）
    2. 簡潔なスペック表：重要なスペック（例: 接続方法、バッテリー時間、重さなど）をHTMLの<table>タグで簡潔にまとめる。
    3. 詳細なレビュー：メリットを多めに、説得力のあるデメリットも1～2点混ぜて論理的に解説する。
    4. まとめ：記事全体の結論と、読者に購入を推奨する言葉。
    
    # 制約
    * 日本語で、親しみやすくプロフェッショナルなトーンで記述してください。
    * 出力は、WordPressにそのまま貼り付けられるHTML形式（<div>, <table>, <p>など）のみとし、余計な説明文や挨拶は一切含めないでください。
    """

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash', # 高速で高品質なモデル
            contents=prompt
        )
        
        # HTML形式の本文を返します
        return response.text
        
    except Exception as e:
        print(f"Gemini APIによる記事生成中にエラーが発生しました: {e}")
        return f"<p>【エラー】記事生成に失敗しました: {e}</p>"


# --- main_poster.py の実行部分（if __name__ == '__main__':）を更新 ---

# scripts/main_poster.py の実行部分（ if __name__ == '__main__': ）を修正

def build_product_column(data: dict, button_color: str, button_text: str) -> str:
    """
    商品情報に基づき、青または黄色のボタンを持つカラムHTMLを生成する。
    """
    color_map = {'青': '#007bff', '黄': '#ffc107'}
    text_color = 'white' if button_color == '青' else 'black'
    
    html = f"""
<div style="display: flex; gap: 20px; border: 1px solid #ccc; padding: 15px; border-radius: 8px; margin-bottom: 25px;">
    <div style="flex: 0 0 50%;">
        <img src="{data['image_url']}" alt="{data['title']}" style="width: 100%; height: auto;">
    </div>
    <div style="flex: 1 1 50%;">
        <p><strong>{data['title']}</strong></p>
        <p>{data['description']}</p>
        <div style="margin-top: 15px;">
            <a href="{data['affiliate_url']}" target="_blank" 
               style="background-color: {color_map.get(button_color, '#007bff')}; color: {text_color}; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                {button_text}
            </a>
        </div>
    </div>
</div>
"""
    return html


def post_article_to_wordpress(title: str, content: str):
    """
    WordPress APIに記事を投稿する。
    """
    api_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    headers = {
        'Content-Type': 'application/json'
    }
    # BASIC認証用のヘッダーを作成
    auth = requests.auth.HTTPBasicAuth(WORDPRESS_USER, WORDPRESS_PASSWORD)
    
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish', # 公開設定
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=post_data, auth=auth)
        response.raise_for_status()
        print(f"✅ 記事の投稿に成功しました！ URL: {response.json()['link']}")
        return True
    except requests.exceptions.HTTPError as err:
        print(f"❌ WordPress投稿エラー: {err}")
        print(f"レスポンス: {response.text}")
        return False
    except Exception as e:
        print(f"❌ 予期せぬ投稿エラー: {e}")
        return False


if __name__ == '__main__':
    
    # ----------------------------------------------------------------------
    # メインループ：2つの記事を処理
    # ----------------------------------------------------------------------
    latest_post_info = None # 後の記事で内部リンクとして使うため、直前の記事情報を保持
    
    for i, asin in enumerate(POST_ASINS):
        print(f"\n================ 記事 {i+1}/{len(POST_ASINS)} の処理を開始 (ASIN: {asin}) ================")
        
        # 1. PA-APIからデータ取得
        product_data = get_product_data(asin)
        if not product_data:
            continue # データ取得失敗時は次のASINへスキップ

        # 2. Geminiで記事本文（導入〜まとめ）を生成
        article_body_html = generate_article_content(product_data)
        
        # 3. 最終HTMLの組み立て
        
        # 3a. 商品リンクカラム（青ボタン）の作成
        product_col_html = build_product_column(
            product_data, 
            button_color='青', 
            button_text='AMAZONで見る⇒',
        )

        final_content = f"<h2>{product_data['title']} レビュー</h2>" # タイトルは記事本文内に入れる
        final_content += product_col_html
        final_content += article_body_html
        
        # 3b. 内部リンクカラム（黄ボタン）の追加
        if latest_post_info:
            # 2つ目以降の記事投稿時に実行される
            latest_post_info['description'] = f"【あわせて読みたい】一つ前の記事『{latest_post_info['title']}』はこちらから！"
            
            internal_link_col_html = build_product_column(
                latest_post_info, 
                button_color='黄', 
                button_text='見に行く⇒',
            )
            final_content += "<h2>▼ こちらの記事も読まれています ▼</h2>"
            final_content += internal_link_col_html
            
        else:
            # 1つ目の記事では、前の記事がないため、仮のデータを取得して次の記事のために備える
            print("最初の記事のため、内部リンクはスキップします。")
            # 内部リンク用として、一旦WPから最新の情報を取得
            # （このスクリプトが連続実行されることを前提に、ここではスキップし、次の投稿で使う）
            pass 

        # 4. WordPressへの投稿
        post_success = post_article_to_wordpress(product_data['title'], final_content)

        # 投稿に成功した場合、次の記事のために最新記事情報を更新
        if post_success:
            # 最新記事情報を、今投稿した記事の情報で上書きする（次のループで内部リンクとして利用するため）
            latest_post_info = {
                'title': product_data['title'],
                # WP APIのレスポンスから取得するのが確実だが、ここでは仮のデータ
                'url': '投稿完了後にWPから取得したURL', 
                'image_url': product_data['image_url'],
                'description': product_data['description'],
                'affiliate_url': '投稿完了後にWPから取得したURL', # URLをアソシエイトURLとして再利用
            }
            # scripts/main_poster.py に追記

# PA-APIが使えない間の静的データ
STATIC_PRODUCT_DATA = {
    'B07YQ4J3V7': {
        'asin': 'B07YQ4J3V7',
        'title': 'ロジクール G502 HERO ゲーミングマウス',
        'image_url': 'https://example.com/g502.jpg', # 暫定画像URL（Amazonから手動で取得）
        'affiliate_url': 'https://amzn.to/xxxxxx', # 暫定アソシエイトURL（Amazonリンク作成ツールで作成）
        'features': [
            'HERO 25Kセンサー搭載', 
            'ウェイト調整機能', 
            'プログラム可能な11個のボタン', 
            '高速スクロールホイール'
        ],
        'description': 'Eスポーツでも人気のロジクールの名作有線ゲーミングマウス。正確性とカスタム性が魅力。',
    },
    # 2つ目のASINも同様に静的データを用意
}
# scripts/main_poster.py の get_product_data 関数を以下のように変更

def get_product_data(asin: str) -> dict or None:
    """
    Amazon PA-APIを使用して、特定ASINのガジェット情報を取得する。
    資格がない場合は、静的データを使用する。
    """
    
    # -----------------------------------------------------
    # 1. 最初に静的データを試みる (PA-API回避策)
    # -----------------------------------------------------
    if asin in STATIC_PRODUCT_DATA:
        print(f"ASIN: {asin} - PA-API回避のため静的データを使用します。")
        temp_data = STATIC_PRODUCT_DATA[asin].copy()
        
        # アソシエイトURLをここで確実に生成しておく
        if 'affiliate_url' not in temp_data or not temp_data['affiliate_url']:
            temp_data['affiliate_url'] = f"https://www.amazon.co.jp/dp/{asin}?tag={AMAZON_PARTNER_TAG}"

        return temp_data
    
    # -----------------------------------------------------
    # 2. PA-APIによる取得ロジック
    # -----------------------------------------------------
    # 静的データがないASINの場合はPA-APIを叩く
    try:
        response = amazon_api.get_items(
            items=[
                {'id': asin, 'ItemType': 'ASIN'} # 新しい引数名と辞書形式
            ],
        )
        # ... (成功時のデータ抽出ロジック) ...
        
    except Exception as e:
        print(f"PA-API処理中にエラーが発生しました (ASIN: {asin}): {e}")
        # PA-APIが使えない場合も静的データがなければNoneを返す
        return None