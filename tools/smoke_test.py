from postcard_city.model import Decision
from postcard_city.simulation import Simulation


if __name__ == "__main__":
    simulation = Simulation.from_default_slice()
    simulation.start_social_housing(100)
    simulation.apply_land_decision("parcel_b", "lease_ground")
    simulation.apply_decision(Decision("aurora_leisure_proposal", "renegotiate"))
    simulation.run(36)
    assert simulation.state.metrics["permanent_population"] > 0
    assert simulation.state.social_housing.cumulative_arrears >= 0
    print("Postcard City integration smoke test passed")
