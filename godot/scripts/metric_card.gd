extends PanelContainer

func set_metric(title: String, value: String) -> void:
    $Content/Title.text = title
    $Content/Value.text = value
    $Content/Trend.text = "Inspectable state"
