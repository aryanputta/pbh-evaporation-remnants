"""Create a browser-based live toy PBH evaporation simulation."""

from __future__ import annotations

from pathlib import Path


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PBH Evaporation Live Toy Simulation</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #101418; color: #edf2f7; }
    main { max-width: 980px; margin: 0 auto; padding: 24px; }
    canvas { width: 100%; height: 420px; background: #05070a; border: 1px solid #39424e; display: block; }
    .controls { display: grid; grid-template-columns: repeat(3, minmax(160px, 1fr)); gap: 14px; margin: 16px 0; }
    label { display: grid; gap: 6px; font-size: 14px; color: #cbd5e1; }
    input { width: 100%; }
    button { background: #2f81f7; color: white; border: 0; padding: 10px 14px; cursor: pointer; }
    output { color: #ffffff; font-weight: bold; }
  </style>
</head>
<body>
<main>
  <h1>PBH Evaporation Live Toy Simulation</h1>
  <p>This is an analytic Hawking evaporation toy model using dM/dt = -alpha/M^2. It is not a GRChombo or Einstein Toolkit simulation.</p>
  <div class="controls">
    <label>Initial mass log10(g)<input id="mass" type="range" min="7" max="13" step="0.1" value="10"><output id="massOut"></output></label>
    <label>Remnant mass log10(g)<input id="remnant" type="range" min="0" max="9" step="0.1" value="5"><output id="remnantOut"></output></label>
    <label>Speed<input id="speed" type="range" min="0.2" max="5" step="0.1" value="1"><output id="speedOut"></output></label>
  </div>
  <button id="restart">restart</button>
  <canvas id="sim" width="1200" height="520"></canvas>
</main>
<script>
const canvas = document.getElementById("sim");
const ctx = canvas.getContext("2d");
const alpha = Math.pow(5e14, 3) / (3 * 4.35e17);
let start = performance.now();

function values() {
  const m0 = Math.pow(10, Number(document.getElementById("mass").value));
  const rem = Math.pow(10, Number(document.getElementById("remnant").value));
  const speed = Number(document.getElementById("speed").value);
  document.getElementById("massOut").textContent = m0.toExponential(2) + " g";
  document.getElementById("remnantOut").textContent = rem.toExponential(2) + " g";
  document.getElementById("speedOut").textContent = speed.toFixed(1) + "x";
  return {m0, rem: Math.min(rem, 0.9 * m0), speed};
}

function massAt(m0, rem, phase) {
  const lifetime = (Math.pow(m0, 3) - Math.pow(rem, 3)) / (3 * alpha);
  const t = phase * lifetime;
  const remaining = Math.pow(m0, 3) - 3 * alpha * t;
  return Math.cbrt(Math.max(remaining, Math.pow(rem, 3)));
}

function draw() {
  const {m0, rem, speed} = values();
  const elapsed = (performance.now() - start) / 1000;
  const phase = (elapsed * 0.04 * speed) % 1;
  const mass = massAt(m0, rem, phase);
  const radius = 20 + 150 * Math.sqrt(mass / m0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#05070a";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  const gradient = ctx.createRadialGradient(600, 230, radius * 0.7, 600, 230, radius * 2.7);
  gradient.addColorStop(0, "#ffffff");
  gradient.addColorStop(0.08, "#fbbf24");
  gradient.addColorStop(0.35, "#dc2626");
  gradient.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(600, 230, radius * 2.7, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#000000";
  ctx.beginPath();
  ctx.arc(600, 230, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 3;
  ctx.strokeRect(180, 440, 840, 22);
  ctx.fillStyle = "#2f81f7";
  ctx.fillRect(180, 440, 840 * phase, 22);
  ctx.fillStyle = "#edf2f7";
  ctx.font = "24px Arial";
  ctx.fillText("mass = " + mass.toExponential(3) + " g", 40, 54);
  ctx.fillText("relative abundance = " + (mass / m0).toExponential(3), 40, 90);
  ctx.fillText("simulation phase = " + (100 * phase).toFixed(1) + "%", 40, 126);
  requestAnimationFrame(draw);
}

document.getElementById("restart").onclick = () => { start = performance.now(); };
draw();
</script>
</body>
</html>
"""


def main() -> None:
    path = Path("results") / "live_evaporation_simulation.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HTML, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()

