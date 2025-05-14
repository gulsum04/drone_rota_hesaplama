import heapq
from utils.distance import euclidean
from datetime import datetime

def a_star(start, goal, weight, priority, nfz_list, drone_battery):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    max_iterations = 20000
    iterations = 0

    while open_set:
        iterations += 1
        if iterations > max_iterations:
            print(f"⛔ A* maksimum iterasyona ulaştı: {start} → {goal}")
            return None, None

        _, current = heapq.heappop(open_set)

        if euclidean(current, goal) < 10:
            total_energy = g_score[current]
            print(f"🎯 Hedefe ulaşıldı: {current} → {goal}, Enerji: {total_energy:.1f}, Batarya: {drone_battery}")
            if total_energy <= drone_battery:
                return reconstruct_path(came_from, current), total_energy
            else:
                print("⚠️ Batarya yetmiyor.")
                return None, total_energy

        neighbors = generate_neighbors(current)

        for neighbor in neighbors:
            step_distance = euclidean(current, neighbor)
            tentative_g = g_score[current] + step_distance * weight

            if in_noflyzone(neighbor, nfz_list, datetime.now().time()):
                tentative_g += 1000  # Ceza uygulanıyor

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None, None

def generate_neighbors(pos):
    step = 50
    return [
        (pos[0] + step, pos[1]), (pos[0] - step, pos[1]),
        (pos[0], pos[1] + step), (pos[0], pos[1] - step),
        (pos[0] + step, pos[1] + step), (pos[0] - step, pos[1] + step),
        (pos[0] + step, pos[1] - step), (pos[0] - step, pos[1] - step)
    ]

def in_noflyzone(pos, nfz_list, current_time):
    for nfz in nfz_list:
        if is_inside_polygon(pos, nfz.coordinates):
            start = datetime.strptime(nfz.active_time[0], "%H:%M").time()
            end = datetime.strptime(nfz.active_time[1], "%H:%M").time()
            if start <= current_time <= end:
                return True
    return False

def is_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    px1, py1 = polygon[0]
    for i in range(n + 1):
        px2, py2 = polygon[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
        px1, py1 = px2, py2
    return inside

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]
