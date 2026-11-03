"""Mass and combustion-energy estimation for the 42-class waste detector.

Caloric values (MJ/kg, LHV as-received) and effective densities (kg/m3)
are literature-typical figures from municipal solid-waste characterization
(e.g., Tchobanoglous et al., Integrated Solid Waste Management; Phyllis2).
Incombustibles (glass, metals, ceramics) have LHV 0.
Swap data/caloric.csv for a local waste characterization when you have one.
"""
import csv
from pathlib import Path

DATA = Path(__file__).parent / "data" / "caloric.csv"
PX_PER_M = 100  # ponytail: fixed px->m scale, no depth model; calibrate for your camera height

_rows = {}
with DATA.open() as f:
    for row in csv.DictReader(f):
        _rows[int(row["class_id"])] = row


def estimate(cls_id, w_px, h_px, px_per_m=PX_PER_M):
    """Return (mass_kg, energy_mj) for a detection box.

    Volume = w x h x min(w, h), assumed solid - hollow objects overshoot.
    ponytail: no depth/hollowness model; the per-camera scale factor is the knob.
    """
    r = _rows[cls_id]
    w, h = w_px / px_per_m, h_px / px_per_m
    mass = w * h * min(w, h) * float(r["density_kg_m3"])
    return mass, mass * float(r["lhv_mj_kg"])


if __name__ == "__main__":
    assert len(_rows) == 42
    mass, mj = estimate(24, 100, 200)  # plastic bottle, 100 px/m: 1x2x1 m
    assert abs(mass - 160.0) < 1e-6 and abs(mj - 160.0 * 26) < 1e-6
    print("ok")
