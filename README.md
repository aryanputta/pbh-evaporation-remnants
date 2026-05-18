# PBH Evaporation And Remnant Evolution

This repo models Hawking evaporation for a monochromatic population of small
black holes and compares scenarios with and without a stable remnant mass.

The code tracks mass loss, survival time, and final abundance for simple input
parameters. It is meant as a clear computational starting point, not a complete
particle-physics evaporation code.

## Run

```bash
python evaporation_model.py
python benchmark_evaporation.py
python live_simulation.py
pytest
```

Outputs:

- `results/evaporation_history.csv`
- `results/remnant_comparison.png`
- `results/evaporation_benchmark.csv`
- `results/evaporation_benchmark_compare.png`
- `results/live_evaporation_simulation.html`

## Approximation

The mass-loss law is

```text
dM/dt = -alpha / M^2
```

with `alpha` calibrated so a `5e14 g` black hole lives roughly one age of the
Universe. Greybody factors, changing particle thresholds, and clustering are
not included.

## Live Simulation

`live_simulation.py` writes a browser-based animated toy simulation to
`results/live_evaporation_simulation.html`. Open it locally to adjust initial
mass, remnant mass, and animation speed.

This is an interactive visualization of the analytic model, not a full
numerical-relativity simulation.
