import hashlib
from pathlib import Path


def build_video_cache_signature(video_path: str | Path) -> str:
    path = Path(video_path)
    stat = path.stat()
    raw_signature = f"{stat.st_size}:{stat.st_mtime_ns}"

    return hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()[:12]
