class_name SimulationSession
extends RefCounted

signal state_updated(state: Dictionary)
signal event_received(event: Dictionary)
signal crisis_triggered(crisis: Dictionary)
signal decision_applied(decision: Dictionary)
signal outcome_changed(outcome: Dictionary)

const MAX_MONTHS := 6
var state: Dictionary
var postcards: Array[Dictionary] = []
var selected_intervention := ""
var crisis_active := false
var crisis_resolved := false
var initial_snapshot: Dictionary = {}

func start_demo() -> void:
    state = {"month": 0, "budget": 12000000.0, "tourism_pressure": 0.62, "housing_affordability": 0.54, "healthcare_staffing": 0.71, "district_health": 0.60, "map_nodes": {"hospital": 0.46, "workers_housing": 0.52, "historic_core": 0.68}, "project_status": "baseline", "events": ["Month 0: the historic core is stable but fragile."], "decision": null, "causal_chain": []}
    postcards.clear()
    selected_intervention = ""
    crisis_active = false
    crisis_resolved = false
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
    var details := intervention_details(selected_intervention)
    state.decision = selected_intervention
    state.budget += -120000.0 if selected_intervention == "protect_workers" else 180000.0
    state.healthcare_staffing += 0.08 if selected_intervention == "protect_workers" else -0.14
    state.housing_affordability += -0.06 if selected_intervention == "protect_workers" else 0.01
    state.map_nodes.hospital += 0.10 if selected_intervention == "protect_workers" else -0.10
    state.map_nodes.workers_housing += -0.04 if selected_intervention == "protect_workers" else -0.02
    state.district_health += 0.08 if selected_intervention == "protect_workers" else -0.12
    state.causal_chain.append("Decision: %s." % details.title)
    state.events.append("Month %d: %s" % [state.month, details.title])
    decision_applied.emit({"id": selected_intervention, "title": details.title, "details": details})
    event_received.emit({"month": state.month, "text": "Cause recorded: %s. Advance time to observe the consequence." % details.title})
    selected_intervention = ""
    crisis_resolved = true
    crisis_active = false
    state_updated.emit(state)

func advance_month() -> void:
    if state.month >= MAX_MONTHS:
        finish()
        return
    state.month += 1
    state.tourism_pressure = min(1.0, state.tourism_pressure + 0.025)
    state.housing_affordability = max(0.0, state.housing_affordability - 0.012)
    state.healthcare_staffing = clamp(state.healthcare_staffing - 0.008, 0.0, 1.0)
    state.budget += 180000.0 - state.month * 4000.0
    state.district_health = clamp(state.district_health - 0.015 if state.decision == "defer_response" else state.district_health + 0.005, 0.0, 1.0)
    if state.month == 1:
        crisis_active = true
        crisis_triggered.emit({"title": "Hospital staffing crisis", "location": "Hospital & workers' housing", "text": "The hospital cannot cover all shifts. Protect essential workers or defer the response and preserve funds."})
    if state.month == 2 and state.decision != null:
        var consequence := "The hospital kept its shifts, but housing investment slowed." if state.decision == "protect_workers" else "Reduced coverage spreads through the district; residents report longer waits."
        state.causal_chain.append("Consequence: %s" % consequence)
        state.events.append("Month %d: %s" % [state.month, consequence])
        event_received.emit({"month": state.month, "text": consequence})
    if state.month >= MAX_MONTHS:
        finish()
    state_updated.emit(state)

func capture_postcard(place: String, caption: String, tag: String) -> void:
    postcards.append({"place": place, "month": state.get("month", 0), "caption": caption, "tag": tag, "decision": state.get("decision", null), "causal_chain": state.get("causal_chain", []).duplicate(), "metrics": {"tourism_pressure": state.get("tourism_pressure", 0.0), "housing_affordability": state.get("housing_affordability", 0.0), "healthcare_staffing": state.get("healthcare_staffing", 0.0), "district_health": state.get("district_health", 0.0)}})

func finish() -> void:
    if postcards.size() < 2 or postcards.back().month != state.month:
        capture_postcard("Historic Core", "After the crisis response", "after")
    var success := state.district_health >= 0.52 and state.healthcare_staffing >= 0.55
    outcome_changed.emit({"success": success, "text": "Partial success: care held, but housing remains under pressure." if success else "Hard lesson: preserving funds accelerated the district's decline."})

func postcard_comparison() -> String:
    if postcards.size() < 2:
        return "Advance time to capture the after postcard."
    var before: Dictionary = postcards[0].metrics
    var after: Dictionary = postcards[postcards.size() - 1].metrics
    var decision_text := "No intervention recorded." if after.decision == null else "Decision: %s" % after.decision
    return "%s\nBefore → after (month %d → %d)\nHospital health: %.0f%% → %.0f%%\nHousing affordability: %.0f%% → %.0f%%\nDistrict health: %.0f%% → %.0f%%\n\n%s\n\nCausal trace:\n%s" % [after.caption, postcards[0].month, postcards.back().month, before.get("healthcare_staffing", 0.0) * 100.0, after.get("healthcare_staffing", 0.0) * 100.0, before.get("housing_affordability", 0.0) * 100.0, after.get("housing_affordability", 0.0) * 100.0, before.get("district_health", 0.0) * 100.0, after.get("district_health", 0.0) * 100.0, decision_text, "\n".join(after.causal_chain)]
