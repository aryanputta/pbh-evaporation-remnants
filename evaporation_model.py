"""Toy Hawking evaporation model with optional stable remnants."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

AGE_UNIVERSE_S = 4.35e17
CALIBRATION_MASS_G = 5.0e14
ALPHA_G3_PER_S = CALIBRATION_MASS_G**3 / (3.0 * AGE_UNIVERSE_S)


def lifetime_seconds(initial_mass_g: float, remnant_mass_g: float = 0.0) -> float:
    if initial_mass_g <= 0:
        raise ValueError("initial_mass_g must be positive")
    if remnant_mass_g < 0 or remnant_mass_g >= initial_mass_g:
        raise ValueError("remnant_mass_g must satisfy 0 <= remnant < initial")
    return (initial_mass_g**3 - remnant_mass_g**3) / (3.0 * ALPHA_G3_PER_S)


def mass_at_time(initial_mass_g: float, time_s: np.ndarray, remnant_mass_g: float = 0.0) -> np.ndarray:
    if initial_mass_g <= 0:
        raise ValueError("initial_mass_g must be positive")
    time_s = np.asarray(time_s)
    remaining_cubed = initial_mass_g**3 - 3.0 * ALPHA_G3_PER_S * time_s
    floor = remnant_mass_g**3 if remnant_mass_g > 0 else 0.0
    mass_cubed = np.maximum(remaining_cubed, floor)
    mass = np.cbrt(mass_cubed)
    if remnant_mass_g == 0:
        mass = np.where(remaining_cubed > 0, mass, 0.0)
    return mass


def abundance_history(
    initial_mass_g: float,
    initial_fraction: float,
    remnant_mass_g: float = 0.0,
    n_steps: int = 240,
) -> dict[str, np.ndarray]:
    if initial_fraction < 0:
        raise ValueError("initial_fraction must be non-negative")
    end_time = min(AGE_UNIVERSE_S, lifetime_seconds(initial_mass_g, remnant_mass_g) * 1.2)
    time = np.linspace(0.0, end_time, n_steps)
    mass = mass_at_time(initial_mass_g, time, remnant_mass_g)
    fraction = initial_fraction * mass / initial_mass_g
    return {"time_s": time, "mass_g": mass, "relative_fraction": fraction}


def write_csv(history: dict[str, np.ndarray], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(history.keys())
        for row in zip(*history.values()):
            writer.writerow([f"{value:.8e}" for value in row])


def make_plot(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for remnant in [0.0, 1e5, 1e9]:
        history = abundance_history(1e10, 1.0, remnant)
        label = "no remnant" if remnant == 0 else f"remnant={remnant:.0e} g"
        ax.plot(history["time_s"], history["relative_fraction"], label=label)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Relative PBH mass abundance")
    ax.set_title("Toy evaporation with optional remnants")
    ax.set_yscale("log")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    results_dir = Path("results")
    history = abundance_history(1e10, 1.0, remnant_mass_g=1e5)
    write_csv(history, results_dir / "evaporation_history.csv")
    make_plot(results_dir / "remnant_comparison.png")
    print(f"lifetime_no_remnant_s={lifetime_seconds(1e10):.6e}")
    print(f"final_relative_fraction={history['relative_fraction'][-1]:.6e}")


if __name__ == "__main__":
    main()

