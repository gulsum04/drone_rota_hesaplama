
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone

def parse_drone_file(filepath):
    drones = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            drone = Drone(
                id=int(parts[0]),
                max_weight=float(parts[1]),
                battery=int(parts[2]),
                speed=float(parts[3]),
                start_pos=(float(parts[4]), float(parts[5]))
            )
            drones.append(drone)
    return drones

def parse_teslimat_file(filepath):
    teslimatlar = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            teslimat = Teslimat(
                id=int(parts[0]),
                pos=(float(parts[1]), float(parts[2])),
                weight=float(parts[3]),
                priority=int(parts[4]),
                time_window=(parts[5], parts[6])
            )
            teslimatlar.append(teslimat)
    return teslimatlar

def parse_nfz_file(filepath):
    nfzs = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            id = int(parts[0])
            coords = [tuple(map(float, xy.split(','))) for xy in parts[1].split(';')]
            time_range = tuple(parts[2].split(','))
            nfzs.append(NoFlyZone(id, coords, time_range))
    return nfzs
