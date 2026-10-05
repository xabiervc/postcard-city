class_name SimulationSession
extends RefCounted

signal state_updated(state: Dictionary)
signal event_received(event: Dictionary)
signal crisis_triggered(crisis: Dictionary)
signal outcome_changed(outcome: Dictionary)

const MAX_MONTHS := 12
var state: Dictionary
var postcards: Array[Dictionary] = []
var selected_intervention := ""
var crisis_resolved := false

func start_demo() -> void:
    state = {"month": 0, "budget": 12000000.0, "tourism_pressure": 0.62, "housing_affordability": 0.54, "healthcare_staffing": 0.71, "project_status": "baseline", "events": ["Initial conditions established"]}
    postcards.clear()
    selected_intervention = ""
    crisis_resolved = false
    capture_postcard("Historic Core", "Before intervention")
    state_updated.emit(state)

func select_intervention(intervention_id: String) -> void:
    selected_intervention = intervention_id

func confirm_intervention() -> void:
    if selected_intervention.is_empty():
        return
    apply_intervention(selected_intervention)
    selected_intervention = ""

func advance_month() -> void:
    if state.month >= MAX_MONTHS:
        finish()
        return
    state.month += 1
    state.tourism_pressure = min(1.0, state.tourism_pressure + 0.025)
    state.housing_affordability = max(0.0, state.housing_affordability - 0.018)
    state.healthcare_staffing = max(0.0, state.healthcare_staffing - 0.012)
    state.budget += 180000.0 - state.month * 4000.0
    var event := {"month": state.month, "text": "Month %d: pressure increased; delayed effects are becoming visible." % state.month}
    state.events.append(event.text)
    event_received.emit(event)
    if state.month == 4 and not crisis_resolved:
        crisis_triggered.emit({"title": "Hospital staffing crisis", "text": "The hospital cannot cover all shifts. Protect essential workers or accept reduced service."})
    if state.month >= MAX_MONTHS:
        finish()
    state_updated.emit(state)

func apply_intervention(intervention_id: String) -> void:
    if intervention_id == "renegotiate":
        state.project_status = "safeguarded_compromise"
        state.tourism_pressure = max(0.0, state.tourism_pressure - 0.08)
        state.events.append("Aurora Leisure renegotiated with safeguards.")
    elif intervention_id == "social_housing":
        state.housing_affordability = min(1.0, state.housing_affordability + 0.12)
        state.budget -= 650000.0
        state.events.append("Social housing construction started.")
    state_updated.emit(state)

func resolve_crisis() -> void:
    crisis_resolved = true
    state.healthcare_staffing = min(1.0, state.healthcare_staffing + 0.08)
    state.budget -= 120000.0
    state.events.append("Essential workers protected; the response had a fiscal cost.")
    state_updated.emit(state)

func finish() -> void:
    capture_postcard("Historic Core", "After the twelve-month slice")
    var success := state.housing_affordability >= 0.45 and state.healthcare_staffing >= 0.55
    outcome_changed.emit({"success": success, "text": "Success: the historic core remains within livability bounds." if success else "Failure: livability fell below the slice threshold."})

func capture_postcard(place: String, caption: String) -> void:
    postcards.append({"place": place, "month": state.get("month", 0), "caption": caption, "metrics": {"tourism_pressure": state.get("tourism_pressure", 0.0), "housing_affordability": state.get("housing_affordability", 0.0), "healthcare_staffing": state.get("healthcare_staffing", 0.0)}})

func postcard_comparison() -> String:
    if postcards.size() < 2:
        return "Advance to month 12 to capture the final postcard."
    var before: Dictionary = postcards[0].metrics
    var after: Dictionary = postcards[postcards.size() - 1].metrics
    return "Before → after\nTourism pressure: %.0f%% → %.0f%%\nHousing affordability: %.0f%% → %.0f%%\nHealthcare staffing: %.0f%% → %.0f%%" % [before.tourism_pressure * 100.0, after.tourism_pressure * 100.0, before.housing_affordability * 100.0, after.housing_affordability * 100.0, before.healthcare_staffing * 100.0, after.healthcare_staffing * 100.0]
