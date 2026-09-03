"""Tray-only localhost download backend for the FrogGrab Edge extension."""
from __future__ import annotations

import ctypes
import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pystray
import imageio_ffmpeg
from PIL import Image
from yt_dlp import YoutubeDL

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "tubegrab.json"
DOWNLOAD_DIR = Path.home() / "Downloads"
JOBS: dict[str, dict] = {}
JOBS_LOCK = threading.Lock()


def config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8-sig"))


CFG = config()
TOKEN, PORT = CFG["token"], int(CFG.get("port", 17843))


def valid_video(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and (p.hostname or "").lower() in {
            "youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"
        } and (p.path == "/watch" and bool(parse_qs(p.query).get("v")) or p.hostname == "youtu.be")
    except ValueError:
        return False


def set_job(job_id: str, **values) -> None:
    with JOBS_LOCK:
        JOBS.setdefault(job_id, {}).update(values)


def run_download(job_id: str, url: str, kind: str) -> None:
    options = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title).180B [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "concurrent_fragment_downloads": 1,
        "retries": 3,
        # Bundled by imageio-ffmpeg, so users do not need a system FFmpeg install.
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
    }
    if kind == "mp3":
        options.update(
            format="bestaudio/best",
            postprocessors=[{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"}],
        )
    else:
        options.update(format="bestvideo*+bestaudio/best", merge_output_format="mp4")
    try:
        DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video") if info else "video"
        set_job(job_id, state="done", message=f"Saved {title}")
    except Exception as exc:
        message = str(exc).replace("ERROR:", "").strip()
        set_job(job_id, state="error", message=message[:300])


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args) -> None:
        pass

    def reply(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def authorized(self) -> bool:
        return self.headers.get("X-Frog-Token") == TOKEN

    def do_GET(self) -> None:
        if not self.authorized():
            self.reply(403, {"ok": False, "error": "Forbidden"})
            return
        job_id = parse_qs(urlparse(self.path).query).get("id", [""])[0]
        with JOBS_LOCK:
            job = JOBS.get(job_id)
        self.reply(200 if job else 404, {"ok": bool(job), **(job or {"error": "Unknown job"})})

    def do_POST(self) -> None:
        if self.path != "/download" or not self.authorized():
            self.reply(403, {"ok": False, "error": "Forbidden"})
            return
        try:
            length = min(int(self.headers.get("Content-Length", 0)), 8192)
            data = json.loads(self.rfile.read(length))
            url, kind = data["url"], data["kind"]
            if not valid_video(url) or kind not in {"mp3", "mp4"}:
                raise ValueError("Invalid download request")
            job_id = uuid.uuid4().hex
            set_job(job_id, state="working", message=f"Downloading {kind.upper()}…")
            threading.Thread(target=run_download, args=(job_id, url, kind), daemon=True).start()
            self.reply(202, {"ok": True, "jobId": job_id})
        except Exception as exc:
            self.reply(400, {"ok": False, "error": str(exc)})


def tray_image() -> Image.Image:
    return Image.open(ROOT / "extension" / "icons" / "icon128.png").convert("RGBA")


def main() -> None:
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\TubeGrabExtensionBackend")
    if ctypes.windll.kernel32.GetLastError() == 183:
        raise SystemExit(0)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 1.0}, daemon=True).start()

    def quit_app(icon, _item) -> None:
        server.shutdown()
        icon.stop()

    icon = pystray.Icon("TubeGrab", tray_image(), "TubeGrab downloader", pystray.Menu(
        pystray.MenuItem("Quit TubeGrab", quit_app, default=True)
    ))
    icon.run()


if __name__ == "__main__":
    main()
