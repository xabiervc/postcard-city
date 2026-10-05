from pathlib import Path

ROOT = Path(__file__).parents[1]
TECH_PATH = ROOT / "docs" / "technology-and-rnd-system.md"
CRISIS_PATH = ROOT / "docs" / "strategic-crisis-catalog.md"


def test_technology_design_covers_contextual_rnd_and_failure():
    text = TECH_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Research and development",
        "no local market",
        "fail technically or institutionally",
        "opportunity cost",
        "Technology trajectories",
    ):
        assert phrase in text


def test_technology_design_covers_leadership_and_lagging_indicators():
    text = TECH_PATH.read_text(encoding="utf-8")
    for phrase in (
        "technology leader",
        "maintenance backlog",
        "talent retention",
        "digital inclusion",
    ):
        assert phrase in text


def test_strategic_catalog_covers_coup_and_nuclear_risks():
    text = CRISIS_PATH.read_text(encoding="utf-8")
    for phrase in (
        "attempted coup",
        "nuclear-plant accident",
        "radiological contamination",
        "continuity of government",
        "evacuation",
    ):
        assert phrase in text


def test_strategic_catalog_is_high_level_and_non_operational():
    text = CRISIS_PATH.read_text(encoding="utf-8")
    for phrase in (
        "not tactical combat",
        "does not provide operational instructions",
        "does not describe weapons",
        "No gore",
    ):
        assert phrase in text
