extends Control

var session := SimulationSession.new()
@onready var metric_panel: VBoxContainer = $MainLayout/LeftColumn/MetricPanel
@onready var event_log = $MainLayout/RightColumn/EventLog
@onready var timeline = $MainLayout/RightColumn/Timeline
@onready var testimonies = $MainLayout/RightColumn/Testimonies
@onready var crisis_panel = $CrisisPanel
@onready var postcard_compare = $PostcardCompare
@onready var tradeoff: Label = $MainLayout/MiddleColumn/DecisionPanel/Tradeoff
@onready var confirm_button: Button = $MainLayout/MiddleColumn/DecisionPanel/Confirm

func _ready() -> void:
    session.state_updated.connect(_on_state_updated)
    session.event_received.connect(_on_event_received)
    session.crisis_triggered.connect(_on_crisis_triggered)
    session.outcome_changed.connect(_on_outcome_changed)
    $MainLayout/MiddleColumn/DecisionPanel/Renegotiate.pressed.connect(func(): _select("renegotiate"))
    $MainLayout/MiddleColumn/DecisionPanel/SocialHousing.pressed.connect(func(): _select("social_housing"))
    confirm_button.pressed.connect(_confirm)
    timeline.advance_pressed.connect(session.advance_month)
    $ShowPostcard.pressed.connect(_show_postcard_comparison)
    crisis_panel.crisis_choice.connect(session.resolve_crisis)

func start_demo() -> void:
    session.start_demo()
    _on_state_updated(session.state)

func _select(intervention_id: String) -> void:
    session.select_intervention(intervention_id)
    confirm_button.disabled = false
    tradeoff.text = "Renegotiation reduces pressure but limits growth." if intervention_id == "renegotiate" else "Social housing improves affordability but costs public funds."

func _confirm() -> void:
    session.confirm_intervention()
    confirm_button.disabled = true
    tradeoff.text = "Decision applied. Advance time to observe consequences."

func _on_state_updated(current: Dictionary) -> void:
    _render_metrics(current)
    timeline.set_month(current.get("month", 0))
    event_log.set_entries(current.get("events", []))
    testimonies.set_state(current)

func _on_event_received(event: Dictionary) -> void:
    event_log.add_entry(event.get("text", ""))

func _on_crisis_triggered(crisis: Dictionary) -> void:
    crisis_panel.show_crisis(crisis)
    crisis_panel.visible = true

func _on_outcome_changed(outcome: Dictionary) -> void:
    tradeoff.text = outcome.text

func _render_metrics(current: Dictionary) -> void:
    for child in metric_panel.get_children():
        child.queue_free()
    for item in [["Budget", "EUR %.1fM" % (current.get("budget", 0.0) / 1000000.0)], ["Tourism pressure", "%.0f%%" % (current.get("tourism_pressure", 0.0) * 100.0)], ["Housing affordability", "%.0f%%" % (current.get("housing_affordability", 0.0) * 100.0)], ["Healthcare staffing", "%.0f%%" % (current.get("healthcare_staffing", 0.0) * 100.0)]]:
        var card := preload("res://scenes/ui/metric_card.tscn").instantiate()
        metric_panel.add_child(card)
        card.set_metric(item[0], item[1])

func _show_postcard_comparison() -> void:
    postcard_compare.show_comparison(session.postcard_comparison())
    postcard_compare.visible = true
