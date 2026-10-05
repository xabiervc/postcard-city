extends Control

var session := SimulationSession.new()
var selected_intervention := ""
@onready var metric_panel: VBoxContainer = $MainLayout/LeftColumn/MetricPanel
@onready var event_log = $MainLayout/RightColumn/EventLog
@onready var timeline = $MainLayout/RightColumn/Timeline
@onready var testimonies = $MainLayout/RightColumn/Testimonies
@onready var crisis_panel = $CrisisPanel
@onready var postcard_compare = $PostcardCompare
@onready var tradeoff: Label = $MainLayout/MiddleColumn/DecisionPanel/Tradeoff
@onready var confirm_button: Button = $MainLayout/MiddleColumn/DecisionPanel/Confirm
@onready var map_view: Control = $MainLayout/MiddleColumn/MapView
@onready var pause_button: Button = $MainLayout/RightColumn/Timeline/Pause

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
    timeline.pause_pressed.connect(_toggle_pause)
    $ShowPostcard.pressed.connect(_show_postcard_comparison)
    crisis_panel.crisis_choice.connect(session.resolve_crisis)
    start_demo()

func start_demo() -> void:
    session.start_demo()
    _on_state_updated(session.state)

func _select(intervention_id: String) -> void:
    selected_intervention = intervention_id
    session.select_intervention(intervention_id)
    var details := session.intervention_details(intervention_id)
    tradeoff.text = "%s\nCost: %s | Effect: %s | Risk: %s\n\n%s" % [details.title, details.cost, details.effect, details.risk, details.description]
    confirm_button.disabled = false
    crisis_panel.set_selected(intervention_id)

func _confirm() -> void:
    session.confirm_intervention()
    confirm_button.disabled = true
    tradeoff.text = "Decision recorded. Advance time to reveal its consequence."

func _toggle_pause() -> void:
    timeline.set_paused(not timeline.is_paused())

func _on_state_updated(current: Dictionary) -> void:
    _render_metrics(current)
    timeline.set_month(current.get("month", 0))
    event_log.set_entries(current.get("events", []))
    testimonies.set_state(current)
    map_view.set_state(current)

func _on_event_received(event: Dictionary) -> void:
    event_log.add_entry(event.get("text", ""))

func _on_crisis_triggered(crisis: Dictionary) -> void:
    crisis_panel.show_crisis(crisis)
    crisis_panel.visible = true
    tradeoff.text = "Inspect the hospital zone, compare both interventions, then confirm one."

func _on_decision_applied(decision: Dictionary) -> void:
    crisis_panel.visible = false
    event_log.add_entry("Decision applied: %s" % decision.title)

func _on_outcome_changed(outcome: Dictionary) -> void:
    tradeoff.text = outcome.text

func _render_metrics(current: Dictionary) -> void:
    for child in metric_panel.get_children():
        child.queue_free()
    for item in [["Budget", "EUR %.1fM" % (current.get("budget", 0.0) / 1000000.0)], ["Tourism pressure", "%.0f%%" % (current.get("tourism_pressure", 0.0) * 100.0)], ["Housing affordability", "%.0f%%" % (current.get("housing_affordability", 0.0) * 100.0)], ["Healthcare staffing", "%.0f%%" % (current.get("healthcare_staffing", 0.0) * 100.0)], ["District health", "%.0f%%" % (current.get("district_health", 0.0) * 100.0)]]:
        var card := preload("res://scenes/ui/metric_card.tscn").instantiate()
        metric_panel.add_child(card)
        card.set_metric(item[0], item[1])

func _show_postcard_comparison() -> void:
    postcard_compare.show_comparison(session.postcard_comparison())
    postcard_compare.visible = true
