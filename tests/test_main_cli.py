from argparse import Namespace
from pathlib import Path

import pytest

from main import parse_args, resolve_input_video


def test_parse_args_accepts_positional_video() -> None:
    args = parse_args(["input/live_01.mp4"])

    assert args.video_path == "input/live_01.mp4"
    assert args.video_option is None


def test_parse_args_accepts_video_option() -> None:
    args = parse_args(["--video", "input/live_01.mp4"])

    assert args.video_path is None
    assert args.video_option == "input/live_01.mp4"


def test_parse_args_rejects_two_video_paths() -> None:
    with pytest.raises(SystemExit):
        parse_args(["input/live_01.mp4", "--video", "input/live_02.mp4"])


def test_resolve_input_video_uses_explicit_path() -> None:
    args = Namespace(
        video_path=None,
        video_option="input/live_01.mp4",
    )

    assert resolve_input_video(args) == Path("input/live_01.mp4")
