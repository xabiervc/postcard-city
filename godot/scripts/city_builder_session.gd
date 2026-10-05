class_name CityBuilderSession
extends RefCounted

signal state_updated(state: Dictionary)
signal event_received(event: Dictionary)
signal crisis_triggered(crisis: Dictionary)
signal finished(summary: Dictionary)

const MAX_MONTHS: int = 5
var state: Dictionary = {}
var seed_value: int = 42
var finished_emitted: bool = false

func start_demo() -> void:
    finished_emitted = false
    state = {"month": 0, "budget": 12000000.0, "population": 18400, "population_change": 0, "tourism_attractiveness": 0.58, "housing_capacity": 19200, "housing_affordability": 0.54, "healthcare_capacity": 0.62, "commercial_activity": 0.46, "district_health": 0.60, "selected_plot": "", "buildings": [{"plot": "0_0", "type": "heritage"}, {"plot": "3_0", "type": "hospital_upgrade"}, {"plot": "1_3", "type": "social_housing"}, {"plot": "3_3", "type": "commercial_block"}], "events": ["Month 0: the old town is lively, but housing capacity is nearly full."]}
    state_updated.emit(state)

func select_plot(plot_id: String) -> void:
    state["selected_plot"] = plot_id
    state_updated.emit(state)

func building_details(building_id: String) -> Dictionary:
    match building_id:
        "social_housing":
            return {"id": building_id, "name": "Social housing", "category": "Residential", "cost": 900000.0, "capacity": 900, "housing": 0.10, "health": 0.08, "description": "Adds homes for residents and essential workers."}
        "hospital_upgrade":
            return {"id": building_id, "name": "Hospital upgrade", "category": "Services", "cost": 1200000.0, "capacity": 0, "healthcare": 0.18, "health": 0.12, "description": "Improves care capacity and district resilience."}
        "commercial_block":
            return {"id": building_id, "name": "Commercial block", "category": "Commerce", "cost": 650000.0, "capacity": 0, "tourism": 0.12, "commerce": 0.16, "health": -0.04, "description": "Raises activity and attractiveness, but increases housing pressure."}
    return {}

func build(building_id: String, plot_id: String) -> bool:
    var details: Dictionary = building_details(building_id)
    if details.is_empty():
        return false
    if float(state.get("budget", 0.0)) < float(details.get("cost", 0.0)):
        event_received.emit({"text": "Construction blocked: insufficient budget."})
        return false
    var buildings: Array = state.get("buildings", [])
    for existing: Dictionary in buildings:
        if str(existing.get("plot", "")) == plot_id:
            event_received.emit({"text": "Construction blocked: this plot is already occupied."})
            return false
    state["budget"] = float(state.get("budget", 0.0)) - float(details.get("cost", 0.0))
    buildings.append({"plot": plot_id, "type": building_id})
    state["buildings"] = buildings
    state["housing_capacity"] = int(state.get("housing_capacity", 0)) + int(details.get("capacity", 0))
    state["housing_affordability"] = clamp(float(state.get("housing_affordability", 0.0)) + float(details.get("housing", 0.0)), 0.0, 1.0)
    state["healthcare_capacity"] = clamp(float(state.get("healthcare_capacity", 0.0)) + float(details.get("healthcare", 0.0)), 0.0, 1.0)
    state["tourism_attractiveness"] = clamp(float(state.get("tourism_attractiveness", 0.0)) + float(details.get("tourism", 0.0)), 0.0, 1.0)
    state["commercial_activity"] = clamp(float(state.get("commercial_activity", 0.0)) + float(details.get("commerce", 0.0)), 0.0, 1.0)
    state["events"].append("Month %d: %s built on plot %s." % [int(state.get("month", 0)), str(details.get("name", building_id)), plot_id])
    event_received.emit({"text": "Construction complete: %s. The city has changed." % str(details.get("name", building_id))})
    state_updated.emit(state)
    return true

func advance_month() -> void:
    var month: int = int(state.get("month", 0))
    if month >= MAX_MONTHS:
        return
    month += 1
    state["month"] = month
    var capacity_gap: int = int(state.get("housing_capacity", 0)) - int(state.get("population", 0))
    var migration: int = 0
    if capacity_gap < 0 or float(state.get("housing_affordability", 0.0)) < 0.30:
        migration = -min(420, abs(capacity_gap) / 4 + 80)
    elif float(state.get("housing_affordability", 0.0)) > 0.50:
        migration = min(260, 90 + int(float(state.get("tourism_attractiveness", 0.0)) * 120.0))
    state["population_change"] = migration
    state["population"] = max(0, int(state.get("population", 0)) + migration)
    state["tourism_attractiveness"] = clamp(float(state.get("tourism_attractiveness", 0.0)) + 0.012, 0.0, 1.0)
    state["housing_affordability"] = clamp(float(state.get("housing_affordability", 0.0)) - (0.018 if migration > 0 else 0.008), 0.0, 1.0)
    state["budget"] = float(state.get("budget", 0.0)) + 220000.0 + float(state.get("commercial_activity", 0.0)) * 90000.0
    var migration_text: String = "%d residents arrived." % migration if migration > 0 else "%d residents left the city." % abs(migration) if migration < 0 else "Population held steady."
    state["events"].append("Month %d: %s" % [month, migration_text])
    event_received.emit({"text": migration_text})
    if month == 3:
        event_received.emit({"text": "Tourist footfall is increasing around the old town."})
    if month == 4 and float(state.get("healthcare_capacity", 0.0)) < 0.70:
        crisis_triggered.emit({"title": "Hospital staffing pressure", "text": "Population and visitor pressure are stretching the hospital.", "zone": "hospital"})
    if month >= MAX_MONTHS and not finished_emitted:
        finished_emitted = true
        finished.emit({"month": month, "population": state.get("population", 0), "population_change": state.get("population_change", 0), "buildings": (state.get("buildings", []) as Array).size(), "budget": state.get("budget", 0.0)})
    state_updated.emit(state)
