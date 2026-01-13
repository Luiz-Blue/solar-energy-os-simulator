class EnergyModel:
    def __init__(self, solar_rate, battery, battery_max):
        self.solar_rate = solar_rate      # energia gerada por ciclo
        self.battery = battery
        self.battery_max = battery_max

    def available_energy(self):
        return self.battery

    def generate(self):
        self.battery += self.solar_rate
        if self.battery > self.battery_max:
            self.battery = self.battery_max

    def consume(self, amount):
        self.battery -= amount
        if self.battery < 0:
            self.battery = 0
