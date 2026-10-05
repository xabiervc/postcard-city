extends Control

signal plot_selected(plot_id: String)

const GRID_WIDTH: int = 5
const GRID_HEIGHT: int = 5
const TILE_W: float = 118.0
const TILE_H: float = 59.0
const ORIGIN := Vector2(405.0, 116.0)

var state: Dictionary = {}
var hovered_plot: String = ""
var selected_plot: String = ""
var plots: Dictionary = {}
var preview_building: String = ""
var pulse: float = 0.0

func _ready() -> void:
    mouse_filter = Control.MOUSE_FILTER_STOP
    set_process(true)

func set_state(next_state: Dictionary) -> void:
    state = next_state
    selected_plot = str(state.get("selected_plot", ""))
    queue_redraw()

func set_selected_plot(plot_id: String) -> void:
    selected_plot = plot_id
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
        var plot_id: String = _plot_at(event.position)
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
    draw_rect(Rect2(Vector2.ZERO, size), Color("15242b"))
    draw_rect(Rect2(18, 18, size.x - 36, size.y - 36), Color("21414a"))
    _draw_waterline()
    plots.clear()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            _draw_plot(x, y)
    _draw_roads()
    _draw_plaza()
    _draw_population_activity()
    draw_string(ThemeDB.fallback_font, Vector2(34, 48), "OLD TOWN · BUILD, WATCH, ADAPT", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color("f4e5c0"))
    if not preview_building.is_empty() and not hovered_plot.is_empty():
        _draw_building(_plot_center(hovered_plot), preview_building, Color(1, 1, 1, 0.45), true)

func _draw_waterline() -> void:
    draw_colored_polygon(PackedVector2Array([Vector2(18, size.y - 130), Vector2(size.x - 18, size.y - 175), Vector2(size.x - 18, size.y - 18), Vector2(18, size.y - 18)]), Color("316b7a"))
    for i in range(8):
        var x: float = 38.0 + i * 100.0
        draw_line(Vector2(x, size.y - 92), Vector2(x + 48, size.y - 100), Color("5b9aaa"), 2.0)

func _draw_roads() -> void:
    draw_line(_iso_point(0, 2), _iso_point(4, 2), Color("d1b47b"), 12.0)
    draw_line(_iso_point(2, 0), _iso_point(2, 4), Color("c3a46f"), 10.0)
    draw_line(_iso_point(0, 0), _iso_point(4, 4), Color("a88962"), 6.0)

func _draw_plaza() -> void:
    var center: Vector2 = _iso_point(2, 2) + Vector2(0, -8)
    draw_colored_polygon(_tile_polygon(center), Color("cda969"))
    for offset in [Vector2(-24, -4), Vector2(0, -10), Vector2(24, -4)]:
        draw_circle(center + offset, 7.0, Color("5e956c"))
        draw_line(center + offset + Vector2(0, 5), center + offset + Vector2(0, 16), Color("624e38"), 3.0)

func _draw_plot(x: int, y: int) -> void:
    var plot_id: String = "%d_%d" % [x, y]
    var center: Vector2 = _iso_point(x, y)
    var polygon: PackedVector2Array = _tile_polygon(center)
    plots[plot_id] = _polygon_rect(polygon)
    var tile_color: Color = Color("3d6870") if (x + y) % 2 == 0 else Color("355e67")
    if plot_id == hovered_plot:
        tile_color = Color("70959a")
    if plot_id == selected_plot:
        tile_color = Color("d4ae67")
    draw_colored_polygon(polygon, tile_color)
    draw_polyline(PackedVector2Array([polygon[0], polygon[1], polygon[2], polygon[3], polygon[0]]), Color("aac0b5"), 1.2)
    var building_id: String = _building_at_plot(plot_id)
    if not building_id.is_empty():
        _draw_building(center, building_id, Color.WHITE, false)

func _polygon_rect(polygon: PackedVector2Array) -> Rect2:
    var min_x: float = polygon[0].x
    var max_x: float = polygon[0].x
    var min_y: float = polygon[0].y
    var max_y: float = polygon[0].y
    for point: Vector2 in polygon:
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
    var height: float = 30.0
    var width: float = 36.0
    var base: Vector2 = center + Vector2(0, -8)
    var palette: Dictionary = {"social_housing": Color("93bba8"), "hospital_upgrade": Color("df8174"), "commercial_block": Color("e1b56c"), "heritage": Color("c4925c")}
    var building_color: Color = palette.get(building_id, Color("a8b3b1"))
    var shadow: PackedVector2Array = PackedVector2Array([base + Vector2(-width, 12), base + Vector2(width + 18, 4), base + Vector2(width + 18, 13), base + Vector2(-width, 21)])
    draw_colored_polygon(shadow, Color(0.03, 0.08, 0.09, 0.38))
    var body: PackedVector2Array = PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, 14), base + Vector2(width, 0), base + Vector2(0, -14)])
    draw_colored_polygon(body, building_color * tint)
    draw_colored_polygon(PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, -height), base + Vector2(0, -14), base + Vector2(-width, 0)]), building_color.lightened(0.16) * tint)
    draw_colored_polygon(PackedVector2Array([base + Vector2(0, -height), base + Vector2(width, 0), base + Vector2(0, 14), base + Vector2(0, -14)]), building_color.darkened(0.12) * tint)
    for row in range(2):
        draw_line(base + Vector2(-19, -13 + row * 10), base + Vector2(-7, -9 + row * 10), Color("f7df9e"), 2.0)
        draw_line(base + Vector2(7, -9 + row * 10), base + Vector2(19, -13 + row * 10), Color("f7df9e"), 2.0)
    if building_id == "hospital_upgrade":
        draw_string(ThemeDB.fallback_font, base + Vector2(-8, -height - 4), "+", HORIZONTAL_ALIGNMENT_LEFT, 20, 18, Color("fff0d0"))
    if building_id == "commercial_block":
        draw_line(base + Vector2(-16, -height - 3), base + Vector2(16, -height - 3), Color("f2d49b"), 3.0)
    if preview:
        draw_polyline(PackedVector2Array([base + Vector2(-width, 0), base + Vector2(0, -height), base + Vector2(width, 0)]), Color("ffffff"), 2.0)

func _draw_population_activity() -> void:
    var population: int = int(state.get("population", 0))
    var count: int = clamp(5 + population / 3800, 5, 14)
    for index in range(count):
        var angle: float = pulse * 0.20 + float(index) * 1.7
        var point: Vector2 = ORIGIN + Vector2(cos(angle) * 210.0, 150.0 + sin(angle * 1.3) * 45.0)
        draw_circle(point, 3.0, Color("ffe5a8"))
