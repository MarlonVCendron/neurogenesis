from brian2 import *
from models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_pca3,
    create_ica3,
)
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from scripts.helpers.neuron_type_mapping import neuron_type_mapping

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "lines.linewidth": 1.5,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
  })

seed(1)

defaultclock.dt = 0.1 * ms

neuron_currents = {
    'mgc': 600 * pA,
    'igc': 100 * pA,
    'bc': 200 * pA,
    'mc': 200 * pA,
    'hipp': 100 * pA,
    'pca3': 500 * pA,
    'ica3': 400 * pA,
}

def main():
  start_scope()

  mgc  = create_mgc(N=1)
  igc  = create_igc(N=1)
  bc   = create_bc(N=1)
  mc   = create_mc(N=1)
  hipp = create_hipp(N=1)
  pca3 = create_pca3(N=1)
  ica3 = create_ica3(N=1)

  neurons = [mgc, igc, bc, mc, hipp, pca3, ica3]
  neuron_map = {n.name: n for n in neurons}

  state_monitors = [StateMonitor(neuron, ['Vm'], record=True) for neuron in neurons]

  net = Network(collect())
  net.add(neurons)
  net.add(state_monitors)

  net.run(100 * ms)

  for name, currents in neuron_currents.items():
      neuron_map[name].I_ext = currents
  net.run(500 * ms)

  for neuron in neurons:
      neuron.I_ext = 0.0 * pA
  net.run(100 * ms)
  
  fig = plt.figure(figsize=(12, 8))
  gs_main = fig.add_gridspec(2, 4, wspace=0.1, hspace=0.1)
  
  # Invert the neuron_type_mapping
  name_to_display = {v: k for k, v in neuron_type_mapping.items()}

  all_vms = np.hstack([sm.Vm[0]/mV for sm in state_monitors])
  vm_min, vm_max = np.min(all_vms), np.max(all_vms)
  v_range = vm_max - vm_min
  global_v_lim = (vm_min - 0.02 * v_range, vm_max + 0.02 * v_range)

  t_max = state_monitors[0].t[-1]/ms

  for i, (neuron, state_monitor) in enumerate(zip(neurons, state_monitors)):
    if i < 4:  # Top row
        row, col = 0, i
    else:  # Bottom row, skipping first column
        row, col = 1, (i - 4) + 1
        
    ax_v = fig.add_subplot(gs_main[row, col])
    # ax_v.axis('off')
    ax_v.spines['right'].set_visible(False)
    ax_v.spines['top'].set_visible(False)
    plt.xticks([], [])
    plt.yticks([], [])


    ax_v.plot(state_monitor.t / ms, state_monitor.Vm[0] / mV, color="black")
    
    current_val_pA = neuron_currents[neuron.name] / pA
    display_name = name_to_display.get(neuron.name, neuron.name)
    text = f'{display_name} ({current_val_pA:.0f} pA)'
    
    try:
        img_path = f"thesis/figuras/neurônios/{neuron.name}.png"
        img = plt.imread(img_path)
        imagebox = OffsetImage(img, zoom=0.04, interpolation='bicubic')
        ab = AnnotationBbox(imagebox, (0.1, 1.025), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0.5))
        ax_v.add_artist(ab)
        ax_v.set_title(text, fontsize=12, y=0.98, x=0.6)
    except FileNotFoundError:
        ax_v.set_title(text, fontsize=12)
        pass

    # ax_v.text(0.95, 0.95, f"{current_val_pA:.0f} pA", transform=ax_v.transAxes, fontsize=12, va='top', ha='right')
    
    ax_v.set_xlim(0, t_max)
    ax_v.set_ylim(global_v_lim)

  # --- Add Scale Box ---
  scale_ax = fig.add_subplot(gs_main[1, 0])
  scale_ax.axis('off')
  scale_ax.set_xlim(0, t_max)
  scale_ax.set_ylim(global_v_lim)

  h_size_ms = 200
  v_size_mv = 20
  x0 = (t_max - h_size_ms) / 2
  y0 = vm_min + (v_range - v_size_mv) / 2

  scale_ax.plot([x0, x0 + h_size_ms], [y0, y0], color='black', linewidth=2)
  scale_ax.plot([x0, x0], [y0, y0 + v_size_mv], color='black', linewidth=2)

  font_props = {'family': 'serif', 'size': 12}
  scale_ax.text(x0 + h_size_ms / 2, y0 - v_range * 0.08, f'{h_size_ms} ms', ha='center', va='top', fontdict=font_props)
  scale_ax.text(x0 - t_max * 0.08, y0 + v_size_mv / 2, f'{v_size_mv} mV', ha='right', va='center', rotation='vertical', fontdict=font_props)

  plt.tight_layout()
  plt.subplots_adjust(wspace=0.1, hspace=0.2)
  
  plt.savefig('figures/spike_traces.png', bbox_inches='tight', pad_inches=0.05)
  plt.savefig('figures/spike_traces.pdf', bbox_inches='tight', pad_inches=0.05)
#   plt.show()


if __name__ == '__main__':
  main()

