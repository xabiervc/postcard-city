extends PanelContainer

signal crisis_choice

func show_crisis(crisis: Dictionary) -> void:
    $Content/Title.text = crisis.get("title", "Crisis")
    $Content/Situation.text = crisis.get("text", "")

func _ready() -> void:
    $Content/Choice.pressed.connect(func(): crisis_choice.emit())
    $Content/Close.pressed.connect(func(): visible = false)
