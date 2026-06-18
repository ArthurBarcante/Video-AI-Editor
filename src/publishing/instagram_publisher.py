def publish_to_instagram(item: dict) -> dict:
    return {
        "platform": "instagram",
        "video_path": item["video_path"],
        "status": "not_implemented",
        "message": "Integração com Instagram ainda não implementada.",
    }
