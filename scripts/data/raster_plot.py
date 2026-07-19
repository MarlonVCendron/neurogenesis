from utils.plot_styles import cell_colors, apply_paper_style, panel_label
import h5py
from glob import glob
import matplotlib.pyplot as plt
import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

RUN_NAME = 'june_final'   # saved-data run to load from res/

MODEL = 'neurogenesis_0.5'
RUN = 0
PATTERN = 0

TIME_START_MS = 300
TIME_END_MS = 1300
XTICK_STEP_MS = 250

NEURONS = ['pp', 'mgc', 'igc', 'pca3']

CELL_TYPES = [
    ('pp',  'EC'),
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('mc',   'MC'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
]

apply_paper_style()


def resolve_target(base):
  pattern = re.compile(r'^(?P<model>.+)_ca3_trial_(?P<trial>\d+)_pattern_(?P<pattern>\d+)$')
  entries = []
  for path in sorted(glob(f'{base}/*')):
    if not os.path.isdir(path):
      continue
    m = pattern.match(os.path.basename(path))
    if m:
      entries.append((m.group('model'), int(m.group('trial')), int(m.group('pattern'))))

  if not entries:
    sys.exit(f'No simulation directories found under {base}/')

  model = MODEL if MODEL is not None else sorted({e[0] for e in entries})[0]
  entries = [e for e in entries if e[0] == model]

  trial = RUN if RUN is not None else sorted({e[1] for e in entries})[0]
  entries = [e for e in entries if e[1] == trial]

  pat = PATTERN if PATTERN is not None else sorted({e[2] for e in entries})[0]

  dir_name = f'{model}_ca3_trial_{trial}_pattern_{pat}'
  file_path = f'{base}/{dir_name}/patterns.h5'
  if not os.path.exists(file_path):
    sys.exit(f'No patterns.h5 found for {dir_name} under {base}/')

  return model, trial, pat, file_path


def load_data(file_path):
  spike_times = {}
  n_neurons = {}

  with h5py.File(file_path, 'r') as f:
    if 'spike_times' not in f:
      sys.exit(f'File {file_path} has no spike_times group.')
    for ct in f['spike_times'].keys():
      t = np.array(f['spike_times'][ct]['times_ms'], dtype=np.float64)
      i = np.array(f['spike_times'][ct]['indices'],  dtype=np.int32)
      spike_times[ct] = (t, i)
      if 'rates' in f and ct in f['rates']:
        n_neurons[ct] = len(f['rates'][ct])

  return spike_times, n_neurons


def draw(fig, spec, base, label=None):
  model, trial, pat, file_path = resolve_target(base)
  spike_times, n_neurons = load_data(file_path)

  wanted = NEURONS if NEURONS is not None else [ct for ct, _ in CELL_TYPES]
  active = [
      (ct, lbl) for ct, lbl in CELL_TYPES
      if ct in wanted and ct in spike_times and n_neurons.get(ct, 0) > 0
  ]

  n_panels = len(active)
  inner = spec.subgridspec(n_panels, 1, hspace=0.15)
  axes = [fig.add_subplot(inner[0])]
  for i in range(1, n_panels):
    axes.append(fig.add_subplot(inner[i], sharex=axes[0]))

  xticks = np.arange(TIME_START_MS, TIME_END_MS + 1, XTICK_STEP_MS)

  for ax, (ct, lbl) in zip(axes, active):
    color = cell_colors.get(ct, '#333333')
    n_neur = n_neurons.get(ct, 1)

    times, indices = spike_times[ct]
    mask = (times >= TIME_START_MS) & (times <= TIME_END_MS)
    ax.plot(times[mask], indices[mask], 'ok', markersize=2)

    ax.set_ylim(0, n_neur)
    ax.set_yticks([0, n_neur])

    ax.set_ylabel(lbl, color=color, fontsize=16, fontweight='bold', rotation=0, ha='left', va='top')
    ax.yaxis.set_label_coords(0.04, 1)

    ax.set_xticks(xticks)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', length=4)

  for ax in axes[:-1]:
    ax.tick_params(axis='x', labelbottom=False)

  axes[-1].set_xlabel('Time (ms)')
  axes[-1].set_xlim(TIME_START_MS, TIME_END_MS)

  # shared y-label across the stacked panels
  host = fig.add_subplot(spec, frameon=False)
  host.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  host.set_xticks([])
  host.set_yticks([])
  host.set_ylabel('Neuron index', labelpad=42)

  if label:
    panel_label(axes[0], label)

  return axes


def main(base):
  fig = plt.figure(figsize=(6, 1.8 * len(NEURONS)), dpi=300)
  model, trial, pat, _ = resolve_target(base)
  draw(fig, fig.add_gridspec(1, 1)[0], base)

  output_path = f'figures/plots/simulation/{RUN_NAME}/spikes_{model}_trial{trial}_pattern{pat}.jpg'
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  fig.savefig(output_path, dpi=300, bbox_inches='tight', format='jpg')
  plt.close(fig)
  print(f'Saved: {output_path}')


if __name__ == '__main__':
  main(f'res/{RUN_NAME}')
