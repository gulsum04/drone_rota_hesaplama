class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id  # Drone kimliği
        self.max_weight = max_weight  # Taşıma kapasitesi
        self.battery = battery  # Batarya kapasitesi (mAh)
        self.speed = speed  # Hız (m/s)
        self.start_pos = start_pos  # Başlangıç konumu
        self.current_pos = start_pos  # Anlık pozisyon
        self.available = True  # Müsaitlik durumu
        self.available_time = 0  # Şarj sonrası hazır olacağı zaman (simülasyonda kullanılabilir)
        self.route = []  # Alınan rota
        self.energy_used = 0  # Kullanılan enerji toplamı
