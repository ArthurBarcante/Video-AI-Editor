RENDER_PROFILES = {
    "fast": {
        "video_codec": "libx264",
        "audio_codec": "aac",
        "preset": "veryfast",
        "crf": "28",
    },
    "balanced": {
        "video_codec": "libx264",
        "audio_codec": "aac",
        "preset": "fast",
        "crf": "23",
    },
    "quality": {
        "video_codec": "libx264",
        "audio_codec": "aac",
        "preset": "medium",
        "crf": "20",
    },
}


def get_render_profile(profile_name: str) -> dict:
    return RENDER_PROFILES.get(profile_name, RENDER_PROFILES["fast"])
