import numpy as np
import matplotlib.pyplot as plt

tau = 20.0  # ms
A = 70.0

delta_t = np.linspace(-100, 100, 400)
delta_w = A * np.exp(-np.abs(delta_t) / tau)

fig, ax = plt.subplots(figsize=(10, 7))
ax.plot(delta_t, delta_w, color='black', linewidth=3)

# ax.set_title("STDP", fontsize=24, weight='bold')
ax.set_ylabel("Mudança no peso sináptico (%)", fontsize=22)
ax.set_xlabel(r"$\Delta t = t_{post} - t_{pre}$ (ms)", fontsize=22)

ax.set_xlim(-100, 100)
ax.set_ylim(0, 100)
ax.tick_params(axis='both', which='major', labelsize=18)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'figures/symmetric_stdp.pdf')
plt.show()
