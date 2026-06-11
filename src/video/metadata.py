from pathlib import Path

from src.rendering.ffmpeg_utils import run_ffprobe_json


def get_video_streams(video_path: str | Path) -> dict:
    data = run_ffprobe_json(video_path)
    return {"streams": data.get("streams", [])}


def parse_fps(rate: str | None) -> float:
    if not rate:
        return 0.0

    numerator, separator, denominator = rate.partition("/")
    try:
        if separator:
            denominator_value = float(denominator)
            if denominator_value == 0:
                return 0.0
            return round(float(numerator) / denominator_value, 3)
        return round(float(rate), 3)
    except ValueError:
        return 0.0


def get_video_metadata(video_path: str | Path) -> dict:
    data = run_ffprobe_json(video_path)
    format_data = data.get("format", {})
    streams = data.get("streams", [])

    video_stream = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == "video"
        ),
        {},
    )

    audio_stream = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == "audio"
        ),
        {},
    )

    return {
        "filename": Path(video_path).name,
        "duration": float(format_data.get("duration", 0)),
        "size_bytes": int(format_data.get("size", 0)),
        "bitrate": int(format_data.get("bit_rate", 0))
        if format_data.get("bit_rate")
        else 0,
        "video_codec": video_stream.get("codec_name"),
        "audio_codec": audio_stream.get("codec_name"),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "fps": parse_fps(video_stream.get("r_frame_rate")),
    }


def format_duration(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02}:{minutes:02}:{secs:02}"


def format_size(size_bytes: int) -> str:
    gb = size_bytes / (1024**3)
    return f"{gb:.2f} GB"
