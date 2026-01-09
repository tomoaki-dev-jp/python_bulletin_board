# Python Bulletin Board

Django 5 で動くシンプルな掲示板アプリです。板一覧 → スレ一覧 → レス投稿の流れで、2ch 風の挙動（sage、トリップ、dat 出力など）を試せます。

## 主な機能
- 板/スレ/レスの基本機能
- sage（メール欄に `sage` を含むと bump しない）
- トリップ（`name#password` 形式）
- 簡易 dat 出力（`/dat/<id>.dat`）
- 連投規制（スレ立て 10 秒、レス投稿 3 秒）
- アンカーリンク（`>>123`）

## 動作要件
- Python 3.12+
- 依存: `Django`, `mysqlclient`, `python-dotenv`（`app/requirements.txt`）

## ローカル実行
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

python app/manage.py migrate
python app/manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` を開きます。

### 初期データ（板の作成）
板は管理画面から作成してください。
```bash
python app/manage.py createsuperuser
# http://127.0.0.1:8000/admin/ から Board を作成
```

Django shell で作る場合:
```bash
python app/manage.py shell
```
```python
from board.models import Board
Board.objects.create(slug="vip", name="VIP", description="雑談")
```

## Docker で実行
```bash
docker compose up --build
```
- Web: `http://127.0.0.1:8000/`
- phpMyAdmin: `http://127.0.0.1:8081/`

注意: 現状 `app/config/settings.py` は SQLite を使う設定です。`docker-compose.yml` の MySQL は接続設定が未反映なので、MySQL を使う場合は settings を環境変数対応に変更してください。

## 主要 URL
- `/` : 板一覧
- `/<board_slug>/` : スレ一覧
- `/<board_slug>/thread/<thread_id>/` : スレ詳細
- `/<board_slug>/dat/<thread_id>.dat` : dat 出力

## 補足
- `DEBUG=True` の開発用設定です。運用時は `SECRET_KEY` と `DEBUG` などを適切に管理してください。
- `Board.max_posts_per_thread` に達するとスレは閲覧のみ（アーカイブ）になります。
