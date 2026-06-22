TRANSCRIPTION_PROFILES = {
    "fast": {
        "beam_size": 1,
        "best_of": 1,
        "word_timestamps": False,
        "condition_on_previous_text": False,
        "vad_filter": True,
        "vad_parameters": {
            "min_silence_duration_ms": 500,
        },
    },
    "balanced": {
        "beam_size": 3,
        "best_of": 3,
        "word_timestamps": False,
        "condition_on_previous_text": True,
        "vad_filter": True,
        "vad_parameters": {
            "min_silence_duration_ms": 700,
        },
    },
    "quality": {
        "beam_size": 5,
        "best_of": 5,
        "word_timestamps": False,
        "condition_on_previous_text": True,
        "vad_filter": True,
        "vad_parameters": {
            "min_silence_duration_ms": 1000,
        },
    },
}


def get_transcription_profile(profile_name: str) -> dict:
    return TRANSCRIPTION_PROFILES.get(
        profile_name,
        TRANSCRIPTION_PROFILES["fast"],
    )
