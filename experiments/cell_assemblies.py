# Not made by me

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation

class Neuron:
    def __init__(self, id):
        self.id = id
        self.is_firing = False
        self.activation = 0.0
        self.is_selected = False
        self.is_user_commanded_fire = False # True if directly commanded by user to fire
        self.blink_counter = 0
        self.blink_duration_on = 2 # Frames to be "on" during a blink
        self.blink_duration_off = 2 # Frames to be "off" during a blink

    def fire(self, user_commanded=False):
        self.is_firing = True
        self.activation = 1.0
        if user_commanded:
            self.is_user_commanded_fire = True
        # Reset blink counter to start the "on" phase of blinking
        self.blink_counter = self.blink_duration_on 

    def reset_fire_state(self): # Call when stopping fire, not full reset
        self.is_firing = False
        self.activation = 0.0
        self.is_user_commanded_fire = False
        self.blink_counter = 0

    def full_reset(self):
        self.reset_fire_state()
        self.is_selected = False
        
    def update_blink(self):
        if self.is_firing:
            self.blink_counter -= 1
            if self.blink_counter <= -self.blink_duration_off: # Cycle completed
                self.blink_counter = self.blink_duration_on # Start new on-phase
        else:
            self.blink_counter = 0 # Not firing, so not blinking

class CellAssembly:
    def __init__(self, num_neurons, ax):
        self.num_neurons = num_neurons
        self.neurons = [Neuron(i) for i in range(num_neurons)]
        self.ax = ax
        self.synapses = np.random.rand(num_neurons, num_neurons) * 0.05
        np.fill_diagonal(self.synapses, 0)
        self.neuron_positions = np.array([
            [np.cos(2 * np.pi * i / self.num_neurons), np.sin(2 * np.pi * i / self.num_neurons)]
            for i in range(self.num_neurons)
        ])
        self.selected_action_indices = []
        self.user_commanded_fire_indices = set() # Neurons user wants to keep firing
        
        self.learning_rate = 0.01 # Slower for continuous learning
        self.firing_threshold = 0.5 
        self.decay_rate = 0.1 
        self.activation_scale = 0.5 # How much activation a firing neuron spreads

        # Inhibition parameters
        self.inhibition_active = False
        self.inhibition_strength = 0.15 # Adjusted for potential impact
        self.inhibition_immunity_threshold = 0.75 # If synapse[i,j] is above this, i won't inhibit j

    def toggle_neuron_selection(self, neuron_idx):
        if 0 <= neuron_idx < self.num_neurons:
            neuron = self.neurons[neuron_idx]
            neuron.is_selected = not neuron.is_selected
            if neuron.is_selected:
                if neuron_idx not in self.selected_action_indices:
                    self.selected_action_indices.append(neuron_idx)
            else:
                if neuron_idx in self.selected_action_indices:
                    self.selected_action_indices.remove(neuron_idx)
            self.plot_network() # Update plot to show selection change

    def start_firing_selected_neurons(self):
        if not self.selected_action_indices:
            print("No neurons selected to start firing.")
            return False # Indicate simulation should not start

        self.user_commanded_fire_indices = set(self.selected_action_indices)
        print(f"User commanded neurons {self.user_commanded_fire_indices} to start firing.")
        
        # Reset activations of all neurons before starting a new commanded fire sequence
        for i, neuron in enumerate(self.neurons):
            neuron.activation = 0.0
            neuron.is_firing = False # Will be set by fire() if commanded
            neuron.is_user_commanded_fire = False
            if i in self.user_commanded_fire_indices:
                neuron.fire(user_commanded=True)
        self.plot_network()
        return True # Indicate simulation should start

    def stop_all_firing(self):
        print("Stopping all firing and network activity.")
        self.user_commanded_fire_indices.clear()
        for neuron in self.neurons:
            neuron.reset_fire_state()
        self.plot_network()
        return False # Indicate simulation should stop

    def update_tick(self):
        # 1. Ensure user-commanded neurons are firing (or trying to)
        for idx in self.user_commanded_fire_indices:
            # If it was somehow turned off by network dynamics, user command overrides for this tick
            if not self.neurons[idx].is_firing:
                 self.neurons[idx].fire(user_commanded=True)
            # Ensure activation is high if user commanded, and it IS user commanded.
            self.neurons[idx].activation = 1.0 
            self.neurons[idx].is_user_commanded_fire = True

        # 2. Hebbian learning for co-firing user-commanded group
        if len(self.user_commanded_fire_indices) >= 2:
            # Create a list from the set for indexing if needed, or iterate directly
            commanded_list = list(self.user_commanded_fire_indices)
            for i_idx in range(len(commanded_list)):
                for j_idx in range(i_idx + 1, len(commanded_list)):
                    neuron_i_actual_idx = commanded_list[i_idx]
                    neuron_j_actual_idx = commanded_list[j_idx]
                    # Check if both are *actually* firing (they should be if user-commanded)
                    if self.neurons[neuron_i_actual_idx].is_firing and self.neurons[neuron_j_actual_idx].is_firing:
                        # Strengthen synapse
                        self.synapses[neuron_i_actual_idx, neuron_j_actual_idx] = min(1.0, self.synapses[neuron_i_actual_idx, neuron_j_actual_idx] + self.learning_rate)
                        self.synapses[neuron_j_actual_idx, neuron_i_actual_idx] = min(1.0, self.synapses[neuron_j_actual_idx, neuron_i_actual_idx] + self.learning_rate)
        
        # 3. Activation propagation and network-driven firing
        new_activations = np.zeros(self.num_neurons)
        current_activations = np.array([n.activation for n in self.neurons])

        for i in range(self.num_neurons):
            if self.neurons[i].is_firing: # Only firing neurons spread activation
                for j in range(self.num_neurons):
                    if i == j: continue
                    # Spread scaled activation based on synapse strength
                    new_activations[j] += current_activations[i] * self.synapses[i, j] * self.activation_scale

        for i in range(self.num_neurons):
            neuron = self.neurons[i]
            # Decay existing activation if not user-commanded to fire
            if i not in self.user_commanded_fire_indices:
                neuron.activation = max(0, neuron.activation - self.decay_rate)
            
            # Add propagated excitatory activation
            neuron.activation = min(1.0, neuron.activation + new_activations[i])

        # 3.5 Apply Inhibition if active
        if self.inhibition_active:
            # Collect all neurons that were firing *before* this inhibition step
            # This includes both user-commanded and network-activated from the previous sub-step within update_tick
            currently_firing_indices_for_inhibition = [k for k, n in enumerate(self.neurons) if n.is_firing]

            for i_idx in currently_firing_indices_for_inhibition:
                for j_idx in range(self.num_neurons):
                    if i_idx == j_idx: continue # Neuron doesn't inhibit itself

                    # Check if neuron i should inhibit neuron j
                    if self.synapses[i_idx, j_idx] < self.inhibition_immunity_threshold:
                        # Apply inhibition
                        self.neurons[j_idx].activation = max(0, self.neurons[j_idx].activation - self.inhibition_strength)
                        # If inhibition stops a user-commanded neuron, that's a dynamic we might want or not.
                        # For now, inhibition can affect anyone not immune.

        # 4. Final check for firing based on potentially modified activation
        for i in range(self.num_neurons):
            neuron = self.neurons[i]
            # If user commanded, it should already be firing. This is for network-driven changes.
            if i not in self.user_commanded_fire_indices:
                if not neuron.is_firing and neuron.activation >= self.firing_threshold:
                    neuron.fire(user_commanded=False) # Network driven fire
                elif neuron.is_firing and neuron.activation < self.firing_threshold:
                    neuron.is_firing = False 
                    neuron.is_user_commanded_fire = False # ensure this is off
            
            neuron.update_blink() 

    def clear_selection(self):
        self.selected_action_indices = []
        for n in self.neurons:
            n.is_selected = False
        if not is_simulation_running: # Only plot if sim isn't also causing a plot
            self.plot_network()

    def reset_network_state(self, reset_synapses=False):
        global is_simulation_running
        is_simulation_running = self.stop_all_firing() # Stop sim and reset states
        print("Resetting network state.")
        for neuron in self.neurons:
            neuron.full_reset()
        if reset_synapses:
            self.synapses = np.random.rand(self.num_neurons, self.num_neurons) * 0.05
            np.fill_diagonal(self.synapses, 0)
            print("Synapses have been reset to initial random values.")
        self.selected_action_indices = []
        self.plot_network()

    def plot_network(self, title=None):
        self.ax.clear()
        self.ax.axis('off') # Remove the plot borders/axes

        for i in range(self.num_neurons):
            for j in range(i + 1, self.num_neurons):
                weight = (self.synapses[i, j] + self.synapses[j, i]) / 2 
                if weight > 0.01:
                    linewidth = weight * 8 + 0.5
                    alpha = min(max(weight * 1.5, 0.2), 1.0)
                    self.ax.plot([self.neuron_positions[i, 0], self.neuron_positions[j, 0]],
                                 [self.neuron_positions[i, 1], self.neuron_positions[j, 1]],
                                 'k-', lw=linewidth, alpha=alpha, zorder=1)

        for idx, neuron in enumerate(self.neurons):
            pos = self.neuron_positions[idx]
            color = 'blue'    # Inactive
            edge_color = 'gray'
            # Further Increased base size and activation scaling for larger nodes
            current_size = 220 + neuron.activation * 300 
            is_blinking_on = neuron.is_firing and (neuron.blink_counter > 0) 

            if neuron.is_user_commanded_fire and neuron.is_firing:
                color = 'orange' if is_blinking_on else 'darkorange' 
                edge_color = 'black'
            elif neuron.is_firing: # Network activated firing
                color = 'red' if is_blinking_on else 'darkred'
                edge_color = 'maroon'
            elif neuron.is_selected:
                color = 'green'  # Selected for Action
                edge_color = 'darkgreen'
            
            # Increased linewidths for thicker edges
            self.ax.scatter(pos[0], pos[1], s=current_size, c=color, zorder=2, edgecolors=edge_color, linewidths=3.0, alpha=0.95)
            self.ax.text(pos[0], pos[1] + 0.16, str(neuron.id), ha='center', va='bottom', fontsize=9, color='black')

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.axis('equal')
        # self.ax.axis('off') # Also ensure it's off after set_title if title was used
        if title:
            self.ax.set_title(title, pad=10) # Add some padding if title is present
        else: # ensure axis is off if no title is drawn over it potentially re-enabling it
            self.ax.set_title("") # Clear any previous title
            self.ax.axis('off')

        self.ax.figure.canvas.draw_idle()

# --- Global variables and UI callback functions ---
assembly = None
is_simulation_running = False
anim = None # Store animation object

def on_click(event):
    global assembly, is_simulation_running
    if event.inaxes != assembly.ax or assembly is None or is_simulation_running:
        # Disable selection changes while simulation is running for simplicity
        if is_simulation_running:
            print("Stop firing to change selection.")
        return
    min_dist_sq = float('inf')
    clicked_neuron_idx = -1
    for i, pos in enumerate(assembly.neuron_positions):
        dist_sq = (pos[0] - event.xdata)**2 + (pos[1] - event.ydata)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            clicked_neuron_idx = i
    
    # Approximate click radius based on default neuron size on screen (adjust factor as needed)
    # This is a rough way to make clicking easier on the neuron body
    click_radius_sq = ( (60 / (assembly.ax.figure.dpi * 2) )**2 ) * 15 
    if clicked_neuron_idx != -1 and min_dist_sq < click_radius_sq: 
         assembly.toggle_neuron_selection(clicked_neuron_idx)

def start_stop_firing_callback(event):
    global assembly, is_simulation_running, anim
    if assembly:
        if not is_simulation_running:
            if assembly.start_firing_selected_neurons():
                is_simulation_running = True
                btn_start_stop.label.set_text("Stop Firing")
                if anim: anim.event_source.start() # Resume animation updates
                print("Simulation started.")
            else:
                print("Could not start simulation (e.g. no neurons selected).")
        else:
            is_simulation_running = assembly.stop_all_firing()
            btn_start_stop.label.set_text("Start Firing")
            if anim: anim.event_source.stop() # Pause animation updates
            print("Simulation stopped.")
        assembly.plot_network() # Ensure plot is updated with button label change

def clear_selection_callback(event):
    global assembly, is_simulation_running
    if assembly and not is_simulation_running:
        assembly.clear_selection()
    elif is_simulation_running:
        print("Stop firing to clear selection.")

def reset_activations_callback(event):
    global assembly
    if assembly: assembly.reset_network_state(reset_synapses=False)

def reset_all_callback(event):
    global assembly
    if assembly: assembly.reset_network_state(reset_synapses=True)

btn_start_stop = None # Declare globally for callback to update label
btn_toggle_inhibition = None # Declare for global access

def animation_update_frame(frame_num):
    global assembly, is_simulation_running
    if assembly and is_simulation_running:
        assembly.update_tick()
        # Plotting is now handled by update_tick if necessary or by explicit calls
        # to avoid double plotting if update_tick calls plot_network.
        # For animation, we must call plot_network here to refresh the canvas.
        assembly.plot_network() 
    return [] # Required by FuncAnimation

# Callback for Toggle Inhibition button
def toggle_inhibition_callback(event):
    global assembly, btn_toggle_inhibition
    if assembly:
        assembly.inhibition_active = not assembly.inhibition_active
        if assembly.inhibition_active:
            btn_toggle_inhibition.label.set_text("Inhibition: ON")
            print("Inhibition: ON")
        else:
            btn_toggle_inhibition.label.set_text("Inhibition: OFF")
            print("Inhibition: OFF")
        if not is_simulation_running: # Redraw if sim is paused to show label change
            assembly.plot_network()

if __name__ == "__main__":
    fig, ax_main = plt.subplots(figsize=(10, 8.5))
    # Adjust layout: more space on right for vertical buttons
    # left, bottom, right, top
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.78, top=0.95)

    num_neurons_sim = 12
    assembly = CellAssembly(num_neurons_sim, ax_main)
    
    # Button properties
    button_width = 0.18
    button_height = 0.06
    button_x_start = 0.81 # Start x-position for buttons (right side)
    button_y_start = 0.85 # Start y-position for top button
    button_y_spacing = 0.03 # Vertical space between buttons

    # Create buttons - Arranged Vertically
    ax_start_stop_button = plt.axes([button_x_start, button_y_start, button_width, button_height])
    btn_start_stop = Button(ax_start_stop_button, 'Start Firing')
    btn_start_stop.on_clicked(start_stop_firing_callback)

    current_y = button_y_start - button_height - button_y_spacing
    ax_toggle_inhibition_button = plt.axes([button_x_start, current_y, button_width, button_height])
    btn_toggle_inhibition = Button(ax_toggle_inhibition_button, 'Inhibition: OFF') # Initial state
    btn_toggle_inhibition.on_clicked(toggle_inhibition_callback)

    current_y -= (button_height + button_y_spacing)
    ax_clear_sel_button = plt.axes([button_x_start, current_y, button_width, button_height])
    btn_clear_sel = Button(ax_clear_sel_button, 'Clear Selection')
    btn_clear_sel.on_clicked(clear_selection_callback)

    current_y -= (button_height + button_y_spacing)
    ax_reset_act_button = plt.axes([button_x_start, current_y, button_width, button_height])
    btn_reset_act = Button(ax_reset_act_button, 'Reset Activations')
    btn_reset_act.on_clicked(reset_activations_callback)

    current_y -= (button_height + button_y_spacing)
    ax_reset_all_button = plt.axes([button_x_start, current_y, button_width, button_height])
    btn_reset_all = Button(ax_reset_all_button, 'Reset Synapses & Acts')
    btn_reset_all.on_clicked(reset_all_callback)
    
    assembly.plot_network() # Initial plot
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Set up the animation
    # Interval in ms. Controls how fast the simulation runs.
    anim = animation.FuncAnimation(fig, animation_update_frame, frames=None, 
                                   interval=150, blit=False, cache_frame_data=False)
    if not is_simulation_running: # Start paused
        anim.event_source.stop()

    plt.sca(ax_main) # Ensure main plot area is active for any further direct plt commands if any
    plt.show()

