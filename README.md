# Python Bulletin Board（2chライク掲示板）

Django + Docker で作られた **2chライク掲示板アプリ**です。  
匿名・ID・トリップ・sage・dat思想を尊重した、  
**「管理人も信用するな」設計**を目指しています。

> 嫌儲避難所用途・実験用途・学習用途を想定しています。

---

## 特徴

- 🧵 板 / スレ / レス 構造
- 🆔 日替わりID（スレ単位）
- 🔑 トリップ対応（`name#password`）
- 📉 sage対応（スレ上がらない）
- 📄 dat思想を意識した構造
- 🔌 Django REST Framework API 搭載
- 🐳 Docker / docker-compose 完全対応
- 🧪 fixture による初期データ投入対応

---

## 動作環境

- Docker Desktop
- docker compose（v2系）
- Windows / macOS / Linux（WSL可）

---

## Quick Start（最短起動）

```bash
git clone <このリポジトリのURL>
cd python_bulletin_board
docker compose up -d --build
```

### 初期セットアップ（重要）

1) データベース作成（必須）
```bash
docker compose run --rm web python manage.py migrate
```

2) テストデータ投入（fixture）
```bash
docker compose run --rm web python manage.py loaddata board_test
```

これで以下が自動作成されます：
- 板（例：vip）
- 初期スレッド
- 初期レス

3) 管理ユーザー作成
```bash
docker compose run --rm web python manage.py createsuperuser
```

※ パスワードはローカル用途なら簡易でもOK  
※ 公開運用では必ず強力なパスワードを設定してください

---

## アクセスURL

- 掲示板トップ: http://localhost:8000/
- VIP板: http://localhost:8000/vip/
- 管理画面: http://localhost:8000/admin/
- phpMyAdmin: http://localhost:8081/

---

## REST API（例）

スレ一覧
```bash
curl http://localhost:8000/api/vip/threads/
```

スレ詳細
```bash
curl http://localhost:8000/api/vip/thread/1/
```

レス投稿（API）
```bash
curl -X POST http://localhost:8000/api/vip/thread/1/posts/ \
  -H "Content-Type: application/json" \
  -d '{"name":"名無しさん","email":"sage","body":"API書き込みテスト"}'
```

---

## ディレクトリ構成（抜粋）

```
app/
├─ board/
│  ├─ models.py
│  ├─ views.py
│  ├─ api.py
│  ├─ serializers.py
│  ├─ fixtures/
│  │   └─ board_test.json
│  └─ templates/
├─ config/
│  └─ settings.py
├─ manage.py
└─ db.sqlite3（※Git管理しない）
```

---

## fixture について

本プロジェクトでは `db.sqlite3` を配布しません。  
代わりに fixture（初期データ）を使用します。

### fixture 再投入

```bash
docker compose run --rm web python manage.py loaddata board_test
```

---

## トラブルシューティング

### 管理画面でエラーが出る場合

ほとんどの場合、DBのズレです。

```bash
rm -f app/db.sqlite3 db.sqlite3
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py loaddata board_test
docker compose restart web
```

---

## ポリシー・注意事項

- IPアドレス等の個人情報は恒久保存しない設計
- 管理人による恣意的な操作を前提としない
- 本番公開時の法的責任は利用者・運用者自身に帰属

---

## ライセンス

MIT License  
自由に改変・再配布してください。

---

## 免責

このソフトウェアは学習・実験目的で提供されています。  
利用によって生じた問題について、作者は責任を負いません。
