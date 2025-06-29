import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from concurrent.futures import ProcessPoolExecutor
from collections import deque
import os

# --- Constants ---
ION_CONFIG = {
    # 'Na+': {'radius': 0.15, 'color': 'red', 'charge': 1},
    # 'K+': {'radius': 0.18, 'color': 'blue', 'charge': 1},
    # 'Cl-': {'radius': 0.16, 'color': 'green', 'charge': -1},
    # 'A-': {'radius': 0.24, 'color': 'purple', 'charge': -10, 'impermeable': True}
    'Na+': {'radius': 0.19, 'color': 'red', 'charge': 2},
    'K+': {'radius': 0.22, 'color': 'blue', 'charge': 2},
    'Cl-': {'radius': 0.2, 'color': 'green', 'charge': -2},
    'A-': {'radius': 0.29, 'color': 'purple', 'charge': -10, 'impermeable': True}
}

# Create a custom colormap for potential visualization
potential_cmap = LinearSegmentedColormap.from_list('potential', ['blue', 'white', 'red'])

# This function must be at the top level to be pickleable for multiprocessing
def update_chunk_task(args):
    """Handles all physics for a CHUNK of ions."""
    chunk_of_ions, dt, bounds, membrane_x, membrane_active, permeability, \
    potential_diff, chemical_force_strength, diffusion_speed, electrical_force_strength, \
    counts_by_type, pumps = args

    x_min, x_max, y_min, y_max = bounds
    crossings = []
    
    for ion in chunk_of_ions:
        # 1. Diffusion (random walk)
        ion.vel += (np.random.rand(2) - 0.5) * diffusion_speed * dt
        
        # 2. Electrical force (Corrected)
        if membrane_active:
            # Force is proportional to q * E, and E is proportional to -dV/dx.
            # dV is proportional to (charge_right - charge_left) = -potential_diff.
            # So F is proportional to q * -(-potential_diff) = q * potential_diff.
            electrical_force = potential_diff * ion.charge * electrical_force_strength
            ion.vel[0] += electrical_force * dt

        # 3. Chemical gradient force (Corrected)
        if membrane_active and ion.type in counts_by_type:
            left_count = counts_by_type[ion.type]['left']
            right_count = counts_by_type[ion.type]['right']
            conc_diff = left_count - right_count
            # Force is proportional to -dC/dx, which is proportional to C_left - C_right.
            chemical_force = np.sign(conc_diff) * chemical_force_strength
            ion.vel[0] += chemical_force * dt

        # 4. Pump attraction force
        if membrane_active and pumps:
            PUMP_ATTRACTION_STRENGTH = 2.0
            for pump in pumps:
                is_na_inside = ion.type == 'Na+' and ion.pos[0] < membrane_x
                is_k_outside = ion.type == 'K+' and ion.pos[0] > membrane_x
                if is_na_inside or is_k_outside:
                    pump_pos = np.array([membrane_x, pump.y_pos])
                    force_vec = pump_pos - ion.pos
                    dist_sq = np.sum(force_vec**2)
                    
                    # Apply force only within a certain radius of the pump
                    if dist_sq < (pump.height * 2.5)**2:
                        force_magnitude = PUMP_ATTRACTION_STRENGTH / (dist_sq + 0.1)
                        force_dir = force_vec / np.sqrt(dist_sq + 1e-6)
                        ion.vel += force_dir * force_magnitude * dt

        # Dampen velocity
        ion.vel *= 0.95

        # Proposed new position
        new_pos = ion.pos + ion.vel * dt

        # 4. Collision with walls
        draw_radius = ion.radius * 2.5
        if new_pos[1] < y_min + draw_radius:
            new_pos[1] = y_min + draw_radius
            ion.vel[1] *= -1
        elif new_pos[1] > y_max - draw_radius:
            new_pos[1] = y_max - draw_radius
            ion.vel[1] *= -1

        if new_pos[0] < x_min + draw_radius:
            new_pos[0] = x_min + draw_radius
            ion.vel[0] *= -1
        elif new_pos[0] > x_max - draw_radius:
            new_pos[0] = x_max - draw_radius
            ion.vel[0] *= -1
        
        # 5. Collision with membrane
        if membrane_active:
            if (ion.pos[0] - membrane_x) * (new_pos[0] - membrane_x) < 0:
                is_permeable = permeability.get(ion.type, False)
                if ion.impermeable or not is_permeable:
                    ion.vel[0] *= -1
                    new_pos[0] = ion.pos[0]
                else:
                    # Ion is crossing
                    if new_pos[0] < membrane_x: # Moving into the cell
                        crossings.append({'type': ion.type, 'direction': 'in'})
                    else: # Moving out of the cell
                        crossings.append({'type': ion.type, 'direction': 'out'})
                    ion.vel[0] *= 0.5

        ion.pos = new_pos
    
    return chunk_of_ions, crossings

class Ion:
    """Represents a single ion with physical properties."""
    def __init__(self, ion_type, x, y):
        self.type = ion_type
        config = ION_CONFIG[ion_type]
        self.radius = config['radius']
        self.color = config['color']
        self.charge = config['charge']
        self.impermeable = config.get('impermeable', False)
        self.pos = np.array([x, y], dtype=float)
        self.vel = (np.random.rand(2) - 0.5) * 0.1
        self.blink_counter = 0

    def start_blink(self, duration=15):
        """Starts the ion's blink effect for a number of frames."""
        self.blink_counter = duration

    def update_blink(self):
        """Decrements the blink counter each frame."""
        if self.blink_counter > 0:
            self.blink_counter -= 1

class NaKPump:
    """Represents an active Na+/K+ pump with visual feedback."""
    def __init__(self, y_pos):
        self.y_pos = y_pos
        self.width = 0.8
        self.height = 1.2
        self.cooldown = 0
        self.cooldown_time = 5
        self.pump_count = 0
        self.animation_phase = 0
        self.animation_speed = 0.2
        self.blink_counter = 0
        self.blink_duration = 15

    def start_blink(self):
        """Starts the pump's blink effect."""
        self.blink_counter = self.blink_duration

    def update_blink(self):
        """Decrements the pump's blink counter."""
        if self.blink_counter > 0:
            self.blink_counter -= 1

    def update_animation(self):
        if self.blink_counter > 0:
            self.animation_phase = (self.animation_phase + self.animation_speed) % (2 * np.pi)
            return np.sin(self.animation_phase) * 0.2  # Oscillation for visual effect
        else:
            self.animation_phase = 0 # Reset for next time
            return 0.0

    def pump(self, ions, membrane_x):
        if self.cooldown > 0:
            self.cooldown -= 1
            return False, []

        # Find closest Na+ and K+ ions within range
        na_inside = [i for i in ions if i.type == 'Na+' and i.pos[0] < membrane_x 
                    and abs(i.pos[1] - self.y_pos) < self.height]
        k_outside = [i for i in ions if i.type == 'K+' and i.pos[0] > membrane_x 
                    and abs(i.pos[1] - self.y_pos) < self.height]

        if len(na_inside) >= 3 and len(k_outside) >= 2:
            na_to_pump = na_inside[:3]
            k_to_pump = k_outside[:2]
            
            crossings = []
            # Move 3 Na+ out and make them blink
            for ion in na_to_pump:
                ion.pos[0] = membrane_x + 0.5
                ion.vel[0] = 2.0  # Give them a push
                ion.start_blink()
                crossings.append({'type': 'Na+', 'direction': 'out'})

            # Move 2 K+ in and make them blink
            for ion in k_to_pump:
                ion.pos[0] = membrane_x - 0.5
                ion.vel[0] = -2.0  # Give them a push
                ion.start_blink()
                crossings.append({'type': 'K+', 'direction': 'in'})
            
            self.cooldown = self.cooldown_time
            self.pump_count += 1
            self.start_blink()
            return True, crossings
        return False, []

class MembraneSimulation:
    def __init__(self, ax, ax_voltage, ax_counts, ax_text):
        self.ax = ax
        self.ax_voltage = ax_voltage
        self.ax_counts = ax_counts
        self.ax_text = ax_text

        self.bounds = np.array([-10, 10, -10, 10])
        self.ions = []
        self.pumps = []
        
        self.membrane_active = True
        self.membrane_x = 0
        self.membrane_width = 0.5
        
        self.permeability = {ion_type: False for ion_type in ION_CONFIG.keys() if ion_type != 'A-'}
        
        self.diffusion_speed = 25.0
        self.electrical_force_strength = 1.0
        self.chemical_force_strength = 1.0
        # Use os.cpu_count() for robust worker determination
        self.executor = ProcessPoolExecutor(max_workers=os.cpu_count())
        self.update_counter = 0
        self.is_running = False
        self.infinite_extracellular = False

        # Data for historical plots
        self.history_size = 100
        self.voltage_history = deque(maxlen=self.history_size)
        self.ion_count_history = deque(maxlen=self.history_size)

        # For blitting - store artists that will be updated
        self.MAX_IONS = 500 # Max ions that can be displayed
        self.ion_circle_artists = []
        self.ion_text_artists = []
        self.pump_artists = []
        self.voltage_line = None
        self.count_lines = {}
        self.potential_artist = None
        self.nernst_artists = {}
        self.membrane_line = None
        self.permeability_lines = {}
        self.extracellular_bg_artist = None
        self.counts_legend = None

    def add_ions(self, ion_type, count, side):
        x_min, x_max, y_min, y_max = self.bounds
        if self.membrane_active:
            if side == 'left':
                x_range = (x_min + 0.5, self.membrane_x - 0.5)
            else:
                x_range = (self.membrane_x + 0.5, x_max - 0.5)
        else:
            x_range = (x_min + 0.5, x_max - 0.5)

        for _ in range(count):
            y = np.random.uniform(y_min + 0.5, y_max - 0.5)
            x = np.random.uniform(*x_range)
            self.ions.append(Ion(ion_type, x, y))

    def clear_ions(self, ion_type=None):
        if ion_type:
            self.ions = [ion for ion in self.ions if ion.type != ion_type]
        else:
            self.ions = []

    def toggle_membrane(self):
        self.membrane_active = not self.membrane_active
        if not self.membrane_active:
            self.pumps = []
        else:
            for ion in self.ions:
                if -0.5 < ion.pos[0] < 0.5:
                    ion.pos[0] = np.sign(ion.pos[0] - self.membrane_x) * 0.6
        print(f"Membrana {'ATIVADA' if self.membrane_active else 'DESATIVADA'}")

    def toggle_ion_permeability(self, ion_type):
        if self.membrane_active:
            self.permeability[ion_type] = not self.permeability[ion_type]
            print(f"Permeabilidade de {ion_type}: {'ATIVADA' if self.permeability[ion_type] else 'DESATIVADA'}")

    def add_pump(self):
        if not self.membrane_active:
            print("Não é possível adicionar a bomba: a membrana não está ativa.")
            return
        # Find an inactive pump artist to activate
        found = False
        for p_artist, pump_obj in self.pump_artists:
            if not pump_obj: # If this slot is empty
                y_pos = np.random.uniform(self.bounds[2] * 0.8, self.bounds[3] * 0.8)
                new_pump = NaKPump(y_pos)
                self.pumps.append(new_pump)
                # Link artist to the new pump object
                self.pump_artists[self.pump_artists.index((p_artist, pump_obj))] = (p_artist, new_pump)
                found = True
                break
        if not found:
            print("Número máximo de bombas atingido.")

    def _compensate_crossings(self, crossings):
        if not self.infinite_extracellular:
            return

        for crossing in crossings:
            ion_type = crossing['type']
            if crossing['direction'] == 'in':
                # Add a new ion to the extracellular space
                x = np.random.uniform(self.membrane_x + 0.5, self.bounds[1] - 0.5)
                y = np.random.uniform(self.bounds[2] + 0.5, self.bounds[3] - 0.5)
                self.ions.append(Ion(ion_type, x, y))
            elif crossing['direction'] == 'out':
                # Remove a random ion of the same type from extracellular space
                candidates = [i for i, ion in enumerate(self.ions) if ion.type == ion_type and ion.pos[0] > self.membrane_x]
                if candidates:
                    ion_to_remove_idx = np.random.choice(candidates)
                    del self.ions[ion_to_remove_idx]

    def _update_history(self):
        stats, voltage = self.calculate_stats()
        self.voltage_history.append(voltage)
        
        counts_to_store = {}
        for ion_type in ['Na+', 'K+', 'Cl-']:
            if ion_type in stats:
                counts_to_store[ion_type] = stats[ion_type]
        self.ion_count_history.append(counts_to_store)

    def update_tick(self):
        dt = 0.1
        self.update_counter += 1

        potential_diff = 0
        counts_by_type = {ion_type: {'left': 0, 'right': 0} for ion_type in self.permeability.keys()}
        left_charge = 0
        right_charge = 0

        if self.membrane_active:
            for ion in self.ions:
                if ion.pos[0] < self.membrane_x:
                    left_charge += ion.charge
                    if ion.type in counts_by_type:
                        counts_by_type[ion.type]['left'] += 1
                else:
                    right_charge += ion.charge
                    if ion.type in counts_by_type:
                        counts_by_type[ion.type]['right'] += 1
            potential_diff = (left_charge - right_charge) * 0.01

        mobile_ions = [ion for ion in self.ions if ion.type != 'A-']
        immobile_ions = [ion for ion in self.ions if ion.type == 'A-']

        if mobile_ions:
            num_workers = self.executor._max_workers
            chunk_size = (len(mobile_ions) + num_workers - 1) // num_workers
            if chunk_size > 0:
                chunks = [mobile_ions[i:i + chunk_size] for i in range(0, len(mobile_ions), chunk_size)]
                
                task_args = [(chunk, dt, self.bounds, self.membrane_x, self.membrane_active, 
                              self.permeability, potential_diff,
                              self.chemical_force_strength, self.diffusion_speed, 
                              self.electrical_force_strength, counts_by_type, self.pumps) 
                             for chunk in chunks]

                results = list(self.executor.map(update_chunk_task, task_args))
                
                updated_mobile_ions = []
                all_crossings = []
                for updated_chunk, crossings in results:
                    updated_mobile_ions.extend(updated_chunk)
                    all_crossings.extend(crossings)

                self.ions = immobile_ions + updated_mobile_ions
                self._compensate_crossings(all_crossings)
        
        for pump in self.pumps:
            pump.update_animation()
            pumped, pump_crossings = pump.pump(self.ions, self.membrane_x)
            if pumped:
                self._compensate_crossings(pump_crossings)
            pump.update_blink()

        for ion in self.ions:
            ion.update_blink()

        self._update_history()
        
    def init_animation(self):
        """Initialize plots for blitting."""
        # Static elements
        self.ax.set_xlim(self.bounds[0], self.bounds[1])
        self.ax.set_ylim(self.bounds[2], self.bounds[3])
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.add_patch(plt.Rectangle((self.bounds[0], self.bounds[2]), 
                                        self.bounds[1]-self.bounds[0], self.bounds[3]-self.bounds[2],
                                        facecolor='none', edgecolor='black'))
        self.ax.text(self.bounds[0], self.bounds[3] + 0.5, "Intracelular (Esquerda)", ha='left', fontsize=16)
        self.ax.text(self.bounds[1], self.bounds[3] + 0.5, "Extracelular (Direita)", ha='right', fontsize=16)

        # Create background for extracellular space
        self.extracellular_bg_artist = self.ax.add_patch(
            plt.Rectangle((self.membrane_x, self.bounds[2]), 
                          self.bounds[1] - self.membrane_x, self.bounds[3] - self.bounds[2],
                          facecolor='lightgrey', alpha=0.3, visible=False, zorder=0)
        )

        # Pre-allocate ion artists
        for i in range(self.MAX_IONS):
            circle = plt.Circle((0,0), 0.25, visible=False) # Increased radius
            self.ax.add_patch(circle)
            self.ion_circle_artists.append(circle)
            
            text = self.ax.text(0, 0, '', ha='center', va='center', color='white',
                                fontsize=10, weight='bold', visible=False)
            self.ion_text_artists.append(text)

        # Create membrane artist
        self.membrane_line, = self.ax.plot([], [], color='red', linewidth=10, solid_capstyle='round')
        
        # Create permeability indicator artists
        y_pos = self.bounds[3] - 1
        for ion_type in self.permeability.keys():
            self.permeability_lines[ion_type], = self.ax.plot([], [], color=ION_CONFIG[ion_type]['color'], linewidth=3)
            y_pos -= 0.5

        # Pre-allocate pump artists (max 10)
        for _ in range(10):
            p_artist = plt.Rectangle((0,0), 0, 0, facecolor='gold', edgecolor='black', zorder=10)
            self.ax.add_patch(p_artist)
            self.pump_artists.append((p_artist, None)) # (artist, pump_object)

        # Voltage plot
        self.ax_voltage.set_title("Potencial de Membrana (mV)", fontsize=18)
        self.ax_voltage.grid(True)
        self.ax_voltage.set_xlim(0, self.history_size)
        self.ax_voltage.set_ylim(-200, 100) # Generous fixed scale
        self.ax_voltage.tick_params(axis='both', which='major', labelsize=12)
        self.voltage_line, = self.ax_voltage.plot([], [], color='orange', linewidth=2.5)
        
        # Ion counts plot
        self.ax_counts.set_title("Contagem de Íons", fontsize=18)
        self.ax_counts.grid(True)
        self.ax_counts.set_xlim(0, self.history_size)
        self.ax_counts.set_ylim(0, 120) # Generous fixed scale
        self.ax_counts.tick_params(axis='both', which='major', labelsize=12)
        for ion_type in ['Na+', 'K+', 'Cl-']:
            color = ION_CONFIG[ion_type]['color']
            self.count_lines[f'{ion_type}_left'], = self.ax_counts.plot([],[], label=f'{ion_type} (Intra)', color=color, linewidth=2.5)
            self.count_lines[f'{ion_type}_right'], = self.ax_counts.plot([],[], label=f'{ion_type} (Extra)', linestyle='--', color=color, linewidth=2.5)
        
        # Text stats
        fig_face_color = self.ax.get_figure().get_facecolor()
        self.ax_text.set_facecolor(fig_face_color)
        for spine in self.ax_text.spines.values():
            spine.set_visible(False)
        self.ax_text.tick_params(top=False, bottom=False, left=False, right=False,
                                 labelleft=False, labelbottom=False)
        self.ax_text.set_ylim(0, 1) # For easy positioning with .text()
        self.ax_text.set_xlim(0, 1)

        font_props = {'family': 'monospace', 'fontsize': 16, 'va': 'top'}
        self.potential_artist = self.ax_text.text(0.05, 1.0, "", fontdict=font_props)
        self.ax_text.text(0.05, 0.9, "                   --- POTENCIAL DE NERNST ---", fontdict=font_props)
        
        y_pos = 0.7
        for ion_type in ['Na+', 'K+', 'Cl-']:
            self.nernst_artists[ion_type] = self.ax_text.text(0.05, y_pos, "", fontdict=font_props)
            y_pos -= 0.23
        
        # Return all dynamic artists to be managed by the animation
        all_artists = [self.potential_artist, self.voltage_line, self.extracellular_bg_artist] + \
               self.ion_circle_artists + self.ion_text_artists + \
               list(self.count_lines.values()) + list(self.nernst_artists.values()) + \
               [p[0] for p in self.pump_artists] + \
               [self.membrane_line] + list(self.permeability_lines.values())
        return all_artists

    def update_animation(self, frame):
        """Update the plot for the current animation frame."""
        self.update_tick()
        
        # Update artists
        self.update_artists()
        
        # Return all artists that need to be redrawn
        all_artists = [self.potential_artist, self.voltage_line, self.extracellular_bg_artist] + \
               self.ion_circle_artists + self.ion_text_artists + \
               list(self.count_lines.values()) + list(self.nernst_artists.values()) + \
               [p[0] for p in self.pump_artists] + \
               [self.membrane_line] + list(self.permeability_lines.values())
        return all_artists

    def update_artists(self):
        """Helper function to update all the artists on the screen."""
        # Update ions using the artist pool
        for i in range(self.MAX_IONS):
            if i < len(self.ions):
                ion = self.ions[i]
                circle = self.ion_circle_artists[i]
                text = self.ion_text_artists[i]

                # Update circle
                is_blinking = ion.blink_counter > 0
                circle.center = ion.pos
                face_color = ion.color
                circle.set_facecolor(face_color)
                circle.set_edgecolor(face_color)
                circle.set_linewidth(3.0 if is_blinking else 0.0)
                circle.set_radius(ION_CONFIG[ion.type]['radius'] * 2.0)
                circle.set_visible(True)
                
                # Update text
                text.set_position(ion.pos)
                text.set_text(ion.type)
                text.set_visible(True)

            else:
                # Hide unused artists
                self.ion_circle_artists[i].set_visible(False)
                self.ion_text_artists[i].set_visible(False)

        # Update membrane and background
        self.extracellular_bg_artist.set_visible(self.infinite_extracellular and self.membrane_active)
        if self.membrane_active:
            self.membrane_line.set_data([self.membrane_x, self.membrane_x], [self.bounds[2], self.bounds[3]])
            self.membrane_line.set_color('black')
            
            y_pos = self.bounds[3] - 1
            for ion_type, line in self.permeability_lines.items():
                if self.permeability.get(ion_type, False):
                    line.set_data([self.membrane_x - 0.2, self.membrane_x + 0.2], [y_pos, y_pos])
                else:
                    line.set_data([], []) # Hide if not permeable
                y_pos -= 0.5
        else:
            self.membrane_line.set_data([], [])
            for line in self.permeability_lines.values():
                line.set_data([], [])

        # Update pumps
        for p_artist, pump_obj in self.pump_artists:
            if pump_obj and pump_obj in self.pumps:
                is_blinking = pump_obj.blink_counter > 0
                pump_color = 'orange' if is_blinking else 'gold'
                scale = 1.2 if is_blinking else 1.0
                x = self.membrane_x + pump_obj.update_animation()
                
                p_artist.set_xy((x - (pump_obj.width*scale)/2, pump_obj.y_pos - (pump_obj.height*scale)/2))
                p_artist.set_width(pump_obj.width * scale)
                p_artist.set_height(pump_obj.height * scale)
                p_artist.set_facecolor(pump_color)
                p_artist.set_visible(True)
            else:
                p_artist.set_visible(False)

        # --- Update Plots and Text ---
        stats, voltage = self.calculate_stats()
        
        # Update voltage plot data
        self.voltage_line.set_data(range(len(self.voltage_history)), list(self.voltage_history))
        
        # Update ion count plot data
        plotted_ions = ['Na+', 'K+', 'Cl-']
        for ion_type in plotted_ions:
            left_counts = [h.get(ion_type, {}).get('left', 0) for h in self.ion_count_history]
            right_counts = [h.get(ion_type, {}).get('right', 0) for h in self.ion_count_history]
            self.count_lines[f'{ion_type}_left'].set_data(range(len(left_counts)), left_counts)
            self.count_lines[f'{ion_type}_right'].set_data(range(len(right_counts)), right_counts)

        # Update text stats
        self.potential_artist.set_text(f"Potencial: {voltage:+.1f} mV")
        
        R, T, F = 8.314, 310, 96485
        RT_F = (R * T) / F * 1000
        for ion_type in ['Na+', 'K+', 'Cl-']:
            if ion_type in stats:
                C_in = stats[ion_type]['left']
                C_out = stats[ion_type]['right']
                charge = ION_CONFIG[ion_type]['charge']
                nernst = 'N/A'
                if C_in > 0 and C_out > 0:
                    nernst = f"{(RT_F / charge) * np.log(C_out / C_in):+.1f} mV"
                self.nernst_artists[ion_type].set_text(f"{ion_type}: {nernst}")

    def calculate_stats(self):
        stats = {t: {'left': 0, 'right': 0} for t in ION_CONFIG}
        left_charge = 0
        right_charge = 0
        
        for ion in self.ions:
            if ion.pos[0] < self.membrane_x:
                stats[ion.type]['left'] += 1
                left_charge += ion.charge
            else:
                stats[ion.type]['right'] += 1
                right_charge += ion.charge

        if self.membrane_active:
            voltage = (left_charge - right_charge) * 1
        else:
            voltage = 0

        return stats, voltage

    def reset(self):
        self.ions = []
        self.pumps = []
        self.membrane_active = True
        self.permeability = {ion_type: False for ion_type in ION_CONFIG.keys() if ion_type != 'A-'}
        self.voltage_history.clear()
        self.ion_count_history.clear()
        # Reset pump artists
        new_pump_artists = []
        for p_artist, _ in self.pump_artists:
            p_artist.set_visible(False)
            new_pump_artists.append((p_artist, None))
        self.pump_artists = new_pump_artists
        print("Simulação reiniciada.")

# --- Global variables and UI callback functions ---
sim = None
anim = None
btn_start_stop = None
check_buttons = None
fig = None

def _update_if_paused():
    """Helper function to force a screen redraw if the animation is paused."""
    if sim and not sim.is_running:
        sim.update_artists()
        fig.canvas.draw_idle()

def on_start_stop(event):
    global sim, btn_start_stop
    if sim:
        sim.is_running = not sim.is_running
        if sim.is_running:
            anim.event_source.start()
            btn_start_stop.label.set_text("Parar")
            print("Simulação em execução.")
        else:
            anim.event_source.stop()
            btn_start_stop.label.set_text("Iniciar")
            print("Simulação pausada.")

def on_reset(event):
    global sim, check_buttons
    if sim:
        sim.reset()
        if check_buttons:
            for i in range(len(check_buttons.labels)):
                check_buttons.set_active(i, False)
        _update_if_paused()
    
def add_ion_factory(ion_type, count, side):
    def on_add(event):
        global sim
        if sim:
            sim.add_ions(ion_type, count, side)
            _update_if_paused()
    return on_add

def on_toggle_membrane(event):
    global sim
    if sim:
        sim.toggle_membrane()
        _update_if_paused()

def on_toggle_permeability(label):
    global sim
    if sim:
        ion_type = label.strip()
        # The .labels attribute holds Text objects, so we get the string from each.
        labels_text = [l.get_text() for l in check_buttons.labels]
        try:
            ion_index = labels_text.index(ion_type)
            # The on_clicked event fires *after* the button's state has changed.
            # We get the new state and sync the simulation to it.
            current_state = check_buttons.get_status()[ion_index]
            if sim.permeability[ion_type] != current_state:
                sim.toggle_ion_permeability(ion_type)

            _update_if_paused()
        except ValueError:
            # This can happen if the label isn't found, which would be unexpected.
            print(f"Error: Could not find ion type '{ion_type}' in checkbox labels.")

def on_add_pump(event):
    global sim
    if sim:
        sim.add_pump()
        _update_if_paused()

def on_toggle_infinite_extracellular(event):
    global sim
    if sim:
        sim.infinite_extracellular = not sim.infinite_extracellular
        mode = "ATIVADO" if sim.infinite_extracellular else "DESATIVADO"
        print(f"Modo extracelular infinito: {mode}")
        _update_if_paused()
        
def animation_update(frame):
    global sim
    # This function is now the main entry point for the animation frame
    if sim.is_running:
        return sim.update_animation(frame)
    # Return current artists without updating if paused
    all_artists = [sim.potential_artist, sim.voltage_line, sim.extracellular_bg_artist] + \
           sim.ion_circle_artists + sim.ion_text_artists + \
           list(sim.count_lines.values()) + list(sim.nernst_artists.values()) + \
           [p[0] for p in sim.pump_artists] + \
           [sim.membrane_line] + list(sim.permeability_lines.values())
    return all_artists

def main():
    global sim, anim, btn_start_stop, check_buttons, fig
    
    fig = plt.figure(figsize=(20, 11))
    gs = fig.add_gridspec(4, 2, width_ratios=[1.5, 2], height_ratios=[4, 4, 1.5, 1])
    
    # Right side for simulation
    ax_main = fig.add_subplot(gs[:, 1])

    # Left side for plots and controls
    ax_voltage = fig.add_subplot(gs[0, 0])
    ax_counts = fig.add_subplot(gs[1, 0])
    ax_text = fig.add_subplot(gs[2, 0])
    # The bottom-left area gs[3, 0] is reserved for buttons
    
    # plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.95, wspace=0.2, hspace=0.9)
    plt.subplots_adjust(left=0.03, bottom=0.01, right=0.99, top=0.96, wspace=0.1, hspace=0.9)

    sim = MembraneSimulation(ax_main, ax_voltage, ax_counts, ax_text)

    # --- UI Setup in the bottom-left corner ---
    all_buttons = []
    
    # Define layout for two rows of buttons in the bottom-left
    row1_y, row2_y = 0.11, 0.04
    btn_h = 0.06

    # --- Row 1: Main Controls ---
    ctrl_w = 0.055
    ctrl_start_x = 0.06
    ctrl_gap = 0.005
    
    ax_start_stop = fig.add_axes([ctrl_start_x, row1_y, ctrl_w, btn_h])
    btn_start_stop = Button(ax_start_stop, 'Iniciar')
    btn_start_stop.on_clicked(on_start_stop)
    
    current_x = ctrl_start_x + ctrl_w + ctrl_gap
    ax_reset = fig.add_axes([current_x, row1_y, ctrl_w, btn_h])
    btn_reset = Button(ax_reset, 'Reiniciar')
    btn_reset.on_clicked(on_reset)
    
    current_x += ctrl_w + ctrl_gap
    ax_membrane = fig.add_axes([current_x, row1_y, ctrl_w, btn_h])
    btn_membrane = Button(ax_membrane, 'Membrana')
    btn_membrane.on_clicked(on_toggle_membrane)
    
    current_x += ctrl_w + ctrl_gap
    ax_add_pump = fig.add_axes([current_x, row1_y, ctrl_w, btn_h])
    btn_add_pump = Button(ax_add_pump, 'Bomba')
    btn_add_pump.on_clicked(on_add_pump)
    
    current_x += ctrl_w + ctrl_gap
    ax_infinite_mode = fig.add_axes([current_x, row1_y, ctrl_w, btn_h])
    btn_infinite_mode = Button(ax_infinite_mode, 'Infinito')
    btn_infinite_mode.on_clicked(on_toggle_infinite_extracellular)

    # --- Permeability Checkboxes ---
    permeability_ions = [it for it in ION_CONFIG.keys() if it != 'A-']
    ax_check = fig.add_axes([ctrl_start_x + 5*(ctrl_w+ctrl_gap), row1_y, 0.06, btn_h * 1.5])
    check_buttons = CheckButtons(ax_check, permeability_ions, [False] * len(permeability_ions))
    check_buttons.on_clicked(on_toggle_permeability)
    
    # --- Row 2: Add Ion Buttons ---
    ion_w = 0.04
    ion_start_x = 0.06
    ion_gap = 0.005
    # fig.text(ion_start_x, row2_y + btn_h, 'Adicionar Íons (Intra | Extra):', transform=fig.transFigure, fontsize=14)
    
    for i, ion_type in enumerate(ION_CONFIG.keys()):
        current_x = ion_start_x + i * (ion_w * 2 + ion_gap * 2.5)
        
        ax_add_left = fig.add_axes([current_x, row2_y, ion_w, btn_h])
        btn_add_left = Button(ax_add_left, f'+5 {ion_type}')
        btn_add_left.on_clicked(add_ion_factory(ion_type, 5, 'left'))
        all_buttons.append(btn_add_left)
        
        ax_add_right = fig.add_axes([current_x + ion_w + ion_gap, row2_y, ion_w, btn_h])
        btn_add_right = Button(ax_add_right, f'+5 {ion_type}')
        btn_add_right.on_clicked(add_ion_factory(ion_type, 5, 'right'))
        all_buttons.append(btn_add_right)

    sim.init_animation()
    anim = animation.FuncAnimation(fig, animation_update, 
                                 init_func=sim.init_animation,
                                 frames=None, interval=1, blit=True, cache_frame_data=False)
    anim.event_source.stop()

    # Draw the initial state
    sim.update_artists()
    fig.canvas.draw_idle()

    plt.show()

if __name__ == "__main__":
    # This is important for multiprocessing to work correctly on all platforms
    main()
