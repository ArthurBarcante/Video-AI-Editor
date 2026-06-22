from src.utils.cache_metadata import (
    get_cache_metadata_path,
    is_cache_valid,
    save_cache_metadata,
)


def test_cache_metadata_invalidates_when_source_changes(tmp_path) -> None:
    source_path = tmp_path / "source.json"
    output_path = tmp_path / "output.json"

    source_path.write_text('{"value": 1}', encoding="utf-8")
    output_path.write_text('{"result": 1}', encoding="utf-8")

    save_cache_metadata(output_path, [source_path])

    assert get_cache_metadata_path(output_path).exists()
    assert is_cache_valid(output_path, [source_path]) is True

    source_path.write_text('{"value": 2}', encoding="utf-8")

    assert is_cache_valid(output_path, [source_path]) is False
