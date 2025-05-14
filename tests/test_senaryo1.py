
from utils.parser import parse_drone_file, parse_teslimat_file, parse_nfz_file
from algorithms.a_star import a_star
from utils.visualizer import plot_routes

def test_senaryo1():
    drones = parse_drone_file("data/drone_verileri.txt")
    deliveries = parse_teslimat_file("data/teslimat_noktalari.txt")
    nfzs = parse_nfz_file("data/no_fly_zone.txt")

    print(f"Senaryo 1: {len(drones)} drone, {len(deliveries)} teslimat, {len(nfzs)} no-fly zone")

    for drone in drones:
        for delivery in deliveries:
            if delivery.weight <= drone.max_weight and not delivery.assigned:
                rota, enerji = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, nfzs, drone.battery)
                if rota:
                    if drone.battery - enerji < 30:
                        print(f"⚠️ Drone {drone.id} bataryası az, şarj ediliyor...")
                        drone.battery = 100
                    drone.battery -= enerji
                    drone.route = rota
                    delivery.assigned = True
                    drone.start_pos = delivery.pos
                    print(f"✅ Teslimat {delivery.id} başarıyla atandı.")
                    break
                else:
                    print(f"❌ Rota bulunamadı → Drone {drone.id} için teslimat {delivery.id}")

    plot_routes(drones, deliveries, nfzs)

if __name__ == "__main__":
    test_senaryo1()
