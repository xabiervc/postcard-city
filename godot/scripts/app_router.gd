extends Node

var shell_scene := preload("res://scenes/app/game_shell.tscn")
var current_shell: Node

func open_game() -> void:
    if current_shell:
        current_shell.queue_free()
    current_shell = shell_scene.instantiate()
    get_tree().root.add_child(current_shell)
