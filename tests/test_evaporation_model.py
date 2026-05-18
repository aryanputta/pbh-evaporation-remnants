import numpy as np

from evaporation_model import abundance_history, lifetime_seconds, mass_at_time


def test_lifetime_increases_with_mass():
    assert lifetime_seconds(2e10) > lifetime_seconds(1e10)


def test_mass_decreases_without_remnant():
    time = np.linspace(0.0, lifetime_seconds(1e10), 50)
    mass = mass_at_time(1e10, time)
    assert mass[0] > mass[-1]
    assert mass[-1] == 0.0


def test_remnant_survives():
    history = abundance_history(1e10, 1.0, remnant_mass_g=1e5)
    assert history["mass_g"][-1] >= 1e5

