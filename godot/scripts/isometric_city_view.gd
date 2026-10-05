extends Control

signal plot_selected(plot_id: String)

const GRID_WIDTH: int = 4
const GRID_HEIGHT: int = 4
const TILE_W: float = 112.0
const TILE_H: float = 56.0
const ORIGIN := Vector2(360.0, 82.0)

var state: Dictionary = {}
var hovered_plot: String = ""
var plots: Dictionary = {}
var preview_building: String = ""
var pulse: float = 0.0

func _ready() -> void:
    mouse_filter = Control.MOUSE_FILTER_STOP
    set_process(true)

func set_state(next_state: Dictionary) -> void:
    state = next_state
    queue_redraw()

func set_preview(building_id: String) -> void:
    preview_building = building_id
    queue_redraw()

func _process(delta: float) -> void:
    pulse += delta
    queue_redraw()

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        hovered_plot = _plot_at(event.position)
        queue_redraw()
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        var plot_id := _plot_at(event.position)
        if not plot_id.is_empty():
            plot_selected.emit(plot_id)
            accept_event()

func _plot_at(point: Vector2) -> String:
    for plot_id: String in plots:
        if plots[plot_id].has_point(point):
            return plot_id
    return ""

func _iso_point(grid_x: int, grid_y: int) -> Vector2:
    return ORIGIN + Vector2((grid_x - grid_y) * TILE_W * 0.5, (grid_x + grid_y) * TILE_H * 0.5)

func _tile_polygon(center: Vector2) -> PackedVector2Array:
    return PackedVector2Array([center + Vector2(0, -TILE_H * 0.5), center + Vector2(TILE_W * 0.5, 0), center + Vector2(0, TILE_H * 0.5), center + Vector2(-TILE_W * 0.5, 0)])

func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, size), Color("0d151c"))
    draw_rect(Rect2(20, 18, size.x - 40, size.y - 36), Color("142733"))
    draw_string(ThemeDB.fallback_font, Vector2(40, 50), "HISTORIC CORE · ISOMETRIC DISTRICT", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color("f1e4c1"))
    plots.clear()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            _draw_plot(x, y)
    _draw_population_activity()
    if not preview_building.is_empty() and not hovered_plot.is_empty():
        _draw_building(_plot_center(hovered_plot), preview_building, Color(1, 1, 1, 0.35), true)

func _plot_center(plot_id: String) -> Vector2:
    var parts := plot_id.split("_")
    return _iso_point(int(parts[0]), int(parts[1]))

func _draw_plot(x: int, y: int) -> void:
    var plot_id := "%d_%d" % [x, y]
    var center := _iso_point(x, y)
    var polygon := _tile_polygon(center)
    plots[plot_id] = _polygon_rect(polygon)
    var selected: String = str(state.get("selected_plot", ""))
    var tile_color := Color("31505a") if (x + y) % 2 == 0 else Color("294650")
    if plot_id == hovered_plot:
        tile_color = Color("56747a")
    if plot_id == selected:
        tile_color = Color("c39b5b")
    draw_colored_polygon(polygon, tile_color)
    draw_polyline(PackedVector2Array([polygon[0], polygon[1], polygon[2], polygon[3], polygon[0]]), Color("91a9a5"), 1.5)
    var building_id: String = _building_at_plot(plot_id)
    if not building_id.is_empty():
        _draw_building(center, building_id, Color.WHITE, false)

func _polygon_rect(polygon: PackedVector2Array) -> Rect2:
    var min_x := polygon[0].x
    var max_x := polygon[0].x
    var min_y := polygon[0].y
    var max_y := polygon[0].y
    for point in polygon:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)
    return Rect2(Vector2(min_x, min_y), Vector2(max_x - min_x, max_y - min_y))

func _building_at_plot(plot_id: String) -> String:
    var buildings: Array = state.get("buildings", [])
    for building: Dictionary in buildings:
        if str(building.get("plot", "")) == plot_id:
            return str(building.get("type", ""))
    return ""

func _draw_building(center: Vector2, building_id: String, tint: Color, preview: bool) -> void:
    var height := 26.0
    var width := 34.0
    var base := center + Vector2(0, -8)
    var palette := {"social_housing": Color("8ab3a3"), "hospital_upgrade": Color("d77770"), "commercial_block": Color("d7aa63"), "heritage": Color("b78c59")}
    var building_color: Color = palette.get(building_id, Color("9aa6ad"))
    building_color = building_color * tint
    var body := PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, 13), base + Vector2(width, 0), base + Vector2(0, -13)])
    draw_colored_polygon(body, building_color)
    draw_colored_polygon(PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, -height), base + Vector2(0, -13), base + Vector2(-width, 0)]), building_color.lightened(0.12))
    draw_colored_polygon(PackedVector2Array([base + Vector2(0, -height), base + Vector2(width, 0), base + Vector2(0, 13), base + Vector2(0, -13)]), building_color.darkened(0.10))
    draw_line(base + Vector2(0, -height), base + Vector2(0, 13), Color("18242a"), 1.0)
    if building_id == "hospital_upgrade":
        draw_string(ThemeDB.fallback_font, base + Vector2(-8, -height - 4), "+", HORIZONTAL_ALIGNMENT_LEFT, 20, 18, Color("f7e9d2"))
    if preview:
        draw_polyline(PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, -height), base + Vector2(width, 0)]), Color("ffffff"), 2.0)

func _draw_population_activity() -> void:
    var population := int(state.get("population", 0))
    var count := clamp(4 + population / 4500, 4, 10)
    for index in range(count):
        var angle := pulse * 0.25 + float(index) * 1.7
        var point := ORIGIN + Vector2(cos(angle) * 170.0, 145.0 + sin(angle * 1.3) * 35.0)
        draw_circle(point, 3.0, Color("f4d9a1"))
