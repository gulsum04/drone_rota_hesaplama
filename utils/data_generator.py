
import random

def generate_random_drones(n):
    drones = []
    for i in range(1, n+1):
        max_weight = round(random.uniform(5.0, 15.0), 1)
        battery = random.randint(8000, 12000)  # ⚡ Yüksek batarya
        speed = round(random.uniform(3.0, 8.0), 1)
        start_x = round(random.uniform(0, 200), 1)
        start_y = round(random.uniform(0, 200), 1)
        line = f"{i},{max_weight},{battery},{speed},{start_x},{start_y}"
        drones.append(line)
    return drones

def generate_random_deliveries(m):
    deliveries = []
    for i in range(1, m+1):
        x = round(random.uniform(0, 200), 1)
        y = round(random.uniform(0, 200), 1)
        weight = round(random.uniform(1.0, 10.0), 1)
        priority = random.randint(1, 5)
        time_window = ("09:00", "17:00")  # Sabit geniş zaman penceresi
        line = f"{i},{x},{y},{weight},{priority},{time_window[0]},{time_window[1]}"
        deliveries.append(line)
    return deliveries

def generate_random_noflyzones(k):
    noflyzones = []
    for i in range(1, k+1):
        base_x = random.randint(30, 150)
        base_y = random.randint(30, 150)
        width = random.randint(5, 10)
        height = random.randint(5, 10)
        coords = [
            (base_x, base_y),
            (base_x + width, base_y),
            (base_x + width, base_y + height),
            (base_x, base_y + height)
        ]
        coord_str = ";".join([f"{x},{y}" for x, y in coords])
        time_range = "09:00,10:00"
        line = f"{i}|{coord_str}|{time_range}"
        noflyzones.append(line)
    return noflyzones

def save_to_txt(lines, filename):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")
