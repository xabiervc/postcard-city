extends PanelContainer

func set_state(state: Dictionary) -> void:
    $Content/Entries.text = "Mara, resident: housing affordability is now %.0f%%.\nJoana, healthcare worker: staffing is now %.0f%%.\nAda, archivist: the current trace will be preserved." % [state.get("housing_affordability", 0.0) * 100.0, state.get("healthcare_staffing", 0.0) * 100.0]
