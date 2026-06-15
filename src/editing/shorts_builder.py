from pathlib import Path

from src.config.paths import OUTPUT_SHORTS_DIR
from src.effects.sfx_effects import get_sfx_actions, resolve_sfx_path
from src.effects.zoom_effects import build_zoom_filter, get_zoom_actions
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path, run_command
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger

logger = get_logger(__name__)


def render_short(
    source_video: str | Path,
    short: dict,
    output_dir: str | Path | None = None,
    force: bool = False,
) -> Path:
    zoom_actions = get_zoom_actions(short.get("actions", []))
    video_filters = []

    if zoom_actions:
        first_zoom = zoom_actions[0]
        video_filters.append(
            build_zoom_filter(
                intensity=first_zoom.get("intensity", 1.2),
                target=first_zoom.get("target", "center"),
            )
        )

    sfx_actions = get_sfx_actions(short.get("actions", []))
    sfx_actions = sfx_actions[:2]

    source_video = Path(source_video)
    if output_dir is None:
        output_dir = OUTPUT_SHORTS_DIR

    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{short['id']}.mp4"
    ensure_safe_project_output_path(output_path)

    if output_path.exists() and not force:
        logger.info("Short já existe: %s", format_project_path(output_path))
        return output_path

    start = str(short["start"])
    duration = str(short["duration"])

    logger.info("Renderizando short: %s", short["id"])

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        start,
        "-i",
        str(source_video),
    ]

    sfx_inputs = []

    for action in sfx_actions:
        sfx_path = resolve_sfx_path(action.get("name", ""))

        if sfx_path:
            sfx_inputs.append((action, sfx_path))
            command.extend(["-i", str(sfx_path)])

    command.extend(["-t", duration])

    if video_filters:
        command.extend(["-vf", ",".join(video_filters)])

    if sfx_inputs:
        audio_filters = []

        audio_filters.append("[0:a]volume=1.0[a0]")

        mix_inputs = ["[a0]"]

        for index, (action, _sfx_path) in enumerate(sfx_inputs, start=1):
            relative_time = max(0, float(action["time"]) - float(short["start"]))
            delay_ms = int(relative_time * 1000)
            volume = float(action.get("volume", 0.3))

            audio_filters.append(
                f"[{index}:a]volume={volume},adelay={delay_ms}|{delay_ms}[sfx{index}]"
            )
            mix_inputs.append(f"[sfx{index}]")

        audio_filters.append(
            f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first[aout]"
        )

        command.extend(
            [
                "-filter_complex",
                ";".join(audio_filters),
                "-map",
                "0:v",
                "-map",
                "[aout]",
            ]
        )

    command.extend(
        [
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )

    run_command(command)

    logger.info("Short exportado: %s", format_project_path(output_path))

    return output_path


def render_shorts_from_edit_plan(
    edit_plan_path: str | Path,
    force: bool = False,
) -> list[Path]:
    edit_plan = load_json(edit_plan_path)

    source_video = edit_plan["source_video"]
    shorts = edit_plan.get("shorts", [])

    rendered = []

    for short in shorts:
        output_path = render_short(
            source_video=source_video,
            short=short,
            force=force,
        )

        rendered.append(output_path)

    logger.info("Shorts renderizados: %s", len(rendered))

    return rendered
