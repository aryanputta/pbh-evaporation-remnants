"""Benchmark evaporation output against the analytic M(t)^3 solution."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from evaporation_model import ALPHA_G3_PER_S, lifetime_seconds, mass_at_time


def reference_mass(initial_mass_g: float, time_s: np.ndarray) -> np.ndarray:
    remaining = initial_mass_g**3 - 3.0 * ALPHA_G3_PER_S * time_s
    return np.where(remaining > 0, np.cbrt(remaining), 0.0)


def run_benchmark(initial_mass_g: float = 1e10) -> dict[str, np.ndarray]:
    time = np.linspace(0.0, lifetime_seconds(initial_mass_g), 180)
    model = mass_at_time(initial_mass_g, time)
    reference = reference_mass(initial_mass_g, time)
    abs_error = np.abs(model - reference)
    return {"time_s": time, "model_mass_g": model, "reference_mass_g": reference, "abs_error_g": abs_error}


def write_csv(data: dict[str, np.ndarray], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(data.keys())
        for row in zip(*data.values()):
            writer.writerow([f"{value:.8e}" for value in row])


def make_plot(data: dict[str, np.ndarray], path: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 6.2), sharex=True)
    axes[0].plot(data["time_s"], data["model_mass_g"], label="model")
    axes[0].plot(data["time_s"], data["reference_mass_g"], "--", label="analytic reference")
    axes[0].set_ylabel("Mass [g]")
    axes[0].set_title("Evaporation benchmark comparison")
    axes[0].grid(alpha=0.3)
    axes[0].legend()
    axes[1].plot(data["time_s"], data["abs_error_g"])
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Absolute error [g]")
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    results_dir = Path("results")
    data = run_benchmark()
    write_csv(data, results_dir / "evaporation_benchmark.csv")
    make_plot(data, results_dir / "evaporation_benchmark_compare.png")
    print(f"max_abs_error_g={data['abs_error_g'].max():.6e}")


if __name__ == "__main__":
    main()

