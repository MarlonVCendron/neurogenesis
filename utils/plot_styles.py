cell_colors = {
  "pp": '#4a555e',
  "mgc": '#d73037',
  "igc": "#ff73b4",
  "mc": '#61cd00',
  "hipp": '#ff7b21',
  "bc": '#ffbe0b',
  "pca3": '#2F2FE4',
  "ica3": '#00e1ff',
  "gc": '#c801ff',
  "control": '#120406'
}

alpha = 0.9
linewidth = 4

FIG_WIDTH_IN = 17


def fig_size(width_frac, aspect=1.0):
    w = FIG_WIDTH_IN * width_frac
    return (w, w * aspect)


def apply_paper_style():
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-v0_8-poster')
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "lines.linewidth": linewidth,
        "lines.solid_joinstyle": "round",
        "lines.solid_capstyle": "round",
    })

igc_connectivity_label = 'EC→iGC excitability (% of mGC)'
# igc_connectivity_label = 'iGC afferent input fraction'
# igc_connectivity_label = 'EC→iGC connectivity (% of mGC)'

# From https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
dense_dots = (0, (1, 0.5))