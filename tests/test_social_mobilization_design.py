from pathlib import Path

ROOT = Path(__file__).parents[1]
DOC_PATH = ROOT / "docs" / "social-mobilization-system.md"


def test_social_design_covers_strikes_protests_and_collective_action():
    text = DOC_PATH.read_text(encoding="utf-8")
    for phrase in (
        "labour strikes",
        "neighbourhood demonstrations",
        "consumer boycotts",
        "tenant campaigns",
        "unions",
        "opposition alliances",
    ):
        assert phrase in text


def test_social_design_covers_negotiation_and_consequences():
    text = DOC_PATH.read_text(encoding="utf-8")
    for phrase in (
        "negotiate",
        "citizens’ assemblies",
        "compensation",
        "lost workdays",
        "essential-service availability",
        "polarisation",
        "institutional reforms",
    ):
        assert phrase in text


def test_social_design_has_complexity_levels_and_rights_constraints():
    text = DOC_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Relaxed",
        "Standard",
        "Advanced",
        "Expert",
        "Peaceful protest is a legitimate civic activity",
        "due process",
        "proportionality",
    ):
        assert phrase in text


def test_social_design_does_not_teach_violent_wrongdoing():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "never taught" in text
    assert "indiscriminate repression" in text
