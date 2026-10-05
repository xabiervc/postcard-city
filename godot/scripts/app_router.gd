extends Node

var game_opened: bool = false

func open_game() -> void:
    if game_opened:
        return
    game_opened = true
    var game_scene: PackedScene = preload("res://scenes/screens/gameplay.tscn")
    var child: Node = game_scene.instantiate()
    add_child.call_deferred(child)
