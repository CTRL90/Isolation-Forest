"""
Draws the figures in assets/ (used by the website and the Word report).
Needs matplotlib, which is NOT required to run the website.

    pip install matplotlib
    python tools/make_figures.py
"""
import math
import random
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from iforest_from_scratch import c  # noqa: E402

OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

IVORY = "#F7F4EB"
PALE = "#E9D99B"
GOLD = "#D6B75C"
GRAY = "#77766E"
CHAR = "#292923"
RUST = "#A65A3A"   # muted accent used only to mark the anomaly / threshold
LIGHT = "#EFEADB"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": GRAY,
    "axes.labelcolor": CHAR,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "text.color": CHAR,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# ---------------------------------------------------------------- Figure 1
def isolate(points, target, rng, max_steps=60):
    """Split the box that holds `target` (paper's rule) until target is alone. Returns split lines."""
    pts = points.copy()
    xmin, ymin = points.min(axis=0) - 0.3
    xmax, ymax = points.max(axis=0) + 0.3
    box = [xmin, xmax, ymin, ymax]
    lines = []
    while len(pts) > 1 and len(lines) < max_steps:
        q = rng.randrange(2)
        lo, hi = pts[:, q].min(), pts[:, q].max()
        if lo == hi:
            continue
        p = rng.uniform(lo, hi)
        if q == 0:
            lines.append(((p, p), (box[2], box[3])))
            if target[0] < p:
                box[1] = p
                pts = pts[pts[:, 0] < p]
            else:
                box[0] = p
                pts = pts[pts[:, 0] >= p]
        else:
            lines.append(((box[0], box[1]), (p, p)))
            if target[1] < p:
                box[3] = p
                pts = pts[pts[:, 1] < p]
            else:
                box[2] = p
                pts = pts[pts[:, 1] >= p]
    return lines


def fig_isolation():
    rs = np.random.RandomState(3)
    normal = rs.normal(0, 1, size=(80, 2))
    anomaly = np.array([[3.6, 3.1]])
    data = np.vstack([normal, anomaly])
    xi = normal[np.argmin(np.linalg.norm(normal, axis=1))]   # a point in the dense centre
    xo = anomaly[0]

    # average number of splits over many random runs (shown in the titles)
    def avg_splits(target, runs=300):
        return np.mean([len(isolate(data, target, random.Random(s))) for s in range(runs)])

    avg_i, avg_o = avg_splits(xi), avg_splits(xo)

    # pick one run whose length is close to the average, so the picture is typical
    def typical(target, avg):
        best = None
        for s in range(300):
            ln = isolate(data, target, random.Random(s))
            if best is None or abs(len(ln) - avg) < abs(len(best) - avg):
                best = ln
        return best

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, target, avg, name in [(axes[0], xi, avg_i, "normal point $x_i$"),
                                  (axes[1], xo, avg_o, "anomaly $x_o$")]:
        lines = typical(target, avg)
        for k, (xs, ys) in enumerate(lines):
            ax.plot(xs, ys, color=GOLD, lw=1.4, alpha=0.95, zorder=1)
        ax.scatter(normal[:, 0], normal[:, 1], s=18, color=GRAY, alpha=0.75, zorder=2)
        ax.scatter([xo[0]], [xo[1]], s=40, color=GRAY, zorder=2)
        ax.scatter([target[0]], [target[1]], s=140, facecolor="none", edgecolor=RUST, lw=2.2, zorder=3)
        ax.set_title(f"Isolating a {name}\nthis run: {len(lines)} splits   |   average of 300 runs: {avg:.1f}",
                     fontsize=11, color=CHAR)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(LIGHT)
    fig.suptitle("Random splits needed to isolate one point (random feature, random value between min and max)",
                 fontsize=12, color=CHAR, y=1.02)
    save(fig, "fig_isolation.png")


# ---------------------------------------------------------------- drawing helpers
def box(ax, x, y, w, h, text, fill=IVORY, edge=GOLD, size=10.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fill, ec=edge, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            color=CHAR, fontweight="bold" if bold else "normal", linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, color=GRAY):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=14))


# ---------------------------------------------------------------- Figure 3
def fig_itree():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
    box(ax, 3.4, 3.6, 3.2, 0.75, "Value  <  21,000 ?", fill=PALE, bold=True)
    box(ax, 1.1, 2.2, 3.4, 0.75, "Value  <  104 ?\n{90, 100, 110, 120}", size=10)
    box(ax, 6.6, 2.2, 2.6, 0.75, "Point 5\n(50,000)", fill="#F3E3D8", edge=RUST, bold=True)
    arrow(ax, 4.4, 3.6, 2.8, 2.95); ax.text(3.2, 3.3, "yes", color=GRAY, fontsize=9)
    arrow(ax, 5.6, 3.6, 7.9, 2.95); ax.text(6.9, 3.3, "no", color=GRAY, fontsize=9)
    box(ax, 0.1, 0.7, 2.4, 0.75, "{90, 100}\nmore splits…", size=10)
    box(ax, 3.0, 0.7, 2.4, 0.75, "{110, 120}\nmore splits…", size=10)
    arrow(ax, 2.2, 2.2, 1.3, 1.45); arrow(ax, 3.4, 2.2, 4.2, 1.45)
    ax.text(7.9, 1.75, "isolated after 1 split\npath length h = 1", ha="center", color=RUST, fontsize=10)
    ax.text(2.75, 0.25, "in this tree, each normal point needs 3 splits", ha="center", color=GRAY, fontsize=10)
    save(fig, "fig_itree_example.png")


# ---------------------------------------------------------------- Workflow of Algorithm 1
def fig_workflow():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.2); ax.axis("off")
    top = [("1", "Initialize Forest", "Forest ← { }"),
           ("2", "Set height limit", "l ← ⌈log₂ ψ⌉\n(ψ = 256 → l = 8)"),
           ("3", "Start the loop", "for i ← 1 to t"),
           ("4", "Sub-sampling", "X' ← sample(X, ψ)\nwithout replacement")]
    xs = [0.2, 3.2, 6.2, 9.2]
    for (n, t, d), x in zip(top, xs):
        box(ax, x, 3.0, 2.6, 1.7, "", fill=PALE if n == "4" else IVORY)
        ax.text(x + 0.18, 4.42, n + ".  " + t, fontsize=11, fontweight="bold", color=CHAR, va="center")
        ax.text(x + 1.3, 3.65, d, fontsize=10.5, color=CHAR, ha="center", va="center", linespacing=1.4)
    for x in xs[:-1]:
        arrow(ax, x + 2.6, 3.85, x + 3.2, 3.85)
    bottom = [("5", "Build one iTree", "Tree ← iTree(X', 0, l)\nForest ← Forest ∪ {Tree}", 9.2),
              ("6", "End of iteration", "i < t ?", 5.2),
              ("7", "Return the forest", "return Forest\n(t iTrees)", 1.2)]
    for n, t, d, x in bottom:
        box(ax, x, 0.4, 2.6 if n != "6" else 2.4, 1.7, "", fill=PALE if n == "5" else IVORY)
        ax.text(x + 0.18, 1.82, n + ".  " + t, fontsize=11, fontweight="bold", color=CHAR, va="center")
        ax.text(x + (1.3 if n != "6" else 1.2), 1.05, d, fontsize=10.5, color=CHAR, ha="center", va="center", linespacing=1.4)
    arrow(ax, 10.5, 3.0, 10.5, 2.1)                       # 4 -> 5
    arrow(ax, 9.2, 1.25, 7.6, 1.25)                       # 5 -> 6
    arrow(ax, 5.2, 1.25, 3.8, 1.25)                       # 6 -> 7 (no)
    ax.text(4.5, 1.4, "no (i = t)", fontsize=9.5, color=GRAY, ha="center")
    # yes: back to step 4
    ax.plot([6.4, 6.4, 9.8], [2.1, 2.55, 2.55], color=RUST, lw=1.4)
    arrow(ax, 9.8, 2.55, 9.8, 3.0, color=RUST)
    ax.text(6.55, 2.66, "yes (i < t): i ← i + 1, new sample", fontsize=9.5, color=RUST, ha="left")
    save(fig, "fig_workflow.png")


if __name__ == "__main__":
    fig_isolation()
    fig_itree()
    fig_workflow()
