class Teslimat:
    def __init__(self, id, pos, weight, priority, time_window):
        self.id = id  # Teslimat kimliği
        self.pos = pos  # Teslimat pozisyonu
        self.weight = weight  # Paket ağırlığı
        self.priority = priority  # 1–5 arası öncelik seviyesi
        self.time_window = time_window  # ("09:00", "10:00") gibi kabul edilebilir zaman
        self.assigned = False  # Atandı mı?
    def __lt__(self, other):
        return self.id < other.id  # aynı öncelik varsa ID'ye göre karşılaştırılır