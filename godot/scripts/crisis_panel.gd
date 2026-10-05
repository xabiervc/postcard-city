extends PanelContainer

signal crisis_choice
var selected_intervention := ""

func show_crisis(crisis: Dictionary) -> void:
    $Content/Title.text = crisis.get("title", "Crisis")
    $Content/Situation.text = "%s\n\nLocation: %s\n\nCompare the interventions in the decision panel before confirming." % [crisis.get("text", ""), crisis.get("location", "District")]

func set_selected(intervention_id: String) -> void:
    selected_intervention = intervention_id

func _ready() -> void:
    $Content/Choice.pressed.connect(func(): crisis_choice.emit())
    $Content/Close.pressed.connect(func(): visible = false)
