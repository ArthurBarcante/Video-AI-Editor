def should_apply_zoom(action: dict) -> bool:
    return action.get("type") == "zoom"


def build_zoom_filter(
    intensity: float = 1.2,
    target: str = "center",
) -> str:
    zoom = max(1.0, min(float(intensity), 2.0))

    if target == "center":
        x_expr = f"(iw-iw/{zoom})/2"
        y_expr = f"(ih-ih/{zoom})/2"
    else:
        x_expr = f"(iw-iw/{zoom})/2"
        y_expr = f"(ih-ih/{zoom})/2"

    return (
        f"crop=iw/{zoom}:ih/{zoom}:{x_expr}:{y_expr},"
        "scale=iw:ih"
    )


def get_zoom_actions(actions: list[dict]) -> list[dict]:
    return [
        action
        for action in actions
        if should_apply_zoom(action)
    ]