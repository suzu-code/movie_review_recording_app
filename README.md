# MovieNest -映画レビューアプリ-

## 🔍 概要
TMDb（The Movie Database）APIを利用して、映画の情報を検索・閲覧・評価・記録できるWebアプリケーションです。ユーザーは見た映画を検索し、ポスターやタイトル、感想などを記録できます。

## 🎯 開発背景
これは私が初めて作ったアプリケーションです。初めて作る上で、せっかくなら自分が日常的に使えるようなものをつくりたいと考えました。私は以前からスマホに映画の感想をメモしていたのですが、文章だけでは後から見直すのが難しく、どんな映画だったか思い出しづらいという問題点に気づきました。そこで、映画のポスターとともに感想を記録し、視覚的にも振り返りやすくすることを目指して開発しました。

## 🧩 主な機能
- 🎥 映画の検索（タイトルで検索 TMDb API）
  ![検索画面](/images/search_movie.png)
- 📋 映画の詳細表示（ポスター・あらすじ・公開日など）・映画の5項目評価＋レビュー入力＆保存
  ![映画詳細](/images/movie_review.png)
- ⭐ お気に入り・視聴済み・視聴予定で映画を分類
  ![映画リスト](/images/movie_list.png)

## 🔧 使用技術
- フロントエンド：HTML / CSS  
- バックエンド：Python (Flask)  
- データベース：SQLite  
- 外部API：TMDb API  
- インフラ：ローカル開発

## 🛠 工夫、挑戦した点
- 初めてのAPI連携に挑戦し、レスポンスから必要情報を抽出する処理を構築しました  
- 初めてデータベースを使用しユーザーの感想データ保存、追記できる機能を実装しました  
- ポスター画像を活用した視覚的にわかりやすいUIを意識して設計しました

## 📈 今後の改善点
- ユーザーごとのログイン機能の追加（レビューの管理範囲を個人単位に）  
- モバイル対応（レスポンシブデザイン）の強化  
- 公開レビュー機能や評価ランキング機能の追加

## ✍️ 自己PR
APIの利用からデータベース設計、フロントエンドの設計まで、全体を一人で設計・実装しました。自分の課題意識をアプリという形に落とし込み、使いやすさや再利用性を意識した設計・開発に挑戦できたと感じています。

---

## ▶️ アプリの起動方法（Run the App）

### 1. リポジトリをクローン：

 ```
   git clone https://github.com/suzu-code/movie_review_recording_app.git
   cd movie_review_recording_app
   ```

### 2. 仮想環境を作成・有効化（Unix/macOS の場合）：

   ```
   python -m venv venv
   source venv/bin/activate
   ```

   Windows の場合：

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

### 3. 必要パッケージをインストール：

   ```
   pip install -r requirements.txt
   ```

### 4. `.env` ファイルをプロジェクトのルートに作成し、必要な環境変数を記述（次項参照）

### 5. アプリを起動：

   ```
   flask run
   ```

## 環境変数の設定

本アプリでは TMDb API キーを環境変数で管理しています。  
プロジェクトルートに `.env` ファイルを作成し、以下の内容を記述してください：

   ```
   TMDB_API_KEY=YOUR_TMDB_API_KEY
   SECRET_KEY=任意のランダムな文字列（Flaskのセッション管理に使用）
   ```

📝 **注意：** 本アプリは [TMDb](https://www.themoviedb.org/) API を使用しており、ポスター画像等はすべて TMDb より取得されたものです。  
This product uses the TMDb API but is not endorsed or certified by TMDb.

