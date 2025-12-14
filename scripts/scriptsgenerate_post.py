# .github/workflows/generate-blog-post.yml

name: 'Generate New Gadget Post'
on:
  workflow_dispatch: # 手動で実行できるようにする
  schedule:
    # 毎日午前9時 (UTC) に実行 (JSTだと午後6時)
    - cron: '0 0 * * *' 
    
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      # --- ステップ 2のスクリプトを実行 ---
      - name: Install dependencies
        run: pip install google-genai

      - name: Run post generation script
        id: post_script # スクリプトの出力を保存
        run: python scripts/generate_post.py
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

      # --- ステップ 3の自動コミット ---
      - name: Commit generated post
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'feat: New AI-generated gadget review post'
          file_pattern: 'posts/*.md' # postsフォルダ内のMarkdownファイルのみ対象