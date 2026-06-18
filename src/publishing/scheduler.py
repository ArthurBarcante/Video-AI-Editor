def schedule_publish_item(item: dict) -> dict:
    return {
        "platform": item["platform"],
        "video_path": item["video_path"],
        "status": "not_implemented",
        "message": "Agendamento real ainda não implementado.",
    }
