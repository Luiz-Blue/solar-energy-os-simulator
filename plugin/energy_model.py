class PhotovoltaicEnergyModel:
    """
    Modelo de PRODUÇÃO e ARMAZENAMENTO de energia fotovoltaica
    com múltiplas células de coleta.

    Cada célula representa um conjunto independente de painéis.
    """

    def __init__(self, E_init, E_max, panel_areas, efficiency):
        self.E = E_init
        self.E_max = E_max
        self.panel_areas = panel_areas  # (m²)
        self.eta = efficiency
        self.last_generation = [0, 0, 0]

    def generate(self, irradiance):
        """
        Geração total:
        G_total(t) = sum(I(t) * A_i * eta)
        """
        generations = []
        for A in self.panel_areas:
            generations.append(irradiance * A * self.eta)

        self.last_generation = generations
        G_total = sum(generations)
        self.E = min(self.E + G_total, self.E_max)
        return G_total

    def available_energy(self):
        return self.E

    def generation_by_cell(self):
        return self.last_generation