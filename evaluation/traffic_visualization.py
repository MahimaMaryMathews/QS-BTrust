import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

AREA_SIZE = 2000

def simulate_traffic(num_vehicles):
    positions = np.random.rand(num_vehicles, 2) * AREA_SIZE
    velocities = np.random.rand(num_vehicles, 2) * 15 + 5
    transmission_ranges = np.random.rand(num_vehicles) * 1500
    return positions, velocities, transmission_ranges


def get_vehicles_in_range(selected_vehicle_idx, positions, transmission_ranges):
    selected_position = positions[selected_vehicle_idx]
    transmission_range = transmission_ranges[selected_vehicle_idx]

    distances = np.linalg.norm(positions - selected_position, axis=1)
    in_range_idx = np.where(distances <= transmission_range)[0]

    return in_range_idx

def update(frame, scat, scat_in_range, scat_selected,
           positions, velocities, selected_vehicle_idx,
           transmission_ranges, transmission_circle):

    positions += velocities * 0.1
    positions[:] = np.mod(positions, AREA_SIZE)

    transmission_circle.center = positions[selected_vehicle_idx]

    in_range_idx = get_vehicles_in_range(selected_vehicle_idx, positions, transmission_ranges)

    scat.set_offsets(positions)
    scat_in_range.set_offsets(positions[in_range_idx])
    scat_selected.set_offsets([positions[selected_vehicle_idx]])

    return scat, scat_in_range, scat_selected, transmission_circle


def run_simulation(num_vehicles):
    positions, velocities, transmission_ranges = simulate_traffic(num_vehicles)

    selected_vehicle_idx = np.random.randint(num_vehicles)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, AREA_SIZE)
    ax.set_ylim(0, AREA_SIZE)

    ax.set_title(
        f"Traffic Simulation ({num_vehicles} Vehicles)\n"
        f"Selected Vehicle Index: {selected_vehicle_idx}"
    )

    scat = ax.scatter(positions[:, 0], positions[:, 1], s=10, c='blue', label="Vehicles")
    scat_in_range = ax.scatter([], [], s=10, c='red', label="In Range")
    scat_selected = ax.scatter(
        positions[selected_vehicle_idx, 0],
        positions[selected_vehicle_idx, 1],
        s=50,
        c='green',
        label="Selected Vehicle"
    )

    transmission_circle = plt.Circle(
        (positions[selected_vehicle_idx, 0], positions[selected_vehicle_idx, 1]),
        transmission_ranges[selected_vehicle_idx],
        color='orange',
        fill=False,
        linestyle='--',
        label="Transmission Range"
    )

    ax.add_patch(transmission_circle)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=100,
        fargs=(
            scat, scat_in_range, scat_selected,
            positions, velocities,
            selected_vehicle_idx,
            transmission_ranges,
            transmission_circle
        ),
        interval=100,
        blit=True
    )

    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    vehicle_scenarios = [1250, 2500, 3750, 5000]

    for n in vehicle_scenarios:
        run_simulation(n)