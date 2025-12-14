import os
import json
import requests
from google import genai
from amazon_paapi import AmazonApi # Amazon PA-APIのライブラリによってインポート名が異なる場合があります

# --- 1. 環境変数の読み込み ---
try:
    # Amazon PA-API
    AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']
    AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY']
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
    amazon_api = AmazonApi( 
        AMAZON_ACCESS_KEY, 
        AMAZON_SECRET_KEY, 
        AMAZON_PARTNER_TAG, 
        'JP' # 日本のリージョン
    )
except Exception as e:
    # PA-APIの初期化エラーは致命的ではないため、警告に留める
    print(f"警告: Amazon APIの初期化に失敗しました: {e}")
    # 処理を続行（静的データを使うため）

# --- 3. 定数/静的データの定義 ---

POST_ASINS = [
    'B08VN76PLB', # 例: ロジクール G502 HERO (ゲーミングマウス)
    'B0CSHCD6R1', # 例: Anker Soundcore Liberty 4 NC (ノイキャンイヤホン)
]

# PA-APIが使えない間の静的データ
STATIC_PRODUCT_DATA = {
    'B08VN76PLB': {
        'asin': 'B08VN76PLB',
        'title': 'ロジクール G502 HERO ゲーミングマウス レビュー',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Placeholder_for_discussion.png/240px-Placeholder_for_discussion.png', 
        'affiliate_url': 'https://amzn.to/4oWfQdE', # 実際のAmazon URLに修正
        'features': ['HERO 25Kセンサー搭載', 'ウェイト調整機能', 'プログラム可能な11個のボタン', '有線接続'],
        'description': 'Eスポーツでも人気のロジクールの名作有線ゲーミングマウス。正確性とカスタム性が魅力。',
    },
    'B0CSHCD6R1': {
        'asin': 'B0CSHCD6R1',
        'title': 'Anker Soundcore Liberty 4 NC ワイヤレスイヤホン レビュー',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Placeholder_for_discussion.png/240px-Placeholder_for_discussion.png',
        'affiliate_url': 'https://www.amazon.co.jp/dp/B0CSHCD6R1',
        'features': ['最大98.5%ノイズキャンセリング', 'LDAC対応', 'ワイヤレス充電対応', 'Bluetooth 5.3'],
        'description': '高音質と強力なノイズキャンセリングを両立した、人気の完全ワイヤレスイヤホン。',
    },
}

# --- 4. 関数定義 ---

def get_product_data(asin: str) -> dict or None:
    """
    Amazon PA-APIを使用して、特定ASINのガジェット情報を取得する。
    PA-APIが使えない場合は、静的データを使用する。
    """
    # 1. 静的データチェック (PA-API回避のメインロジック)
    if asin in STATIC_PRODUCT_DATA:
        print(f"ASIN: {asin} - PA-API回避のため静的データを使用します。")
        temp_data = STATIC_PRODUCT_DATA[asin].copy()
        
        # 内部リンク生成で使うため、affiliate_urlを更新 (もし未設定なら)
        if 'affiliate_url' not in temp_data or not temp_data['affiliate_url']:
            temp_data['affiliate_url'] = f"https://www.amazon.co.jp/dp/{asin}?tag={AMAZON_PARTNER_TAG}"

        return temp_data # 静的データがあればここで処理を終了し、データを返す
    
    # 2. PA-APIによる取得ロジック（静的データがないASINの場合のみ実行）
    try:
        # ItemsResultの取得（複数リソースを指定して詳細情報を得る）
        response = amazon_api.get_items(
            items=[{'id': asin, 'ItemType': 'ASIN'}], # ← 修正済みの正しい引数
            resources=[
                'ItemInfo.Title', 
                'Images.Primary.Large', 
                'Offers.Listings.0.Price', 
                'Offers.Listings.0.URLs', # アソシエイトURLを取得
                'ItemInfo.ContentInfo',
                'ItemInfo.Features',
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
            affiliate_url = item.offers.listings[0].urls.product_url if item.offers.listings[0].urls else ""

        # 特徴を箇条書きリストとして取得
        features = []
        if item.item_info.features and item.item_info.features.display_values:
            features = item.item_info.features.display_values
        
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


def generate_article_content(product_data: dict) -> str:
    """
    Gemini APIを使用して、ガジェットレビュー記事の本文（HTML）を生成する。
    """
    print("DEBUG: Geminiによる記事生成を開始します。") # 追加したデバッグ情報
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
        return response.text
        
    except Exception as e:
        print(f"Gemini APIによる記事生成中にエラーが発生しました: {e}")
        return f"<p>【エラー】記事生成に失敗しました: {e}</p>"


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
    
    print(f"--- WP投稿開始: {title} ---") 
    
    try:
        response = requests.post(api_url, headers=headers, json=post_data, auth=auth)
        response.raise_for_status()
        
        # 成功時の処理
        print(f"✅ 記事の投稿に成功しました！ URL: {response.json()['link']}")
        return response.json().get('link') # 投稿されたURLを返す
        
    except requests.exceptions.HTTPError as err:
        # HTTPエラー処理
        print(f"❌ WordPress投稿エラー (HTTP): {err}")
        print(f"ステータスコード: {response.status_code}")
        try:
            error_details = response.json()
            print(f"エラーコード: {error_details.get('code')}")
            print(f"エラーメッセージ: {error_details.get('message')}")
        except json.JSONDecodeError:
            print(f"エラーレスポンス本文: {response.text}")
        return None
        
    except Exception as e:
        # 予期せぬエラー
        print(f"❌ 予期せぬ投稿エラー: {e}")
        return None


# --- 5. メイン実行ブロック ---

if __name__ == '__main__':
    
    latest_post_info = None # 後の記事で内部リンクとして使うため、直前の記事情報を保持
    
    for i, asin in enumerate(POST_ASINS):
        print(f"\n================ 記事 {i+1}/{len(POST_ASINS)} の処理を開始 (ASIN: {asin}) ================")
        
        # 1. PA-API or 静的データからデータ取得
        product_data = get_product_data(asin)
        if not product_data:
            print(f"DEBUG: ASIN {asin} の商品データ取得に失敗しました。次の記事へスキップします。")
            continue 

        # 2. Geminiで記事本文（導入〜まとめ）を生成
        article_body_html = generate_article_content(product_data)
        
        # 3. 最終HTMLの組み立て
        
        # 3a. 商品リンクカラム（青ボタン）の作成
        product_col_html = build_product_column(
            product_data, 
            button_color='青', 
            button_text='AMAZONで見る⇒',
        )

        # 記事タイトル（H2）と商品カラムで開始
        final_content = f"<h2>{product_data['title']} レビュー</h2>" 
        final_content += product_col_html
        final_content += article_body_html # Geminiが生成した本文
        
        # 3b. 内部リンクカラム（黄ボタン）の追加
        if latest_post_info:
            # 2つ目以降の記事投稿時に実行される
            
            # 内部リンク用データを一時的にコピーして書き換え
            internal_link_data = latest_post_info.copy()
            internal_link_data['description'] = f"【あわせて読みたい】一つ前の記事『{internal_link_data['title']}』はこちらから！"
            
            internal_link_col_html = build_product_column(
                internal_link_data, 
                button_color='黄', 
                button_text='見に行く⇒',
            )
            final_content += "<h2>▼ こちらの記事も読まれています ▼</h2>"
            final_content += internal_link_col_html
            
        else:
            print("最初の記事のため、内部リンクはスキップします。")
            pass 

        # 4. WordPressへの投稿
        posted_url = post_article_to_wordpress(product_data['title'], final_content)

        # 5. 投稿に成功した場合、次の記事のために最新記事情報を更新
        if posted_url:
            # 最新記事情報を、今投稿した記事の情報で上書きする（次のループで内部リンクとして利用するため）
            latest_post_info = {
                'title': product_data['title'],
                'affiliate_url': posted_url, # ここには実際の記事URLを設定
                'image_url': product_data['image_url'],
                'description': product_data['description'],
            }