extends PanelContainer

signal advance_pressed

func _ready() -> void:
    $Content/Advance.pressed.connect(func(): advance_pressed.emit())
    $Content/Speed.add_item("Normal")
    $Content/Speed.add_item("Fast")

func set_month(month: int) -> void:
    $Content/Month.text = "Month %d" % month
