extends PanelContainer

signal advance_pressed
signal pause_pressed

var current_month: int = 0
var paused: bool = false

func _ready() -> void:
    $Content/Advance.pressed.connect(func(): advance_pressed.emit())
    $Content/Pause.pressed.connect(func(): pause_pressed.emit())

func set_month(month: int) -> void:
    current_month = month
    $Content/Month.text = "Month %d" % month

func set_paused(value: bool) -> void:
    paused = value
    $Content/Pause.text = "Resume" if paused else "Pause"

func is_paused() -> bool:
    return paused
