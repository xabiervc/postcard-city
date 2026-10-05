extends Control

func _ready() -> void:
    var city_scene: PackedScene = preload("res://scenes/screens/city_builder.tscn")
    add_child.call_deferred(city_scene.instantiate())
