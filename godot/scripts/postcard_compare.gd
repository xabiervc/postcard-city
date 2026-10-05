extends PanelContainer

func show_comparison(text: String) -> void:
    $Content/Comparison.text = text

func _ready() -> void:
    $Content/Close.pressed.connect(func(): visible = false)
