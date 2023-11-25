import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
	def __init__(self, container, *args, **kwargs):
			super().__init__(container, *args, **kwargs)

			self.canvas = tk.Canvas(self)
			scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
			self.scrollable_frame = tk.Frame(self.canvas)

			self.scrollable_frame.bind(
					"<Configure>",
					lambda e: self.canvas.configure(
							scrollregion=self.canvas.bbox("all")
					)
			)

			self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
			self.canvas.configure(yscrollcommand=scrollbar.set)

			# Bind the mouse wheel event
			self.canvas.bind("<MouseWheel>", self.on_mousewheel)

			self.canvas.pack(side="left", fill="both", expand=True)
			scrollbar.pack(side="right", fill="y")

	def on_mousewheel(self, event):
			self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def main():
    root = tk.Tk()
    root.title("Soccer Game Control")

    # Create a scrollable frame for the entire UI
    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill="both", expand=True)

    # Information Section
    information_frame = tk.Frame(scrollable_frame.scrollable_frame)
    information_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    add_parameter_widgets(information_frame)

    # Team A Section
    team_a_frame = tk.Frame(scrollable_frame.scrollable_frame)
    team_a_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tk.Label(team_a_frame, text="Team A").grid(row=0, column=0, columnspan=5, pady=5)
    populate_team_frame(team_a_frame, "Team A")

    # Team B Section
    team_b_frame = tk.Frame(scrollable_frame.scrollable_frame)
    team_b_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    tk.Label(team_b_frame, text="Team B").grid(row=0, column=0, columnspan=5, pady=5)
    populate_team_frame(team_b_frame, "Team B")

    # Ball Section
    ball_frame = tk.Frame(scrollable_frame.scrollable_frame)
    ball_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    tk.Label(ball_frame, text="Ball").grid(row=0, column=0, columnspan=5, pady=5)
    # Add labels and entry widgets for ball information (similar to team information)

    # Controls Section
    controls_frame = tk.Frame(scrollable_frame.scrollable_frame)
    controls_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

    tk.Label(controls_frame, text="Controls").grid(row=0, column=0, columnspan=5, pady=5)
    add_simulation_controls(controls_frame)

    root.mainloop()

def add_parameter_widgets(container):
    # Add labels, entry widgets, and error labels for simulation parameters
    parameters = ["Environment Size", "Team A Players", "Team B Players", "Match Length",
                  "Simulation Mode", "Max Episodes", "Randomize Positions"]

    parameter_entries = {}
    error_labels = {}

    for i, parameter in enumerate(parameters):
        label = tk.Label(container, text=f"{parameter}:")
        label.grid(row=i + 1, column=0, pady=5, sticky="e")

        entry = tk.Entry(container)
        entry.grid(row=i + 1, column=1, pady=5)
        parameter_entries[parameter] = entry

        error_label = tk.Label(container, text="", fg="red")
        error_label.grid(row=i + 1, column=2, pady=5)
        error_labels[parameter] = error_label

def populate_team_frame(frame, team_name):
    # Add labels for player information
    tk.Label(frame, text="Player Name").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame, text="Velocity, Position, Orientation").grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame, text="Control Brain").grid(row=1, column=2, padx=5, pady=5)
    tk.Label(frame, text="Losses").grid(row=1, column=3, padx=5, pady=5)
    tk.Label(frame, text="Configuration").grid(row=1, column=4, padx=5, pady=5)

    # Add player information frames
    for i in range(6):
        player_frame = tk.Frame(frame, borderwidth=1, relief="solid")
        player_frame.grid(row=i + 2, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

        # Player Name
        player_name_label = tk.Label(player_frame, text=f"{team_name} Player {i + 1}")
        player_name_label.grid(row=0, column=0, padx=5, pady=5)

        # Velocity, Position, Orientation
        vpo_label = tk.Label(player_frame, text="V, P, O")
        vpo_label.grid(row=1, column=0, padx=5, pady=5)

        # Control Brain (Dropdown)
        control_brain_options = ["DDPG", "Manual", "PPO"]
        control_brain_var = tk.StringVar()
        control_brain_var.set(control_brain_options[0])  # Set default value
        control_brain_dropdown = tk.OptionMenu(player_frame, control_brain_var, *control_brain_options)
        control_brain_dropdown.grid(row=2, column=0, padx=5, pady=5)

        # Losses
        losses_label = tk.Label(player_frame, text="0")
        losses_label.grid(row=3, column=0, padx=5, pady=5)

        # Configuration
        config_label = tk.Label(player_frame, text="Config")
        config_label.grid(row=4, column=0, padx=5, pady=5)

def add_simulation_controls(container):
    # Add buttons for simulation controls
    start_button = tk.Button(container, text="Start Simulation", command=start_simulation)
    start_button.grid(row=1, column=0, pady=5)

    pause_button = tk.Button(container, text="Pause Simulation", command=pause_simulation)
    pause_button.grid(row=2, column=0, pady=5)

    cancel_button = tk.Button(container, text="Cancel Simulation", command=cancel_simulation)
    cancel_button.grid(row=3, column=0, pady=5)

def start_simulation():
    # Implement the logic for starting the simulation
    print("Simulation started")

def pause_simulation():
    # Implement the logic for pausing the simulation
    print("Simulation paused")

def cancel_simulation():
    # Implement the logic for canceling the simulation
    print("Simulation canceled")

if __name__ == "__main__":
    main()
