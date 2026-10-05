extends Control

var session := SimulationSession.new()
var selected_intervention: String = ""
@onready var metric_panel: VBoxContainer = $MainLayout/LeftColumn/MetricPanel
@onready var event_log = $MainLayout/RightColumn/EventLog
@onready var timeline = $MainLayout/RightColumn/Timeline
@onready var testimonies = $MainLayout/RightColumn/Testimonies
@onready var crisis_panel = $CrisisPanel
@onready var postcard_compare = $PostcardCompare
@onready var tradeoff: Label = $MainLayout/MiddleColumn/DecisionPanel/Tradeoff
@onready var confirm_button: Button = $MainLayout/MiddleColumn/DecisionPanel/Confirm
@onready var map_view: Control = $MainLayout/MiddleColumn/MapView

func _ready() -> void:
    session.state_updated.connect(_on_state_updated)
    session.event_received.connect(_on_event_received)
    session.crisis_triggered.connect(_on_crisis_triggered)
    session.decision_applied.connect(_on_decision_applied)
    session.outcome_changed.connect(_on_outcome_changed)
    $MainLayout/MiddleColumn/DecisionPanel/ProtectWorkers.pressed.connect(func(): _select("protect_workers"))
    $MainLayout/MiddleColumn/DecisionPanel/DeferResponse.pressed.connect(func(): _select("defer_response"))
    confirm_button.pressed.connect(_confirm)
    timeline.advance_pressed.connect(session.advance_month)
    if timeline.has_signal("pause_pressed"):
        timeline.pause_pressed.connect(_toggle_pause)
    $ShowPostcard.pressed.connect(_show_postcard_comparison)
    start_demo()

func start_demo() -> void:
    session.start_demo()
    _on_state_updated(session.state)

func _select(intervention_id: String) -> void:
    selected_intervention = intervention_id
    session.select_intervention(intervention_id)
    var details: Dictionary = session.intervention_details(intervention_id)
    tradeoff.text = "%s\nCost: %s | Effect: %s | Risk: %s\n\n%s" % [details.get("title", ""), details.get("cost", ""), details.get("effect", ""), details.get("risk", ""), details.get("description", "")]
    confirm_button.disabled = false

func _confirm() -> void:
    session.confirm_intervention()
    confirm_button.disabled = true
    tradeoff.text = "Decision recorded. Advance time to reveal its consequence."

func _toggle_pause() -> void:
    if timeline.has_method("set_paused"):
        timeline.set_paused(not timeline.is_paused())

func _on_state_updated(current: Dictionary) -> void:
    _render_metrics(current)
    timeline.set_month(int(current.get("month", 0)))
    event_log.set_entries(current.get("events", []))
    testimonies.set_state(current)
    map_view.set_state(current)

func _on_event_received(event: Dictionary) -> void:
    event_log.add_entry(str(event.get("text", "")))

func _on_crisis_triggered(crisis: Dictionary) -> void:
    crisis_panel.show_crisis(crisis)
    crisis_panel.visible = true
    tradeoff.text = "Inspect the hospital zone, compare both interventions, then confirm one."

func _on_decision_applied(decision: Dictionary) -> void:
    crisis_panel.visible = false
    event_log.add_entry("Decision applied: %s" % str(decision.get("title", "")))

func _on_outcome_changed(outcome: Dictionary) -> void:
    tradeoff.text = str(outcome.get("text", ""))

func _make_metric_card(title: String, value: String) -> PanelContainer:
    var card := PanelContainer.new()
    var content := VBoxContainer.new()
    var name_label := Label.new()
    var value_label := Label.new()
    name_label.text = title
    value_label.text = value
    value_label.add_theme_font_size_override("font_size", 20)
    content.add_child(name_label)
    content.add_child(value_label)
    card.add_child(content)
    return card

func _render_metrics(current: Dictionary) -> void:
    for child in metric_panel.get_children():
        child.queue_free()
    var metrics: Array[Array] = [["Budget", "EUR %.1fM" % (float(current.get("budget", 0.0)) / 1000000.0)], ["Tourism pressure", "%.0f%%" % (float(current.get("tourism_pressure", 0.0)) * 100.0)], ["Housing affordability", "%.0f%%" % (float(current.get("housing_affordability", 0.0)) * 100.0)], ["Healthcare staffing", "%.0f%%" % (float(current.get("healthcare_staffing", 0.0)) * 100.0)], ["District health", "%.0f%%" % (float(current.get("district_health", 0.0)) * 100.0)]]
    for item: Array in metrics:
        metric_panel.add_child(_make_metric_card(str(item[0]), str(item[1])))

func _show_postcard_comparison() -> void:
    postcard_compare.show_comparison(session.postcard_comparison())
    postcard_compare.visible = true
