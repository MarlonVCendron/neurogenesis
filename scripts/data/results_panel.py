import matplotlib.pyplot as plt

from utils.data import load_pattern_data
from utils.plot_styles import apply_paper_style

from scripts.data import (
    avg_activity_broken,
    avg_pattern_separation,
    avg_activity_ca3,
    pattern_separation_ca3,
    sparsity,
)

apply_paper_style()


def main():
    data = load_pattern_data('june_final')
    groups = sorted(list(data.keys()))

    fig = plt.figure(figsize=(17, 11), dpi=300)
    outer = fig.add_gridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.16)

    left = outer[0].subgridspec(2, 2, hspace=0.45, wspace=0.40)
    avg_activity_broken.draw(fig, left[0, 0], data, groups, label='(a)')
    avg_pattern_separation.draw(fig, left[0, 1], data, groups, label='(b)')
    avg_activity_ca3.draw(fig, left[1, 0], data, groups, label='(c)')
    pattern_separation_ca3.draw(fig, left[1, 1], data, groups, label='(d)')

    sparsity.draw(fig, outer[1], data, groups, measure='gini', label='(e)')

    # fig.savefig('figures/plots/results_panel.jpg', dpi=300, format='jpg', bbox_inches='tight')
    fig.savefig('figures/plots/results_panel.pdf', format='pdf', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
