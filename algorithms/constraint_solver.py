from constraint import Problem
from datetime import datetime
from algorithms.a_star import in_noflyzone
from utils.parser import parse_nfz_file
from utils.distance import euclidean

def assign_deliveries_csp(drones, deliveries):
    nfzs = parse_nfz_file("data/no_fly_zone.txt")
    current_time = datetime.now().time()

    problem = Problem()

    # Teslimatları önceliğe göre sırala (yüksek öncelik önce)
    sorted_deliveries = sorted(deliveries, key=lambda x: -x.priority)
    delivery_ids = [d.id for d in sorted_deliveries]
    drone_ids = [d.id for d in drones]

    # Drone başlangıç batarya durumunu izlemek için harita
    drone_battery = {d.id: d.battery for d in drones}
    drone_positions = {d.id: d.start_pos for d in drones}

    # Her teslimat için atanabilir drone listesi
    for delivery_id in delivery_ids:
        problem.addVariable(delivery_id, drone_ids)

    def valid_assignment(delivery_id_val, drone_id_val):
        delivery = next(d for d in deliveries if d.id == delivery_id_val)
        drone = next(d for d in drones if d.id == drone_id_val)

        # Ağırlık sınırı
        if delivery.weight > drone.max_weight:
            return False

        # No-fly zone kontrolü (orta noktadan geçiyor mu)
        mid_point = (
            (delivery.pos[0] + drone.start_pos[0]) / 2,
            (delivery.pos[1] + drone.start_pos[1]) / 2
        )
        if in_noflyzone(mid_point, nfzs, current_time):
            return False

        # Enerji kontrolü (drone başlangıç pozisyonuna göre)
        mesafe = euclidean(drone.start_pos, delivery.pos)
        enerji_gerekli = mesafe * delivery.weight
        if enerji_gerekli > drone.battery:
            return False

        return True

    # Her teslimat için uygunluk kısıtı eklenir
    for delivery_id in delivery_ids:
        problem.addConstraint(
            lambda drone_id_val, delivery_id_val=delivery_id: valid_assignment(delivery_id_val, drone_id_val),
            [delivery_id]
        )

    solution = problem.getSolution()

    if solution:
        print("📋 CSP Atama Sonuçları:")
        for delivery_id, drone_id in solution.items():
            print(f"🚚 Teslimat {delivery_id} → Drone {drone_id}")
    else:
        print("⚠️ Geçerli bir CSP çözümü bulunamadı.")

    return solution
