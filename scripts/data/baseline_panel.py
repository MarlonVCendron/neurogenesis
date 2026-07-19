
import matplotlib.pyplot as plt

from utils.data import load_pattern_data
from utils.plot_styles import apply_paper_style

from scripts.data import raster_plot, firing_rate_distribution

apply_paper_style()

RASTER_RUN = 'june_final'
RATE_RUN = 'rate8'


def main():
  rate_data = load_pattern_data(RATE_RUN)
  rate_groups = sorted(list(rate_data.keys()))

  fig = plt.figure(figsize=(7, 11), dpi=300)
  outer = fig.add_gridspec(2, 1, height_ratios=[1.35, 1], hspace=0.22)

  raster_plot.draw(fig, outer[0], f'res/{RASTER_RUN}', label='(a)')
  firing_rate_distribution.draw(fig, outer[1], rate_data, rate_groups, label='(b)')

  fig.savefig('figures/plots/baseline_panel.pdf', format='pdf', bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  main()
