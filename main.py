
import time
import heapq
from utils.data_generator import *
from utils.parser import parse_drone_file, parse_teslimat_file, parse_nfz_file
from utils.visualizer import plot_routes
from algorithms.a_star import a_star
from algorithms.constraint_solver import assign_deliveries_csp
from algorithms.genetic_algorithm import optimize_routes
import pandas as pd
import os
from datetime import datetime

def veri_uret(dron_sayisi=3, teslimat_sayisi=5, nfz_sayisi=1):
    print("🔄 Veri üretiliyor...")
    save_to_txt(generate_random_drones(dron_sayisi), "data/drone_verileri.txt")
    save_to_txt(generate_random_deliveries(teslimat_sayisi), "data/teslimat_noktalari.txt")
    save_to_txt(generate_random_noflyzones(nfz_sayisi), "data/no_fly_zone.txt")
    print("✅ Veri üretildi.\n")

def senaryo_astar():
    print("\n===== 🚀 A* Algoritması =====")
    start = time.time()
    drones = parse_drone_file("data/drone_verileri.txt")
    deliveries = parse_teslimat_file("data/teslimat_noktalari.txt")
    nfzs = parse_nfz_file("data/no_fly_zone.txt")

    # Teslimatları önceliğe göre sıralayıp Min-Heap'e koy
    teslimat_heap = []
    for delivery in deliveries:
        heapq.heappush(teslimat_heap, (-delivery.priority, delivery))

    tamamlanan = 0

    for drone in drones:
        while teslimat_heap:
            _, delivery = heapq.heappop(teslimat_heap)
            if delivery.weight > drone.max_weight or delivery.assigned:
                continue

            print(f"🔍 Drone {drone.id} → Teslimat {delivery.id}")
            rota, enerji = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, nfzs, drone.battery)
            if rota:
                if drone.battery - enerji < 30:
                    print(f"⚠️ Drone {drone.id} bataryası düşük! Şarj ediliyor...")
                    drone.battery = 100
                    drone.available_time += 15  # 15 dakikalık şarj süresi

                drone.battery -= enerji
                drone.route = rota
                drone.start_pos = delivery.pos
                delivery.assigned = True
                tamamlanan += 1
                print("✅ Rota bulundu ve teslimat yapıldı.")
            else:
                print("❌ Rota bulunamadı.")
    end = time.time()
    print(f"\n📦 A* Tamamlanan: {tamamlanan}/{len(deliveries)}")
    print(f"⏱ Süre: {round(end - start, 3)} saniye\n")
    plot_routes(drones, deliveries, nfzs)
    return tamamlanan, round(end - start, 3)

def senaryo_csp():
    print("\n===== 🧩 CSP Atama =====")
    start = time.time()
    drones = parse_drone_file("data/drone_verileri.txt")
    deliveries = parse_teslimat_file("data/teslimat_noktalari.txt")
    sonuc = assign_deliveries_csp(drones, deliveries)
    end = time.time()
    atanan = len(sonuc) if sonuc else 0
    print(f"\n📦 CSP Atanan: {atanan}/{len(deliveries)}")
    print(f"⏱ Süre: {round(end - start, 3)} saniye\n")
    return atanan, round(end - start, 3)

def senaryo_ga():
    print("\n===== 🧬 Genetik Algoritma =====")
    start = time.time()
    drones = parse_drone_file("data/drone_verileri.txt")
    deliveries = parse_teslimat_file("data/teslimat_noktalari.txt")
    best = optimize_routes(drones, deliveries)
    end = time.time()
    kullanilan_drone = len(set(best))
    print(f"\n📦 GA Drone Kullanımı: {kullanilan_drone}/{len(drones)}")
    print(f"⏱ Süre: {round(end - start, 3)} saniye\n")
    return kullanilan_drone, round(end - start, 3)

def log_csv(astar, csp, ga):
    os.makedirs("report", exist_ok=True)
    csv_path = "report/metrics.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    veri = [
        {"Tarih": now, "Algoritma": "A*", "Tamamlanan": astar[0], "Toplam": 5, "Süre (sn)": astar[1]},
        {"Tarih": now, "Algoritma": "CSP", "Tamamlanan": csp[0], "Toplam": 5, "Süre (sn)": csp[1]},
        {"Tarih": now, "Algoritma": "GA", "Tamamlanan": ga[0], "Toplam": 5, "Süre (sn)": ga[1]}
    ]
    df = pd.DataFrame(veri)
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(csv_path, index=False)
    print("📄 Sonuçlar metrics.csv dosyasına kaydedildi.")

if __name__ == "__main__":
    print("\n============================================================")
    print("🔎 DRONE ROTA OPTİMİZASYONU TESTİ (KARŞILAŞTIRMA)")
    print("============================================================\n")
    veri_uret(dron_sayisi=3, teslimat_sayisi=5, nfz_sayisi=1)
    astar_sonuc = senaryo_astar()
    csp_sonuc = senaryo_csp()
    ga_sonuc = senaryo_ga()
    log_csv(astar_sonuc, csp_sonuc, ga_sonuc)
