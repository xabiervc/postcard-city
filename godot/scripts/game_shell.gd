extends Node

func _ready() -> void:
    var gameplay := get_node("CurrentScreen/Gameplay")
    gameplay.start_demo()
