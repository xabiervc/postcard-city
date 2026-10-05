extends Control

var state: Dictionary = {}

func set_state(next_state: Dictionary) -> void:
    state = next_state
    queue_redraw()

func _draw() -> void:
    draw_rect(Rect2(0, 0, size.x, size.y), Color("172832"))
    draw_line(Vector2(40, size.y * 0.72), Vector2(size.x - 40, size.y * 0.72), Color("48636c"), 8.0)
    _draw_node(Vector2(size.x * 0.22, size.y * 0.32), "Historic core", state.get("map_nodes", {}).get("historic_core", 0.68), Color("d3a85f"))
    _draw_node(Vector2(size.x * 0.72, size.y * 0.30), "Hospital", state.get("map_nodes", {}).get("hospital", 0.46), Color("de7770"))
    _draw_node(Vector2(size.x * 0.52, size.y * 0.70), "Workers' housing", state.get("map_nodes", {}).get("workers_housing", 0.52), Color("80b89a"))
    draw_string(ThemeDB.fallback_font, Vector2(18, 24), "DISTRICT MAP · select a zone to read its condition", HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("dce8e8"))

func _draw_node(position: Vector2, label: String, health: float, base_color: Color) -> void:
    var color := base_color.lerp(Color("563c45"), 1.0 - clamp(health, 0.0, 1.0))
    draw_circle(position, 30.0, color)
    draw_circle(position, 34.0, Color(color, 0.35), false, 3.0)
    draw_string(ThemeDB.fallback_font, position + Vector2(-55, 54), label, HORIZONTAL_ALIGNMENT_CENTER, 110, 14, Color("dce8e8"))
    draw_string(ThemeDB.fallback_font, position + Vector2(-25, 5), "%d%%" % round(health * 100.0), HORIZONTAL_ALIGNMENT_CENTER, 50, 14, Color("10181d"))
