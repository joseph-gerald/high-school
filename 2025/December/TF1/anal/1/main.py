from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).with_name("data.csv")
PLOT_FILE = Path(__file__).with_name("distance_plot.png")


def _parse_distance(raw_value: str) -> float:
	"""Extract the numeric part of the measurement and convert decimal commas."""
	match = re.search(r"-?\d+(?:,\d+)?", raw_value)
	if not match:
		raise ValueError(f"Could not parse distance from '{raw_value}'")
	return float(match.group(0).replace(",", "."))


def load_measurements(csv_path: Path = DATA_FILE) -> Tuple[List[float], List[float]]:
	if not csv_path.exists():
		raise FileNotFoundError(f"Data file not found: {csv_path}")

	times: List[float] = []
	distances: List[float] = []

	with csv_path.open("r", encoding="utf-8", newline="") as handle:
		reader = csv.DictReader(handle, delimiter="\t")
		for row in reader:
			times.append(float(row["Tid (s)"]))
			distances.append(_parse_distance(row["Avstand (cm)"]))

	return times, distances


def plot_measurements(
	times: List[float],
	distances: List[float],
	output: Path | None = PLOT_FILE,
	show_plot: bool = True,
) -> None:
	plt.figure(figsize=(10, 5))
	plt.plot(times, distances, marker="o", linewidth=1, markersize=3)
	plt.title("Avstand over tid")
	plt.xlabel("Tid (s)")
	plt.ylabel("Avstand (cm)")
	plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
	plt.tight_layout()
	if output:
		plt.savefig(output, dpi=200)
	if show_plot:
		plt.show()
	plt.close()


if __name__ == "__main__":
	time_values, distance_values = load_measurements()
	plot_measurements(time_values, distance_values)
	if PLOT_FILE.exists():
		print(f"Plot saved to {PLOT_FILE}")
