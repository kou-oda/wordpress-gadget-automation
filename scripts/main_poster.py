# scripts/main_poster.py

import os
import json
import requests
from google import genai
from amazon_paapi import AmazonAPI # Amazon PA-APIのライブラリによってインポート名が異なる場合があります

# --- 1. 環境変数の読み込み ---
try:
    # Amazon PA-API
    AMAZON_ACCESS_KEY = os.environ[AKPA5BMF2Y1765720761]
    AMAZON_SECRET_KEY = os.environ[0RJK4zxgKqK2kqqBoWO5PI9f6dKuS5g0iR15qBFk]
    AMAZON_PARTNER_TAG = os.environ[kou011209-22]
    
    # Gemini API
    GEMINI_API_KEY = os.environ[AIzaSyAAbPl25r_HIxYpR5bBI9ks9wS8B9yNZww]
    
    # WordPress API
    WORDPRESS_URL = os.environ[https://wwnaoya.com/]
    WORDPRESS_USER = os.environ[ODA]
    WORDPRESS_PASSWORD = os.environ[ODAKENTO777]

except KeyError as e:
    print(f"環境変数 {e} が設定されていません。GitHub Actions Secretsを確認してください。")
    exit(1)

# --- 2. クライアントの初期化 ---
# Gemini クライアント
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Amazon PA-API クライアント（リージョンは日本を想定）
try:
    amazon_api = AmazonAPI(
        AMAZON_ACCESS_KEY, 
        AMAZON_SECRET_KEY, 
        AMAZON_PARTNER_TAG, 
        'JP' # 日本のリージョン
    )
except Exception as e:
    print(f"Amazon APIの初期化に失敗しました: {e}")
    exit(1)

# ここから主要な関数を定義します...