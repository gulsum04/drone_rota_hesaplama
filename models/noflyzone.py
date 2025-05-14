class NoFlyZone:
    def __init__(self, id, coordinates, active_time):
        self.id = id
        self.coordinates = coordinates  # Liste [(x1,y1), (x2,y2), ...]
        self.active_time = active_time  # Tuple ("09:30", "11:00")
