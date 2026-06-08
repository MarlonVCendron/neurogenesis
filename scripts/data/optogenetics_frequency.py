import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import welch
from scipy.ndimage import gaussian_filter1d
import h5py
from utils.plot_styles import cell_colors

NEG = False
ALL_LEVELS = False

RUN_NAME = 'FINAL_opto_june_positive'

ONSET_TIME_MS = 400
DURATION_MS   = 30.0 if NEG else 5.0
BREAK_TIME_MS = 300.0

ANALYSIS_START_MS = DURATION_MS
ANALYSIS_END_MS   = 200.0

BIN_SIZE_MS  = 1.0
ENVELOPE_MS  = 8.0
BAND_LO_HZ   = 20.0
BAND_HI_HZ   = 200.0

CELL_TYPES = [
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('mc',   'MC'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
]

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
})


def load_data(group_file_path):
    files = sorted(glob(f'{group_file_path}*/**/*.h5', recursive=True))
    if not files:
        sys.exit(f'No .h5 files found under {group_file_path}/')

    spike_times = {}
    n_neurons   = {}

    for fpath in files:
        with h5py.File(fpath, 'r') as f:
            for neuron in f['spike_times'].keys():
                times = np.array(f['spike_times'][neuron]['times_ms'], dtype=np.float64)
                spike_times.setdefault(neuron, []).append(times)
                n_neurons[neuron] = max(len(f['rates'][neuron]), n_neurons.get(neuron, 0))

    return spike_times, n_neurons


def population_rate(trials, n_neurons, onset_abs):
    t_start = onset_abs + ANALYSIS_START_MS
    t_end   = onset_abs + ANALYSIS_END_MS
    bins    = np.arange(t_start, t_end + BIN_SIZE_MS, BIN_SIZE_MS)

    counts = np.zeros(len(bins) - 1)
    for times in trials:
        counts += np.histogram(times, bins=bins)[0]

    scale = n_neurons * len(trials) * (BIN_SIZE_MS / 1000.0)
    rate  = counts / scale
    t     = (bins[:-1] + bins[1:]) / 2.0 - onset_abs
    return t, rate


def power_spectrum(rate):
    envelope = gaussian_filter1d(rate, sigma=ENVELOPE_MS / BIN_SIZE_MS)
    osc      = rate - envelope

    fs      = 1000.0 / BIN_SIZE_MS
    nperseg = min(len(osc), 256)
    freqs, pxx = welch(osc, fs=fs, nperseg=nperseg, detrend='constant')
    return freqs, pxx


def band_metrics(f_band, p_band):
    if not p_band.size or p_band.max() <= 0:
        return float('nan'), float('nan'), float('nan')
    i_peak     = int(np.argmax(p_band))
    peak_freq  = float(f_band[i_peak])
    peak_power = float(p_band[i_peak])
    median     = float(np.median(p_band))
    ratio      = peak_power / median if median > 0 else float('nan')
    return peak_freq, peak_power, ratio


def main(group_file_path, neurogenesis_level):
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS

    spike_times, n_neurons = load_data(group_file_path)
    active = [(n, lbl) for n, lbl in CELL_TYPES if n in spike_times]

    n_panels = len(active)
    fig, axes = plt.subplots(
        n_panels, 2,
        figsize=(10, 1.5 * n_panels),
        dpi=300,
    )
    if n_panels == 1:
        axes = axes[np.newaxis, :]

    panels  = []
    metrics = []
    for neuron, label in active:
        n_neur = n_neurons.get(neuron, 1)
        t, rate = population_rate(spike_times[neuron], n_neur, onset_abs)

        freqs, pxx = power_spectrum(rate)
        band = (freqs >= BAND_LO_HZ) & (freqs <= BAND_HI_HZ)
        f_band, p_band = freqs[band], pxx[band]

        peak_freq, peak_power, ratio = band_metrics(f_band, p_band)
        metrics.append((label, peak_freq, peak_power, ratio))
        panels.append((neuron, label, t, rate, f_band, p_band, peak_freq))

    psd_ymax = max((p[5].max() for p in panels if p[5].size), default=1.0) * 1.05

    for (ax_rate, ax_psd), (neuron, label, t, rate, f_band, p_band, peak_freq) in zip(axes, panels):
        color = cell_colors.get(neuron, '#333333')

        ax_rate.plot(t, rate, color=color, lw=1.2)
        ax_rate.set_ylabel(label, color=color, fontsize=14, fontweight='bold',
                           rotation=0, ha='right', va='center')

        ax_psd.plot(f_band, p_band, color=color, lw=1.2)
        if not np.isnan(peak_freq):
            ax_psd.axvline(peak_freq, color='black', ls='--', lw=0.8)
            ax_psd.text(0.97, 0.9, f'{peak_freq:.0f} Hz', transform=ax_psd.transAxes,
                        ha='right', va='top', fontsize=11)
        ax_psd.set_xlim(BAND_LO_HZ, BAND_HI_HZ)
        ax_psd.set_ylim(0, psd_ymax)

        for ax in (ax_rate, ax_psd):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', labelsize=9)

    axes[0, 0].set_title('Population rate', fontsize=13)
    axes[0, 1].set_title('Power spectrum', fontsize=13)
    axes[-1, 0].set_xlabel('Time w.r.t. onset (ms)')
    axes[-1, 1].set_xlabel('Frequency (Hz)')

    plt.tight_layout()

    sign = 'neg' if NEG else 'pos'
    output_path = f'figures/plots/optogenetics/frequency_{sign}_{neurogenesis_level}.jpg'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches='tight', format='jpg')
    plt.close()
    print(f'Saved: {output_path}')

    print_metrics(metrics)


def print_metrics(metrics):
    print(f'{"pop":>5}  {"freq (Hz)":>9}  {"peak power":>10}  {"peak/median":>11}')
    for label, peak_freq, peak_power, ratio in metrics:
        print(f'{label:>5}  {peak_freq:>9.1f}  {peak_power:>10.4g}  {ratio:>11.2f}')


if __name__ == '__main__':
    base  = f'res/{RUN_NAME}'
    files = sorted(glob(f'{base}/*'))

    if ALL_LEVELS:
        groups_file_paths = {base}
    else:
        groups_file_paths = {file.split('_ca3')[0] for file in files}

    pattern = re.compile(r".*(\d.\d)")
    for group_file_path in sorted(groups_file_paths):
        level = 'all' if ALL_LEVELS else pattern.search(group_file_path).group(1)
        main(group_file_path, level)
