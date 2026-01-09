import base64
import hashlib
import re
from datetime import date

ANCHOR_RE = re.compile(r"(>>\d+)")

def compute_thread_id(ip: str, thread_id: int, secret: str, day: date | None = None) -> str:
    """日替わり＆スレごとID（2chっぽい）"""
    if day is None:
        day = date.today()
    raw = f"{ip}|{thread_id}|{day.isoformat()}|{secret}".encode("utf-8")
    h = hashlib.sha256(raw).digest()
    # base32で短く
    s = base64.b32encode(h).decode("ascii").rstrip("=")
    return s[:8]  # ID:XXXXXXXX

def compute_ip_hash(ip: str, secret: str) -> str:
    """DBに生IPを保存しない用（内部識別用）"""
    raw = f"{ip}|{secret}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def render_trip(name: str, secret: str) -> tuple[str, str | None]:
    """
    名前欄に `name#password` が来たら簡易トリップ生成
    返り値: (表示名, trip)
    """
    if "#" not in name:
        return name.strip() or "名無しさん", None

    base, pw = name.split("#", 1)
    base = base.strip() or "名無しさん"
    pw = pw.strip()

    raw = f"{pw}|{secret}".encode("utf-8")
    h = hashlib.sha1(raw).digest()
    trip = base64.b64encode(h).decode("ascii")
    trip = trip.replace("+", ".").replace("/", "_")
    trip = trip[:10]
    return base, f"◆{trip}"

def link_anchors(text: str) -> str:
    """本文の >>123 をリンク化（テンプレ側で safe で使う）"""
    def repl(m):
        s = m.group(1)         # >>123
        num = s[2:]            # 123
        return f'<a href="#res-{num}">{s}</a>'
    return ANCHOR_RE.sub(repl, text)
