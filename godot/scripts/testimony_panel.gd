extends PanelContainer

func set_state(state: Dictionary) -> void:
    var staffing := state.get("healthcare_staffing", 0.0) * 100.0
    var housing := state.get("housing_affordability", 0.0) * 100.0
    var decision := state.get("decision", null)
    var health_text := "Joana, healthcare worker: the hospital has enough cover to keep shifts open." if staffing >= 60.0 else "Joana, healthcare worker: reduced coverage means longer waits."
    var resident_text := "Mara, resident: housing investment is under pressure, but the district feels cared for." if decision == "protect_workers" else "Mara, resident: the budget is intact, but the hospital's decline reaches our homes."
    $Content/Entries.text = "%s\n\n%s\n\nAda, archivist: the postcard now records month %d and the decision %s." % [resident_text, health_text, state.get("month", 0), "is visible" if decision != null else "is pending"]
