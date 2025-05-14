import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt


def plot_routes(drones, deliveries, nfzs):
    fig, ax = plt.subplots()

    for drone in drones:
        x, y = drone.start_pos
        ax.scatter(x, y, color='blue', label=f"Drone {drone.id}")
        if hasattr(drone, "route") and drone.route:
            rx = [p[0] for p in drone.route]
            ry = [p[1] for p in drone.route]
            ax.plot(rx, ry, linestyle='--', label=f"Rota {drone.id}")
            for i, point in enumerate(drone.route):
                ax.text(point[0], point[1], f"{i}", fontsize=6)

    for d in deliveries:
        ax.scatter(d.pos[0], d.pos[1], color='green', marker='x')

    for nfz in nfzs:
        polygon = nfz.coordinates + [nfz.coordinates[0]]
        px = [p[0] for p in polygon]
        py = [p[1] for p in polygon]
        ax.plot(px, py, color='red')

    ax.legend()
    plt.title("Drone Rotaları ve No-Fly Zone")
    plt.grid(True)
    plt.savefig("rota_cizimi.png")
    plt.show(block=True)
