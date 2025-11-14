

class BruteForce(Tower):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.range = 200
        self.damage = 5
        self.fire_rate = 0.5
