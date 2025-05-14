import math

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def distance_cost(p1, p2, weight, priority):
    distance = euclidean(p1, p2)
    penalty = (6 - priority) * 100  # Öncelik cezası (1-5)
    return distance * weight + penalty
