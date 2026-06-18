def publish_to_youtube(item: dict) -> dict:
    return {
        "platform": "youtube",
        "video_path": item["video_path"],
        "status": "not_implemented",
        "message": "Integração com YouTube ainda não implementada.",
    }
