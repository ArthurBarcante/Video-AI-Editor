def publish_to_tiktok(item: dict) -> dict:
    return {
        "platform": "tiktok",
        "video_path": item["video_path"],
        "status": "not_implemented",
        "message": "Integração com TikTok ainda não implementada.",
    }
