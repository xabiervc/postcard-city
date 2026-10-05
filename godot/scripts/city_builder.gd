extends Control

var session := CityBuilderSession.new()
var selected_plot: String = "0_0"
var selected_building: String = ""
@onready var map_view: Control = $MainLayout/MiddleColumn/MapView
@onready var metric_panel: VBoxContainer = $MainLayout/LeftColumn/MetricPanel
@onready var zone_info: Label = $MainLayout/MiddleColumn/ZoneInfo
@onready var build_info: Label = $MainLayout/MiddleColumn/BuildInfo
@onready var event_log = $MainLayout/RightColumn/EventLog
@onready var timeline = $MainLayout/RightColumn/Timeline
@onready var crisis_panel = $CrisisPanel

func _ready() -> void:
    session.state_updated.connect(_on_state_updated)
    session.event_received.connect(_on_event_received)
    session.crisis_triggered.connect(_on_crisis_triggered)
    map_view.plot_selected.connect(_on_plot_selected)
    $MainLayout/MiddleColumn/BuildPanel/SocialHousing.pressed.connect(func(): _prepare_build("social_housing"))
    $MainLayout/MiddleColumn/BuildPanel/HospitalUpgrade.pressed.connect(func(): _prepare_build("hospital_upgrade"))
    $MainLayout/MiddleColumn/BuildPanel/CommercialBlock.pressed.connect(func(): _prepare_build("commercial_block"))
    $MainLayout/MiddleColumn/BuildPanel/Build.pressed.connect(_build_selected)
    timeline.advance_pressed.connect(session.advance_month)
    if timeline.has_signal("pause_pressed"):
        timeline.pause_pressed.connect(_toggle_pause)
    start_demo()

func start_demo() -> void:
    session.start_demo()

func _on_plot_selected(plot_id: String) -> void:
    selected_plot = plot_id
    session.select_plot(plot_id)
    map_view.set_selected_plot(plot_id)
    zone_info.text = "Plot %s\nClick a building type, then Build." % plot_id

func _prepare_build(building_id: String) -> void:
    selected_building = building_id
    var details: Dictionary = session.building_details(building_id)
    build_info.text = "%s\nCost: EUR %.1fM\n%s" % [str(details.get("name", "")), float(details.get("cost", 0.0)) / 1000000.0, str(details.get("description", ""))]
    map_view.set_preview(building_id)

func _build_selected() -> void:
    if selected_building.is_empty() or selected_plot.is_empty():
        return
    session.build(selected_building, selected_plot)
    selected_building = ""
    map_view.set_preview("")

func _toggle_pause() -> void:
    timeline.set_paused(not timeline.is_paused())

func _on_state_updated(current: Dictionary) -> void:
    _render_metrics(current)
    map_view.set_state(current)
    timeline.set_month(int(current.get("month", 0)))
    event_log.set_entries(current.get("events", []))

func _on_event_received(event: Dictionary) -> void:
    event_log.add_entry(str(event.get("text", "")))

func _on_crisis_triggered(crisis: Dictionary) -> void:
    crisis_panel.show_crisis(crisis)
    crisis_panel.visible = true

func _render_metrics(current: Dictionary) -> void:
    for child in metric_panel.get_children():
        child.queue_free()
    var values: Array[Array] = [["Budget", "EUR %.1fM" % (float(current.get("budget", 0.0)) / 1000000.0)], ["Population", "%d (%+d)" % [int(current.get("population", 0)), int(current.get("population_change", 0))]], ["Housing capacity", "%d" % int(current.get("housing_capacity", 0))], ["Housing affordability", "%.0f%%" % (float(current.get("housing_affordability", 0.0)) * 100.0)], ["Attractiveness", "%.0f%%" % (float(current.get("tourism_attractiveness", 0.0)) * 100.0)]]
    for item: Array in values:
        var card: PanelContainer = PanelContainer.new()
        var content: VBoxContainer = VBoxContainer.new()
        var title: Label = Label.new()
        var value: Label = Label.new()
        title.text = str(item[0])
        value.text = str(item[1])
        value.add_theme_font_size_override("font_size", 20)
        content.add_child(title)
        content.add_child(value)
        card.add_child(content)
        metric_panel.add_child(card)
