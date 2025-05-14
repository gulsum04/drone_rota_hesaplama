
from utils.parser import parse_drone_file, parse_teslimat_file
from algorithms.genetic_algorithm import optimize_routes

def test_senaryo2():
    drones = parse_drone_file("data/drone_verileri.txt")
    deliveries = parse_teslimat_file("data/teslimat_noktalari.txt")

    print("Senaryo 2: Genetik algoritma ile optimizasyon başlatılıyor...")
    best_assignment = optimize_routes(drones, deliveries)

    print("🚁 Teslimat → Drone Atamaları:")
    for i, drone_id in enumerate(best_assignment):
        print(f"📦 Teslimat {deliveries[i].id} → Drone {drone_id}")

if __name__ == "__main__":
    test_senaryo2()
