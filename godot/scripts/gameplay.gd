extends Control

var session := SimulationSession.new()
@onready var metric_panel: VBoxContainer = $MainLayout/LeftColumn/MetricPanel
@onready var event_log = $MainLayout/RightColumn/EventLog
@onready var timeline = $MainLayout/RightColumn/Timeline
@onready var postcard_compare = $PostcardCompare

func _ready() -> void:
    session.state_updated.connect(_on_state_updated)
    session.event_received.connect(_on_event_received)
    $MainLayout/MiddleColumn/DecisionPanel/Renegotiate.pressed.connect(func(): session.apply_intervention("renegotiate"))
    $MainLayout/MiddleColumn/DecisionPanel/SocialHousing.pressed.connect(func(): session.apply_intervention("social_housing"))
    timeline.advance_pressed.connect(session.advance_month)
    $ShowPostcard.pressed.connect(_show_postcard_comparison)

func start_demo() -> void:
    session.start_demo()
    _on_state_updated(session.state)

func _on_state_updated(current: Dictionary) -> void:
    _render_metrics(current)
    timeline.set_month(current.get("month", 0))
    event_log.set_entries(current.get("events", []))

func _on_event_received(event: Dictionary) -> void:
    event_log.add_entry(event.get("text", ""))

func _render_metrics(current: Dictionary) -> void:
    for child in metric_panel.get_children():
        child.queue_free()
    for item in [
        ["Budget", "EUR %.1fM" % (current.get("budget", 0.0) / 1000000.0)],
        ["Tourism pressure", "%.0f%%" % (current.get("tourism_pressure", 0.0) * 100.0)],
        ["Housing affordability", "%.0f%%" % (current.get("housing_affordability", 0.0) * 100.0)],
        ["Healthcare staffing", "%.0f%%" % (current.get("healthcare_staffing", 0.0) * 100.0)]
    ]:
        var card := preload("res://scenes/ui/metric_card.tscn").instantiate()
        metric_panel.add_child(card)
        card.set_metric(item[0], item[1])

func _show_postcard_comparison() -> void:
    session.capture_postcard("Historic Core", "After current decisions")
    postcard_compare.show_comparison(session.postcard_comparison())
    postcard_compare.visible = true
