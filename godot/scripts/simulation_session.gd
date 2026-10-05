class_name SimulationSession
extends RefCounted

signal state_updated(state: Dictionary)
signal event_received(event: Dictionary)
signal crisis_triggered(crisis: Dictionary)
signal decision_applied(decision: Dictionary)
signal outcome_changed(outcome: Dictionary)

const MAX_MONTHS: int = 6
var state: Dictionary = {}
var postcards: Array[Dictionary] = []
var selected_intervention: String = ""
var crisis_active: bool = false
var crisis_resolved: bool = false
var initial_snapshot: Dictionary = {}
var outcome_emitted: bool = false

func start_demo() -> void:
    state = {"month": 0, "budget": 12000000.0, "tourism_pressure": 0.62, "housing_affordability": 0.54, "healthcare_staffing": 0.71, "district_health": 0.60, "map_nodes": {"hospital": 0.46, "workers_housing": 0.52, "historic_core": 0.68}, "project_status": "baseline", "events": ["Month 0: the historic core is stable but fragile."], "decision": null, "causal_chain": []}
    postcards.clear()
    selected_intervention = ""
    crisis_active = false
    crisis_resolved = false
    outcome_emitted = false
    capture_postcard("Historic Core", "Before the hospital staffing crisis", "baseline")
    initial_snapshot = state.duplicate(true)
    state_updated.emit(state)

func select_intervention(intervention_id: String) -> void:
    selected_intervention = intervention_id

func intervention_details(intervention_id: String) -> Dictionary:
    if intervention_id == "protect_workers":
        return {"id": intervention_id, "title": "Protect essential workers", "cost": "−120.000 €", "effect": "+8 staffing · +10 hospital health", "risk": "−6 housing investment", "description": "Fund emergency shifts and transport for hospital staff. The hospital remains open, but housing investment is delayed."}
    return {"id": intervention_id, "title": "Defer response", "cost": "0 €", "effect": "+4 budget", "risk": "−14 staffing · −10 hospital health", "description": "Preserve funds now, but accept reduced coverage and a visible deterioration around the hospital."}

func confirm_intervention() -> void:
    if selected_intervention.is_empty() or not crisis_active:
        return
    var details: Dictionary = intervention_details(selected_intervention)
    state["decision"] = selected_intervention
    state["budget"] = float(state.get("budget", 0.0)) + (-120000.0 if selected_intervention == "protect_workers" else 180000.0)
    state["healthcare_staffing"] = float(state.get("healthcare_staffing", 0.0)) + (0.08 if selected_intervention == "protect_workers" else -0.14)
    state["housing_affordability"] = float(state.get("housing_affordability", 0.0)) + (-0.06 if selected_intervention == "protect_workers" else 0.01)
    var nodes: Dictionary = state.get("map_nodes", {})
    nodes["hospital"] = float(nodes.get("hospital", 0.0)) + (0.10 if selected_intervention == "protect_workers" else -0.10)
    nodes["workers_housing"] = float(nodes.get("workers_housing", 0.0)) + (-0.04 if selected_intervention == "protect_workers" else -0.02)
    state["map_nodes"] = nodes
    state["district_health"] = float(state.get("district_health", 0.0)) + (0.08 if selected_intervention == "protect_workers" else -0.12)
    var chain: Array = state.get("causal_chain", [])
    chain.append("Decision: %s." % str(details.get("title", "")))
    state["causal_chain"] = chain
    var events: Array = state.get("events", [])
    events.append("Month %d: %s" % [int(state.get("month", 0)), str(details.get("title", ""))])
    state["events"] = events
    decision_applied.emit({"id": selected_intervention, "title": details.get("title", ""), "details": details})
    event_received.emit({"month": state.get("month", 0), "text": "Cause recorded: %s. Advance time to observe the consequence." % str(details.get("title", ""))})
    selected_intervention = ""
    crisis_resolved = true
    crisis_active = false
    state_updated.emit(state)

func advance_month() -> void:
    if outcome_emitted:
        return
    if int(state.get("month", 0)) >= MAX_MONTHS:
        finish()
        return
    var month: int = int(state.get("month", 0)) + 1
    state["month"] = month
    state["tourism_pressure"] = min(1.0, float(state.get("tourism_pressure", 0.0)) + 0.025)
    state["housing_affordability"] = max(0.0, float(state.get("housing_affordability", 0.0)) - 0.012)
    state["healthcare_staffing"] = clamp(float(state.get("healthcare_staffing", 0.0)) - 0.008, 0.0, 1.0)
    state["budget"] = float(state.get("budget", 0.0)) + 180000.0 - month * 4000.0
    var health_delta: float = -0.015 if state.get("decision", null) == "defer_response" else 0.005
    state["district_health"] = clamp(float(state.get("district_health", 0.0)) + health_delta, 0.0, 1.0)
    if month == 1:
        crisis_active = true
        crisis_triggered.emit({"title": "Hospital staffing crisis", "location": "Hospital & workers' housing", "text": "The hospital cannot cover all shifts. Protect essential workers or defer the response and preserve funds."})
    if month == 2 and state.get("decision", null) != null:
        var consequence: String = "The hospital kept its shifts, but housing investment slowed." if state.get("decision") == "protect_workers" else "Reduced coverage spreads through the district; residents report longer waits."
        var chain: Array = state.get("causal_chain", [])
        chain.append("Consequence: %s" % consequence)
        state["causal_chain"] = chain
        var events: Array = state.get("events", [])
        events.append("Month %d: %s" % [month, consequence])
        state["events"] = events
        event_received.emit({"month": month, "text": consequence})
    if month >= MAX_MONTHS:
        finish()
    state_updated.emit(state)

func capture_postcard(place: String, caption: String, tag: String) -> void:
    postcards.append({"place": place, "month": int(state.get("month", 0)), "caption": caption, "tag": tag, "decision": state.get("decision", null), "causal_chain": (state.get("causal_chain", []) as Array).duplicate(), "metrics": {"tourism_pressure": float(state.get("tourism_pressure", 0.0)), "housing_affordability": float(state.get("housing_affordability", 0.0)), "healthcare_staffing": float(state.get("healthcare_staffing", 0.0)), "district_health": float(state.get("district_health", 0.0))}})

func finish() -> void:
    if postcards.size() < 2 or int(postcards.back().get("month", -1)) != int(state.get("month", 0)):
        capture_postcard("Historic Core", "After the crisis response", "after")
    var success: bool = float(state.get("district_health", 0.0)) >= 0.52 and float(state.get("healthcare_staffing", 0.0)) >= 0.55
    outcome_emitted = true
    outcome_changed.emit({"success": success, "text": "Partial success: care held, but housing remains under pressure." if success else "Hard lesson: preserving funds accelerated the district's decline."})

func postcard_comparison() -> String:
    if postcards.size() < 2:
        return "Advance time to capture the after postcard."
    var before: Dictionary = postcards[0].get("metrics", {})
    var after: Dictionary = postcards[postcards.size() - 1].get("metrics", {})
    var decision_text: String = "No intervention recorded." if after.get("decision", null) == null else "Decision: %s" % str(after.get("decision", ""))
    return "%s\nBefore → after (month %d → %d)\nHospital health: %.0f%% → %.0f%%\nHousing affordability: %.0f%% → %.0f%%\nDistrict health: %.0f%% → %.0f%%\n\n%s\n\nCausal trace:\n%s" % [str(postcards.back().get("caption", "")), int(postcards[0].get("month", 0)), int(postcards.back().get("month", 0)), float(before.get("healthcare_staffing", 0.0)) * 100.0, float(after.get("healthcare_staffing", 0.0)) * 100.0, float(before.get("housing_affordability", 0.0)) * 100.0, float(after.get("housing_affordability", 0.0)) * 100.0, float(before.get("district_health", 0.0)) * 100.0, float(after.get("district_health", 0.0)) * 100.0, decision_text, "\n".join((after.get("causal_chain", []) as Array))]
